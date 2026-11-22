-- Rulat o singură dată pe instanța locală Cursora, conectat ca postgres.
-- Instanța folosește autentificare trust numai pe localhost și portul 5433.
CREATE ROLE cursora_user WITH LOGIN;

CREATE DATABASE cursora_db
    WITH OWNER = cursora_user
    ENCODING = 'UTF8';

GRANT ALL PRIVILEGES ON DATABASE cursora_db TO cursora_user;
