from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales_notes", "0002_create_trigger_vcpe"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Crear taula de staging per a vaixells (idèntica a vessel però sense FKs estrictes)
            CREATE TABLE IF NOT EXISTS public.vessel_auto_download (
                "Code" bpchar(12) NULL,
                "EventCode" bpchar(3) NULL,
                "EventStartDate" date NULL,
                "EventEndDate" date NULL,
                "LicenceInd" bool NULL,
                "RegistrationNum" varchar(15) NULL,
                "Name" varchar(50) NULL,
                "BasePortCode" int4 NULL,
                "BasePortName" varchar(30) NULL,
                "IRCS" varchar(10) NULL,
                "VMS" bool NULL,
                "GearMainCode" varchar(3) NULL,
                "GearSecCode" varchar(3) NULL,
                "LOA_m" numeric(10, 2) NULL,
                "LBP_m" numeric(10, 2) NULL,
                "GT" numeric(10, 2) NULL,
                "TRB" numeric(10, 2) NULL,
                "PowerMain_kW" numeric(10, 2) NULL,
                "PowerAux_kW" numeric(10, 2) NULL,
                "HullMaterial" varchar(20) NULL,
                "ServiceStartingDate" date NULL,
                "BasePortId" int2 NULL,
                "AIS" bool NULL,
                "Id" serial PRIMARY KEY
            );

            -- Índexs per optimitzar la cerca i comparació posterior
            CREATE INDEX IF NOT EXISTS idx_vessel_auto_code ON public.vessel_auto_download ("Code");
            CREATE INDEX IF NOT EXISTS idx_vessel_auto_startdate ON public.vessel_auto_download ("EventStartDate");
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS public.vessel_auto_download;
            """,
        )
    ]
