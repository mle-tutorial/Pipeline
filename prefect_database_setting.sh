#!/bin/bash

docker exec -it postgresql \
psql -U postgres \
-c "CREATE DATABASE prefect"

prefect config unset PREFECT_API_DATABASE_CONNECTION_URL
prefect config unset PREFECT_API_URL
prefect config unset PREFECT_API_KEY
prefect config set PREFECT_ORION_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/prefect"
# Deprecated. Use PREFECT_API_DATABASE_CONNECTION_URL instead.