-- Script d'inicialització de la base de dades PostgreSQL/PostGIS
-- per l'API de notes de venda VCPE

-- Crear extensions necessàries
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Per cerca de text

-- Configuració de la base de dades
ALTER DATABASE vcpe_db SET timezone TO 'Europe/Madrid';

-- Comentaris de la base de dades
COMMENT ON DATABASE vcpe_db IS 'Base de dades per gestió de notes de venda del sector pesquer - ICATMAR';

-- Crear esquema per auditoria (opcional, per separar taules d'auditoria)
-- CREATE SCHEMA IF NOT EXISTS audit;

-- Configurar permisos
GRANT CONNECT ON DATABASE vcpe_db TO vcpe_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vcpe_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vcpe_user;

-- Índexs per millor rendiment en cerques de text (es crearan després amb Django)
-- Aquests són opcionals i es poden crear després

-- Missatge de confirmació
DO $$
BEGIN
    RAISE NOTICE 'Base de dades vcpe_db inicialitzada correctament';
    RAISE NOTICE 'Extensions: postgis, uuid-ossp, pg_trgm';
    RAISE NOTICE 'Timezone: Europe/Madrid';
END $$;