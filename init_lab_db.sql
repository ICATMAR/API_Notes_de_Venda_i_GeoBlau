-- init_db.sql
-- Script d'inicialització de la base de dades PostgreSQL/PostGIS
-- per l'API de notes de venda VCPE - TFM Ciberseguretat

-- Crear extensions necessàries
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Per cerca de text

-- Configuració de la base de dades
ALTER DATABASE vcpe_db SET timezone TO 'Europe/Madrid';

-- Comentaris de la base de dades
COMMENT ON DATABASE vcpe_db IS 'Base de dades per TFM Ciberseguretat - API Segura Notes de Venda ICATMAR';

-- Configurar permisos per l'usuari vcpe_user
GRANT CONNECT ON DATABASE vcpe_db TO vcpe_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO vcpe_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vcpe_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vcpe_user;

-- Permisos per taules futures (que crearà Django)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vcpe_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO vcpe_user;

-- Missatge de confirmació
DO $$
BEGIN
    RAISE NOTICE '====================================================';
    RAISE NOTICE '  ✅ Base de dades vcpe_db inicialitzada';
    RAISE NOTICE '====================================================';
    RAISE NOTICE 'Extensions: postgis, postgis_topology, uuid-ossp, pg_trgm';
    RAISE NOTICE 'Schema: public (per defecte)';
    RAISE NOTICE 'Timezone: Europe/Madrid';
    RAISE NOTICE 'Usuari: vcpe_user amb tots els permisos';
    RAISE NOTICE '====================================================';
END $$;