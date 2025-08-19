#!/bin/bash

cd /scripts

# step 1) create user, if needed
if [ "${POSTGRES_USER}" != "postgres" ]; then
    psql -U postgres -d postgres -c "DROP USER IF EXISTS ${POSTGRES_USER}; CREATE USER ${POSTGRES_USER} WITH PASSWORD ${POSTGRES_PASSWORD};"
fi

if [ "${POSTGRES_DB}" != "postgres" ]; then
  # drop and recreate the database
  psql -U ${POSTGRES_USER} -d postgres -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};"
  psql -U ${POSTGRES_USER} -d postgres -c "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};"
fi

psql -d ${POSTGRES_DB} --user ${POSTGRES_USER} -f create_test_database.sql
