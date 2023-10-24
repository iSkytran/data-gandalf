#!/bin/bash
psql -U "$POSTGRES_USER" --dbname "$POSTGRES_DB" < <dump_filename>.sql