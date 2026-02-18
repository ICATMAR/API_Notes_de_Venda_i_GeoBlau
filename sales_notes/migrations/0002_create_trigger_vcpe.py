# /API_dev/sales_notes/migrations/0002_create_trigger_vcpe.py

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales_notes", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- 1. Crear la taula destí (vcpe_auto_download)
            -- Utilitzem l'estructura exacta proporcionada.
            -- Nota: Comentem les FKs per evitar errors si les taules mestres no existeixen a l'entorn de dev.
            CREATE TABLE IF NOT EXISTS public.vcpe_auto_download (
                "VesselCode" varchar(12) NULL,
                "VesselName" varchar(50) NULL,
                "VesselType" varchar(30) NULL,
                "SaleNumber" varchar(30) NULL,
                "Lot" varchar(30) NULL,
                "Calibre" varchar(40) NULL,
                "Size" varchar(20) NULL,
                "DocType" varchar(10) NULL,
                "SpecieCode" bpchar(3) NULL,
                "SpecieName" varchar(30) NULL,
                "PortName" varchar(50) NULL,
                "Date" date NULL,
                "PortType" varchar(40) NULL,
                "Freshness" varchar(20) NULL,
                "Presentation" varchar(50) NULL,
                "Conservation" varchar(20) NULL,
                "FishingArtCode" varchar(10) NULL,
                "FishingArtName" varchar(100) NULL,
                "VesselOwnerCode" varchar(50) NULL,
                "OtherFishingArts" varchar(30) NULL,
                "Weight" numeric(20, 3) NULL,
                "Amount" numeric(20, 4) NULL,
                "Id" bigserial NOT NULL,
                "PortId" int2 NULL,
                "VesselId" int4 NULL,
                "SpecieId" int4 NULL,
                "BasePortCode" int4 NULL,
                "BasePortName" varchar(50) NULL,
                "BasePortId" int2 NULL,
                "MetierCAT" varchar(30) NULL,
                "MetierDCF" varchar(10) NULL,
                "TrackCode" varchar NULL,
                CONSTRAINT vcpe_auto_download_pkey PRIMARY KEY ("Id")
                -- CONSTRAINT "fk_BasePortId" FOREIGN KEY ("BasePortId") REFERENCES public.port_all("Id"),
                -- CONSTRAINT "fk_PortId" FOREIGN KEY ("PortId") REFERENCES public.port("Id")
            );

            -- 2. Funció del Trigger
            CREATE OR REPLACE FUNCTION parse_and_insert_sales_notes()
            RETURNS TRIGGER AS $$
            DECLARE
                estab_element jsonb;
                venta_element jsonb;
                especie_element jsonb;

                -- Variables per dades
                v_num_envio text;
                v_est_id text;
                v_est_name text;

                v_buque_code text;
                v_owner_code text;
                v_puerto_al5 text;

                v_num_doc text;
                v_fecha_venta timestamp;
                v_especie_code text;
                v_kg numeric;
                v_eur numeric;
                v_track_code text;

                -- Variables per nous camps JSON
                v_doc_type text;
                v_lote text;
                v_talla text;
                v_calibre text;
                v_frescura text;
                v_presentacion text;
                v_conservacion text;
                v_vessel_type text;

                -- Variables per IDs (Lookups)
                v_port_id int;
                v_vessel_id int;
                v_specie_id int;

                -- Variables per Noms (Lookups)
                v_vessel_name text;
                v_port_name_real text;
                v_specie_name text;

                -- Variables per dades extra del vaixell
                v_base_port_id int;
                v_base_port_name text;
                v_base_port_code int;
                v_fishing_art_code text;
                v_other_fishing_arts text;
                v_fishing_art_name text;
            BEGIN
                v_num_envio := NEW.raw_data ->> 'NumEnvio';
                RAISE WARNING '[DEBUG] Iniciant parseig enviament: %', v_num_envio;

                -- Validar que hi ha establiments
                IF NEW.raw_data -> 'EstablecimientosVenta' -> 'EstablecimientoVenta' IS NOT NULL THEN

                    -- Bucle sobre Establiments
                    FOR estab_element IN SELECT * FROM jsonb_array_elements(
                        CASE jsonb_typeof(NEW.raw_data -> 'EstablecimientosVenta' -> 'EstablecimientoVenta')
                            WHEN 'array' THEN NEW.raw_data -> 'EstablecimientosVenta' -> 'EstablecimientoVenta'
                            ELSE jsonb_build_array(NEW.raw_data -> 'EstablecimientosVenta' -> 'EstablecimientoVenta')
                        END
                    )
                    LOOP
                        v_est_id := estab_element ->> 'NumIdentificacionEstablec';
                        v_est_name := estab_element ->> 'NombreEstablecimiento';

                        -- Bucle sobre Vendes
                        IF estab_element -> 'Ventas' -> 'VentasUnidadProductiva' IS NOT NULL THEN
                            FOR venta_element IN SELECT * FROM jsonb_array_elements(
                                CASE jsonb_typeof(estab_element -> 'Ventas' -> 'VentasUnidadProductiva')
                                    WHEN 'array' THEN estab_element -> 'Ventas' -> 'VentasUnidadProductiva'
                                    ELSE jsonb_build_array(estab_element -> 'Ventas' -> 'VentasUnidadProductiva')
                                END
                            )
                            LOOP
                                v_buque_code := venta_element -> 'DatosUnidadProductiva' ->> 'CodigoBuque';
                                -- Acceptar NIFPersona si CodigoBuque és NULL (Polimorfisme)
                                IF v_buque_code IS NULL THEN
                                    v_buque_code := venta_element -> 'DatosUnidadProductiva' ->> 'NIFPersona';
                                END IF;

                                v_puerto_al5 := venta_element -> 'DatosUnidadProductiva' ->> 'PuertoAL5';
                                -- Acceptar LugarDescarga si PuertoAL5 és NULL
                                IF v_puerto_al5 IS NULL THEN
                                    v_puerto_al5 := venta_element -> 'DatosUnidadProductiva' ->> 'LugarDescarga';
                                END IF;

                                v_owner_code := venta_element -> 'DatosUnidadProductiva' ->> 'CodigoArmador';

                                -- ---------------------------------------------------------
                                -- ZONA DE LOOKUPS (Traducció Codis -> IDs)
                                -- ---------------------------------------------------------

                                -- Lookup Port: Usem port.Name creuant amb NombreEstablecimiento (Peticio usuari)
                                SELECT "Id", "Name" INTO v_port_id, v_port_name_real
                                FROM public.port
                                WHERE "Name" = v_est_name LIMIT 1;

                                IF v_port_id IS NULL THEN
                                    RAISE WARNING '[DEBUG] Port no trobat per nom: "%"', v_est_name;
                                END IF;

                                -- Reset variables opcionals
                                v_base_port_name := NULL;

                                -- Lookup Vessel: Usem Code de la taula vessel (verificat amb esquema)
                                -- Recuperem BasePortCode per buscar el nom a port_all després
                                -- INTENT 1: Coincidència per Codi i Data (Històric)
                                SELECT "Id", "Name", "BasePortId", "BasePortCode",
                                "GearMainCode", "GearSecCode"
                                INTO v_vessel_id, v_vessel_name, v_base_port_id,
                                     v_base_port_code,
                                     v_fishing_art_code, v_other_fishing_arts
                                FROM public.vessel
                                WHERE "Code" = v_buque_code
                                  AND v_fecha_venta::date >= "EventStartDate"
                                  AND v_fecha_venta::date <= "EventEndDate"
                                LIMIT 1;

                                -- INTENT 2: Fallback només per Codi
                                IF v_vessel_id IS NULL THEN
                                    SELECT "Id", "Name", "BasePortId", "BasePortCode",
                                    "GearMainCode", "GearSecCode"
                                    INTO v_vessel_id, v_vessel_name, v_base_port_id,
                                         v_base_port_code,
                                         v_fishing_art_code, v_other_fishing_arts
                                    FROM public.vessel
                                    WHERE "Code" = v_buque_code
                                    ORDER BY "EventEndDate" DESC
                                    LIMIT 1;
                                END IF;

                                IF v_vessel_id IS NULL THEN
                                    RAISE WARNING '[DEBUG] Vaixell no trobat. Code rebut: "%"', v_buque_code;
                                END IF;

                                -- Lookup Base Port Name: Creuant port_all.Code amb vessel.BasePortCode
                                IF v_base_port_code IS NOT NULL THEN
                                    SELECT "Name" INTO v_base_port_name
                                    FROM public.port_all
                                    WHERE "Code" = v_base_port_code;
                                END IF;

                                -- Lookup Gear Name (Art de Pesca)
                                SELECT "CatalanName" INTO v_fishing_art_name
                                FROM public.gear
                                WHERE "Code" = v_fishing_art_code LIMIT 1;

                                -- VesselType Logic
                                IF v_buque_code LIKE 'ESP%' OR v_buque_code LIKE 'BOC%' THEN
                                    v_vessel_type := 'VAIXELL';
                                ELSE
                                    v_vessel_type := 'PERSONA FÍSICA / JURÍDICA';
                                END IF;

                                v_specie_id := NULL;

                                -- Bucle sobre Espècies
                                IF venta_element -> 'Especies' -> 'Especie' IS NOT NULL THEN
                                    FOR especie_element IN SELECT * FROM jsonb_array_elements(
                                        CASE jsonb_typeof(venta_element -> 'Especies' -> 'Especie')
                                            WHEN 'array' THEN venta_element -> 'Especies' -> 'Especie'
                                            ELSE jsonb_build_array(venta_element -> 'Especies' -> 'Especie')
                                        END
                                    )
                                    LOOP
                                        v_num_doc := especie_element ->> 'NumDocVenta';
                                        v_fecha_venta := (especie_element ->> 'FechaVenta')::timestamp;
                                        v_doc_type := especie_element ->> 'TipoDocumento';
                                        v_especie_code := especie_element ->> 'EspecieAL3';
                                        v_kg := (especie_element ->> 'Cantidad')::numeric;
                                        v_eur := (especie_element ->> 'Precio')::numeric;

                                        -- Nous camps detallats
                                        v_lote := especie_element ->> 'Lote';
                                        v_talla := especie_element ->> 'Talla';
                                        v_calibre := especie_element ->> 'Calibre';
                                        v_frescura := especie_element ->> 'Frescura';
                                        v_presentacion := especie_element ->> 'Presentacion';
                                        v_conservacion := especie_element ->> 'Conservacion';

                                        -- Generar TrackCode: VesselCode + _ + YYYY-MM-DD
                                        v_track_code := v_buque_code || '_' || to_char(v_fecha_venta, 'YYYY-MM-DD');

                                        -- Lookup Especie: Usem 3A_Code de la taula species (verificat amb esquema)
                                        SELECT "Id", "CatalanName"
                                        INTO v_specie_id, v_specie_name
                                        FROM public.species
                                        WHERE "3A_Code" = v_especie_code LIMIT 1;

                                        IF v_specie_id IS NULL THEN
                                            -- Fallback: Intentem amb GeneralitatCode (com feia l'importació legacy)
                                            SELECT "Id", "CatalanName"
                                            INTO v_specie_id, v_specie_name
                                            FROM public.species
                                            WHERE "GeneralitatCode" = v_specie_code LIMIT 1;
                                        END IF;

                                        IF v_specie_id IS NULL THEN
                                            RAISE WARNING '[DEBUG] Especie no trobada. Code rebut: "%"',
                                            v_especie_code;
                                        END IF;

                                        -- INSERT a la taula plana
                                        INSERT INTO public.vcpe_auto_download (
                                            "VesselCode",
                                            "VesselName",
                                            "VesselType",
                                            "VesselOwnerCode",
                                            "SaleNumber",
                                            "DocType",
                                            "Lot",
                                            "Size",
                                            "Calibre",
                                            "Freshness",
                                            "Presentation",
                                            "Conservation",
                                            "SpecieCode",
                                            "SpecieName",
                                            "PortName",
                                            "Date",
                                            "FishingArtCode",
                                            "FishingArtName",
                                            "OtherFishingArts",
                                            "Weight",
                                            "Amount",
                                            "PortId",
                                            "VesselId",
                                            "SpecieId",
                                            "TrackCode",
                                            "BasePortId",
                                            "BasePortName",
                                            "BasePortCode"
                                        ) VALUES (
                                            v_buque_code,
                                            v_vessel_name,
                                            v_vessel_type,
                                            v_owner_code,
                                            v_num_doc,
                                            v_doc_type,
                                            v_lote,
                                            v_calibre,
                                            v_talla,
                                            v_frescura,
                                            v_presentacion,
                                            v_conservacion,
                                            v_especie_code,
                                            v_specie_name,
                                            -- Usem nom oficial, fallback a establiment
                                            COALESCE(v_port_name_real, v_est_name),
                                            v_fecha_venta::date,
                                            v_fishing_art_code,
                                            v_fishing_art_name,
                                            v_other_fishing_arts,
                                            v_kg,
                                            v_eur,
                                            v_port_id,
                                            v_vessel_id,
                                            v_specie_id,
                                            v_track_code,
                                            v_base_port_id,
                                            v_base_port_name,
                                            v_base_port_code
                                        );
                                    END LOOP;
                                END IF;
                            END LOOP;
                        END IF;
                    END LOOP;
                END IF;

                -- Actualitzar l'estat de l'enviament pare a 'procesado_en_db = True'
                UPDATE public.envio_staging
                SET procesado_en_db = true
                WHERE id = NEW.envio_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- 3. Associar Trigger a la taula raw_sales_note
            DROP TRIGGER IF EXISTS trigger_parse_sales_notes ON raw_sales_note;

            CREATE TRIGGER trigger_parse_sales_notes
            AFTER INSERT ON raw_sales_note
            FOR EACH ROW
            EXECUTE FUNCTION parse_and_insert_sales_notes();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_parse_sales_notes ON raw_sales_note;
            DROP FUNCTION IF EXISTS parse_and_insert_sales_notes;
            DROP TABLE IF EXISTS public.vcpe_auto_download;
            """,
        )
    ]
