import io
import logging
import os
import time
import zipfile
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.core.management.base import BaseCommand
from django.db import connection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Descarrega les dades de la flota europea automàticament (Headless)"

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

        # --- CONFIGURACIÓ SELENIUM ---
        self.current_step = "Configuració Selenium"
        download_dir = "/app/downloads"
        os.makedirs(download_dir, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        prefs = {
            "download.default_directory": "/home/seluser/Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = None
        try:
            driver = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", options=chrome_options)
            wait = WebDriverWait(driver, 20)

            # 1. Accedir a la web
            self.current_step = "Accedint a la web"
            url = "https://webgate.ec.europa.eu/fleet-europa/search_en"
            logger.info(f"Accedint a: {url}")
            driver.get(url)

            # 2. Gestionar Cookies
            self.current_step = "Gestionar Cookies"
            try:
                cookie_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.wt-cck-btn-accept"))
                )
                cookie_btn.click()
                logger.info("Banner de cookies acceptat.")
                time.sleep(1)
            except Exception:
                logger.info("No s'ha detectat banner de cookies o ja estava acceptat.")

            # 3. Seleccionar País [ESP] (Lògica Robusta JS)
            self.current_step = "Seleccionar País"
            logger.info("Seleccionant país [ESP] via JS...")
            driver.execute_script("$('#country-sel').val('ESP').trigger('change');")
            logger.info("País forçat via JS.")
            time.sleep(1)

            # 4. Seleccionar 'All Vessels'
            self.current_step = "Seleccionar All Vessels"
            logger.info("Marcant opció 'All Vessels'...")
            try:
                radio_label_css = "label[for='period1']"
                radio_label = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, radio_label_css)))
                driver.execute_script("arguments[0].click();", radio_label)
            except Exception as e:
                logger.error("Error marcant 'All Vessels'.")
                raise e

            # 5. Clicar Download
            self.current_step = "Clicar Download"
            logger.info("Clicant botó de descàrrega...")
            download_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.download-btn")))
            driver.execute_script("arguments[0].click();", download_btn)

            # Esperar fitxer
            self.current_step = "Esperant fitxer"
            logger.info("Esperant fitxer...")
            timeout = 120
            start_time = time.time()
            zip_path = None

            while time.time() - start_time < timeout:
                files = os.listdir(download_dir)
                valid_files = [
                    f for f in files if not f.endswith(".crdownload") and not f.endswith(".tmp") and f.endswith(".zip")
                ]

                if valid_files:
                    zip_path = os.path.join(download_dir, valid_files[0])
                    if os.path.getsize(zip_path) > 0:
                        logger.info(f"✅ Fitxer detectat: {zip_path}")
                        break
                time.sleep(1)

            if not zip_path:
                raise Exception("Timeout: No s'ha descarregat cap fitxer ZIP vàlid.")

            # 6. Processar ZIP i CSV
            self.current_step = "Processar ZIP i CSV"
            csv_content = self.extract_zip(zip_path)

            # Neteja: Eliminar el fitxer ZIP un cop llegit
            if os.path.exists(zip_path):
                os.remove(zip_path)
                logger.info(f"🗑️ Fitxer ZIP eliminat per alliberar espai: {zip_path}")

            if csv_content:
                self.current_step = "Carregar a Staging"
                df_new = self.process_csv(csv_content)
                if df_new is not None and not df_new.empty:
                    self.load_to_staging(df_new)
                else:
                    logger.info("✅ Cap registre nou per processar.")

            # Enviar mail d'èxit (Test)
            send_email_robust(
                f"Èxit Sync UE Fleet Rregister diari ({datetime.now().strftime('%Y-%m-%d')}) ✅",
                f"Procés completat correctament.\nRegistres nous: "
                f"{len(df_new) if 'df_new' in locals() and df_new is not None else 0}",
                ["arampuig.work@gmail.com"],
            )

            logger.info("=== PROCÉS COMPLETAT AMB ÈXIT ===")

        except Exception as e:
            logger.error(f"ERROR FATAL DURANT L'EXECUCIÓ: {e}")
            if driver:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                error_shot = os.path.join(download_dir, f"error_{ts}.png")
                driver.save_screenshot(error_shot)
                logger.info(f"Captura d'error guardada a: {error_shot}")

            # Enviar mail d'error
            warnings_text = "\n".join(self.warnings) if self.warnings else "Cap warning detectat."
            error_summary = (
                f"Pas fallit: {self.current_step}\nError: {str(e)}\n\n--- WARNINGS ACUMULATS ---\n{warnings_text}"
            )

            send_email_robust(
                f"❌ Error Sync Fleet Selenium ({datetime.now().strftime('%Y-%m-%d')})",
                f"{error_summary}\n\nCaptura guardada al servidor: {error_shot if 'error_shot' in locals() else 'N/A'}",
                ["apuig@icatmar.cat"],
            )

            raise e

        finally:
            if driver:
                driver.quit()

    def extract_zip(self, zip_path):
        try:
            logger.info(f"Extreient ZIP: {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as z:
                filename = z.namelist()[0]
                with z.open(filename) as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error extreient ZIP: {e}")
            raise e

    def process_csv(self, csv_content):
        logger.info("Processant CSV i comparant amb BBDD...")
        try:
            df = pd.read_csv(io.BytesIO(csv_content), sep=";", encoding="latin1", dtype=str)

            column_mapping = {
                "CFR": "Code",
                "Event": "EventCode",
                "Event Start Date": "EventStartDate",
                "Event End Date": "EventEndDate",
                "Licence indicator": "LicenceInd",
                "Registration Number": "RegistrationNum",
                "Name of vessel": "Name",
                "Place of registration": "TempPortVal",
                "IRCS": "IRCS",
                "VMS": "VMS",
                "Main fishing gear": "GearMainCode",
                "Subsidiary fishing gear 1": "GearSecCode",
                "LOA": "LOA_m",
                "LBP": "LBP_m",
                "Other tonnage": "TRB",
                "Tonnage GT": "GT",
                "Power of main engine": "PowerMain_kW",
                "Power of auxiliary engine": "PowerAux_kW",
                "AIS Indicator": "AIS",
                "Hull material": "HullMaterial",
                "Date of entry into service": "ServiceStartingDate",
            }
            df = df.rename(columns=column_mapping)

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
            for col in ["LicenceInd", "AIS"]:
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
