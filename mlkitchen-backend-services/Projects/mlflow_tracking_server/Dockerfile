FROM python:3.11-slim

WORKDIR /code
RUN useradd -u 65532 -g 100 -ms /bin/bash nonroot
RUN chown -R 65532:100 /code

RUN pip install --no-cache-dir --upgrade mlflow==2.16.* psycopg2_binary==2.9.*

EXPOSE 5000

USER 65532

CMD mlflow ui --port 5000 --backend-store-uri postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${MLFLOW_POSTGRES_SERVICE_HOST}:${MLFLOW_POSTGRES_SERVICE_PORT}/${POSTGRES_DB} --host ${MLFLOW_HOST} --default-artifact-root /gaia/artifacts