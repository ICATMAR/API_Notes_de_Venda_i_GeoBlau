import base64
import io
import json
import logging
import os
import time
import uuid
from datetime import datetime

import pandas as pd
import requests
import websocket
from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Descarrega les dades de la flota europea automàticament (via API)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--local-file",
            type=str,
            help="Ruta a un arxiu Excel local per testejar el procés sense descarregar-lo de l'API.",
        )

    def handle(self, *args, **options):
        self.warnings = []
        self.current_step = "Inicialització"

        # --- CONFIGURACIÓ DE LOGS ---
        log_dir = "/app/logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "sync_fleet.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, mode="a"), logging.StreamHandler()],
        )

        logger.info("=== INICIANT SINCRONITZACIÓ DE VESSELS ===")

        # --- PETICIÓ API (Substitució de Selenium) ---
        self.current_step = "Preparant petició API"
        local_file = options.get("local_file")

        try:
            if local_file:
                self.current_step = "Carregant Excel local"
                logger.info(f"Opció --local-file detectada. Ometent API i llegint: {local_file}")

                if not os.path.exists(local_file):
                    raise FileNotFoundError(f"L'arxiu indicat no existeix: {local_file}")

                with open(local_file, "rb") as f:
                    file_content = f.read()
                logger.info(f"✅ Fitxer local carregat a la memòria correctament ({len(file_content)} bytes).")

            else:
                self.current_step = "Fent petició a l'API de Fleet Europa"
                api_url = "https://appsync-api-fleet-europa.ocean-store.ec.europa.eu/graphql"
                headers = {
                    "content-type": "application/json",
                    "x-api-key": "da2-qi43aom7lbfezjlxndlvet3szq",
                    "origin": "https://vessel-register.oceans-and-fisheries.ec.europa.eu",
                    "referer": "https://vessel-register.oceans-and-fisheries.ec.europa.eu/",
                    "user-agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
                    ),
                }

                file_name_ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                file_name = f"Search_Vessels_Full_{file_name_ts}_{str(uuid.uuid4())[:4]}"
                req_id = str(uuid.uuid4())

                payload = {
                    "operationName": "MyQuery",
                    "query": (
                        "mutation MyQuery ($filter: SearchVesselFilter,$fileName: String!)"
                        "{SearchVesselQuery(filter: $filter,orderBy: [event_start_date_desc],"
                        'requestId: "%s",fileName: $fileName)}'
                    )
                    % req_id,
                    "variables": {
                        "filter": {
                            "flagStateOption": "other",
                            "flagState": ["ESP"],
                            "vesselTypeOption": "allFishingVessels",
                            "vesselType": [],
                            "startPeriodDate": None,
                            "endPeriodDate": None,
                            "periodOption": "fullHistory",
                            "vesselIdentifier": "",
                            "eventType": [],
                            "loaFrom": "",
                            "loaTo": "",
                            "gtFrom": "",
                            "gtTo": "",
                            "mainPowerFrom": "",
                            "mainPowerTo": "",
                            "publicAid": [],
                            "constructionYearFrom": "",
                            "constructionYearTo": "",
                            "nationalLicence": "all",
                            "vms": "all",
                            "ircs": "all",
                            "ers": "all",
                            "ersExemption": "all",
                            "ais": "all",
                            "gearMain": [],
                            "gearAux": [],
                            "fleetSegmentOption": "other",
                            "fleetSegment": [],
                            "registrationPlace": [],
                            "maritimeFront": [],
                            "nuts": [],
                            "csvType": "full",
                        },
                        "fileName": file_name,
                    },
                }

                logger.info("Enviant mutació GraphQL...")
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Resposta rebuda: {data}")

                # 2. CONEXIÓ WEBSOCKET (Esperar la URL d'Amazon S3)
                self.current_step = "Connexió WebSocket per descarregar"
                logger.info("Iniciant connexió WebSocket per obtenir la URL final...")

                host = "appsync-api-fleet-europa.ocean-store.ec.europa.eu"
                api_key = "da2-qi43aom7lbfezjlxndlvet3szq"

                ws_header = {"host": host, "x-api-key": api_key}
                b64_header = base64.b64encode(json.dumps(ws_header).encode()).decode()
                b64_payload = base64.b64encode(json.dumps({}).encode()).decode()

                wss_url = f"wss://{host}/graphql/realtime?header={b64_header}&payload={b64_payload}"

                ws = websocket.create_connection(wss_url, subprotocols=["graphql-ws"], timeout=60)
                ws.send(json.dumps({"type": "connection_init"}))

                # Subscripció al Job
                sub_msg = {
                    "id": str(uuid.uuid4()),
                    "type": "start",
                    "payload": {
                        "data": json.dumps(
                            {
                                "query": (
                                    '\n subscription MySubscription($jobId: ID = "") '
                                    "{\n onAsyncDataCompleted(jobId: $jobId) "
                                    "{\n asyncData\n jobId\n }\n }\n "
                                ),
                                "variables": {"jobId": req_id},
                            }
                        ),
                        "extensions": {"authorization": {"host": host, "x-api-key": api_key}},
                    },
                }
                ws.send(json.dumps(sub_msg))

                final_url = None
                timeout_limit = time.time() + 600  # 10 minuts màxim d'espera

                while time.time() < timeout_limit:
                    res = ws.recv()
                    res_data = json.loads(res)

                    if res_data.get("type") == "data":
                        async_str = (
                            res_data.get("payload", {}).get("data", {}).get("onAsyncDataCompleted", {}).get("asyncData")
                        )
                        if async_str:
                            async_info = json.loads(async_str)
                            progress = async_info.get("progress")
                            status = async_info.get("status")

                            if progress is not None:
                                logger.info(f"Generant arxiu remot... {progress}% ({status})")

                            if status == "done" and async_info.get("csv"):
                                final_url = async_info.get("csv")
                                break

                ws.close()

                if not final_url:
                    raise Exception("Timeout esperant que l'API de Fleet Europa generi l'arxiu (via WebSocket).")

                self.current_step = "Descarregant l'Excel"
                logger.info("Arxiu llest! Descarregant dades des de l'S3...")
                excel_response = requests.get(final_url, timeout=300)
                excel_response.raise_for_status()

                file_content = excel_response.content
                logger.info(f"✅ Fitxer descarregat a la memòria correctament ({len(file_content)} bytes).")

            self.current_step = "Processar Excel i Dades"
            if file_content:
                self.current_step = "Carregar a Staging"
                df_new = self.process_excel(file_content)
                if df_new is not None and not df_new.empty:
                    self.load_to_staging(df_new)
                else:
                    logger.info("✅ Cap registre nou per processar.")

            # Enviar mail d'èxit (Test)
            # send_email_robust(
            #    f"Èxit Sync UE Fleet Rregister diari ({datetime.now().strftime('%Y-%m-%d')}) ✅",
            #    f"Procés completat correctament.\nRegistres nous: "
            #    f"{len(df_new) if 'df_new' in locals() and df_new is not None else 0}",
            #    ["arampuig.work@gmail.com"],
            # )

            logger.info("=== PROCÉS COMPLETAT AMB ÈXIT ===")

        except Exception as e:
            logger.error(f"ERROR FATAL DURANT L'EXECUCIÓ: {e}")

            # Enviar mail d'error
            warnings_text = "\n".join(self.warnings) if self.warnings else "Cap warning detectat."
            error_summary = (
                f"Pas fallit: {self.current_step}\nError: {str(e)}\n\n--- WARNINGS ACUMULATS ---\n{warnings_text}"
            )

            recipients = (
                [a[1] for a in settings.NOTIFICATION_EMAIL]
                if getattr(settings, "NOTIFICATION_EMAIL", None)
                else ["arampuig.work@gmail.com"]
            )

            send_email_robust(
                f"❌ Error Sync Fleet Selenium ({datetime.now().strftime('%Y-%m-%d')})",
                f"{error_summary}",
                recipients,
            )

            raise e

    def process_excel(self, file_content):
        logger.info("Processant Excel i comparant amb BBDD...")
        try:
            df = pd.read_excel(io.BytesIO(file_content), dtype=str)

            logger.info(f"Columnes originals de l'Excel: {df.columns.tolist()}")
            # 1. Neteja agressiva: Traiem espais innecessaris i posem TOT en minúscules
            original_cols = df.columns.tolist()
            df.columns = df.columns.str.strip().str.lower()
            logger.info(f"Columnes originals de l'Excel: {original_cols}")
            logger.info(f"Columnes normalitzades (minúscules): {df.columns.tolist()}")

            # Mapping robust: l'Excel de la nova API té noms lleugerament diferents al CSV antic
            # 2. Diccionari unificat amb totes les variants en minúscules sense claus duplicades
            column_mapping_robust = {
                "Code": ["cfr", "vessel number", "code", "vessel cfr"],
                "EventCode": ["event", "event code", "event type", "event type code"],
                "EventStartDate": ["event start date", "start date", "event date"],
                "EventEndDate": ["event end date", "end date"],
                "LicenceInd": ["licence indicator", "license indicator", "national licence"],
                "RegistrationNum": ["registration number", "external marking", "fleet register number"],
                "Name": ["name of vessel", "vessel name", "vessel's name", "name"],
                "TempPortVal": [
                    "place of registration code",
                    "place of registration",
                    "port of registration",
                    "registration port",
                    "port base",
                    "base port",
                    "port",
                    "place of registration name",
                ],
                "IRCS": ["ircs", "international radio call sign", "call sign", "ircs indicator"],
                "VMS": ["vms indicator", "vms"],
                "GearMainCode": ["main fishing gear", "main gear", "gear main", "fishing gear"],
                "GearSecCode": ["subsidiary fishing gear 1", "subsidiary gear 1", "subsidiary gear", "gear subsidiary"],
                "LOA_m": ["loa (m)", "loa", "length overall", "length overall (loa)", "length"],
                "LBP_m": ["lbp (m)", "lbp", "length between perpendiculars", "length between perpendiculars (lbp)"],
                "TRB": ["other tonnage", "other_tonnage"],
                "GT": ["tonnage gt", "gross tonnage", "gross tonnage (gt)", "gt", "tonnage", "tonnage gts"],
                "PowerMain_kW": [
                    "power of main engine",
                    "main engine power",
                    "power of main engine (kw)",
                    "main power",
                ],
                "PowerAux_kW": [
                    "power of auxiliary engine",
                    "auxiliary engine power",
                    "power of auxiliary engine (kw)",
                ],
                "AIS": ["ais indicator", "ais"],
                "HullMaterial": ["hull material", "hull"],
                "ServiceStartingDate": ["date of entry into service", "entry into service date", "construction year"],
                "MMSI": ["mmsi"],
            }

            rename_dict = {}
            for final_col, possible_names in column_mapping_robust.items():
                for possible_name in possible_names:
                    if possible_name in df.columns:
                        rename_dict[possible_name] = final_col
                        break

            df = df.rename(columns=rename_dict)
            logger.info(f"Columnes mapejades amb èxit: {list(rename_dict.values())}")

            missing_cols = set(column_mapping_robust.keys()) - set(rename_dict.values())
            if missing_cols:
                logger.warning(f"⚠️ Atenció: No s'han mapejat aquestes columnes: {missing_cols}")
                logger.warning(f"⚠️ ATENCIÓ: Les següents columnes NO s'han trobat a l'Excel: {missing_cols}")
                logger.warning(
                    "   => Revisa el log 'Columnes normalitzades (minúscules)' "
                    "de dalt per identificar quin nom tenen ara."
                )

            date_cols = ["EventStartDate", "EventEndDate", "ServiceStartingDate"]
            for col in date_cols:
                if col in df.columns:
                    # El log indicava format YYYY-MM-DD, per tant dayfirst=False és més segur per evitar warnings/errors
                    df[col] = pd.to_datetime(df[col], dayfirst=False, errors="coerce").dt.date

                    # LOGGING: Identificar registres amb dates nul·les
                    null_dates = df[df[col].isna()]
                    if not null_dates.empty:
                        msg = f"⚠️  {col}: {len(null_dates)} registres tenen data invàlida o buida (NaT)."
                        logger.warning(msg)
                        self.warnings.append(msg)

            # Transformació de booleans (Y/N -> true/false)
            for col in ["LicenceInd", "AIS", "VMS"]:
                if col in df.columns:
                    df[col] = df[col].map({"Y": "true", "N": "false", "y": "true", "n": "false"})

            # --- FIX: Normalització per comparació ---
            # Convertim NaT i NaN a None perquè coincideixi amb el que retorna la BBDD (None)
            df = df.replace({pd.NaT: None})
            df = df.where(pd.notnull(df), None)

            # Assegurar que la connexió a la BBDD està viva després de l'espera de Selenium
            connection.close_if_unusable_or_obsolete()

            with connection.cursor() as cursor:
                cursor.execute('SELECT "Code", "EventStartDate", "EventEndDate" FROM public.vessel')
                existing_data = cursor.fetchall()

                # --- GESTIÓ DE PORTS (BasePortCode, BasePortName, BasePortId) ---
                cursor.execute('SELECT "Code", "AL5", "Name", "Id" FROM public.port_all')
                ports_data = cursor.fetchall()

            # Creem diccionaris de cerca per Code i AL5
            port_by_code = {}
            port_by_al5 = {}
            for p_code, p_al5, p_name, p_id in ports_data:
                port_obj = {"Code": p_code, "Name": p_name, "Id": p_id}
                # Code sol ser numèric a la BBDD, convertim a string per comparar amb CSV
                port_by_code[str(p_code).strip()] = port_obj
                if p_al5:
                    port_by_al5[str(p_al5).strip()] = port_obj

            def resolve_port(row):
                val = str(row.get("TempPortVal", "")).strip()
                # Si és buit o nan, retornem nuls
                if not val or val.lower() == "nan":
                    return None, None, None

                # 1. Intentar per Code
                if val in port_by_code:
                    p = port_by_code[val]
                    return p["Code"], p["Name"], p["Id"]

                # 2. Intentar per AL5
                if val in port_by_al5:
                    p = port_by_al5[val]
                    return p["Code"], p["Name"], p["Id"]

                return None, None, None

            # Apliquem la resolució de ports
            port_results = df.apply(resolve_port, axis=1, result_type="expand")
            df[["BasePortCode", "BasePortName", "BasePortId"]] = port_results

            # Assegurar longitud màxima de 50 per BasePortName (per evitar DataError)
            df["BasePortName"] = df["BasePortName"].apply(lambda x: str(x)[:50] if x and pd.notnull(x) else x)

            # --- ESTADÍSTIQUES DE CODI ---
            db_codes = set(str(r[0]).strip() for r in existing_data)
            csv_codes = set(df["Code"].astype(str).str.strip())
            intersection = db_codes.intersection(csv_codes)

            logger.info("📊 ESTADÍSTIQUES DE VESSEL CODES:")
            logger.info(f"   - Codes de vessel al CSV: {len(csv_codes)}")
            logger.info(f"   - Codes de vessel a BBDD: {len(db_codes)}")
            logger.info(f"   - Codes de vessel coincidents: {len(intersection)}")
            logger.info(f"   - Codes de vessel nous al CSV: {len(csv_codes - db_codes)}")
            logger.info(f"   - Codes de vessel a BBDD no al CSV: {len(db_codes - csv_codes)}")

            # Creem el set de claus existents normalitzant tipus (datetime -> date)
            existing_keys = set()
            for code, start_date, end_date in existing_data:
                if not start_date:
                    continue
                # Si la BBDD retorna datetime (timestamp), ho passem a date
                if isinstance(start_date, datetime):
                    start_date = start_date.date()
                if isinstance(end_date, datetime):
                    end_date = end_date.date()
                existing_keys.add((str(code).strip(), start_date, end_date))

            def is_new(row):
                if "Code" not in row or "EventStartDate" not in row:
                    return False
                return (str(row["Code"]).strip(), row["EventStartDate"], row["EventEndDate"]) not in existing_keys

            df_filtered = df[df.apply(is_new, axis=1)]

            logger.info(f"Registres totals: {len(df)} | Nous/Modificats: {len(df_filtered)}")
            return df_filtered

        except Exception as e:
            logger.error(f"Error processant CSV: {str(e)}")
            raise e

    def load_to_staging(self, df):
        logger.info("Inserint a vessel_auto_download...")

        # Assegurar connexió viva abans d'inserir
        connection.close_if_unusable_or_obsolete()

        with connection.cursor() as cursor:
            # Ampliar columna BasePortName a 50 caràcters si cal
            try:
                cursor.execute('ALTER TABLE public.vessel_auto_download ALTER COLUMN "BasePortName" TYPE varchar(50)')
            except Exception as e:
                msg = f"No s'ha pogut alterar la taula (potser ja està modificada): {e}"
                logger.warning(msg)
                self.warnings.append(msg)

            cursor.execute("TRUNCATE TABLE public.vessel_auto_download RESTART IDENTITY")

        # Nota: La neteja de NaT/NaN ja s'ha fet a process_csv, així que aquí ja tenim None

        valid_columns = [
            "Code",
            "EventCode",
            "EventStartDate",
            "EventEndDate",
            "LicenceInd",
            "RegistrationNum",
            "Name",
            "BasePortName",
            "BasePortCode",
            "BasePortId",
            "IRCS",
            "VMS",
            "GearMainCode",
            "GearSecCode",
            "LOA_m",
            "LBP_m",
            "GT",
            "TRB",
            "PowerMain_kW",
            "PowerAux_kW",
            "AIS",
            "HullMaterial",
            "ServiceStartingDate",
            "MMSI",
        ]
        cols_to_insert = [c for c in df.columns if c in valid_columns]

        if not cols_to_insert:
            return

        columns_sql = ", ".join([f'"{c}"' for c in cols_to_insert])
        placeholders = ", ".join(["%s"] * len(cols_to_insert))
        query = f"INSERT INTO public.vessel_auto_download ({columns_sql}) VALUES ({placeholders})"  # nosec

        data = [tuple(x) for x in df[cols_to_insert].to_numpy()]

        with connection.cursor() as cursor:
            cursor.executemany(query, data)
        logger.info("✅ Càrrega a staging completada.")


def send_email_robust(subject, message, recipient_list):
    """Envia correu de forma robusta gestionant la connexió."""
    try:
        # Usem get_connection() per assegurar una connexió neta cada vegada.
        # El 'with' s'encarrega de tancar-la correctament.
        with get_connection(fail_silently=False) as connection:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                connection=connection,
            )
        logger.info("Email enviat correctament.")
    except Exception as e:
        logger.error(f"❌ Error CRÍTIC enviant mail: {e}")
        logger.error("   Verifica la configuració SMTP al fitxer .env (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, etc.)")
