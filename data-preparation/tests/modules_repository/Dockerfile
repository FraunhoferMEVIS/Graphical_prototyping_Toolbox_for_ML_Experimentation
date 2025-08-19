FROM postgres:14.0

RUN mkdir scripts
COPY create_test_database.sql /scripts/create_test_database.sql
COPY init_db.sh /docker-entrypoint-initdb.d