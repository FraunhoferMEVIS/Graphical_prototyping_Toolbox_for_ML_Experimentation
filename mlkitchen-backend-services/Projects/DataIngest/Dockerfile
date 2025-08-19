FROM python:3.11-slim

WORKDIR /code
RUN apt-get update && apt-get install -y zip jq

COPY ./requirements/requirements_core.txt  /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY methods_repository /code/methods_repository
COPY data_provider_src /code/data_provider_src
COPY configuration /code/configuration
COPY serve_data_provider.py /code/serve_data_provider.py

EXPOSE ${Data_INGEST_PORT}
CMD python serve_data_provider.py
