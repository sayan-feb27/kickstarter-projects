#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER "$DJANGO_DB_USER" WITH PASSWORD '$DJANGO_DB_USER_PASSWORD';
	CREATE DATABASE "$DJANGO_DB";
	GRANT ALL PRIVILEGES ON DATABASE "$DJANGO_DB" TO "$DJANGO_DB_USER";
EOSQL
