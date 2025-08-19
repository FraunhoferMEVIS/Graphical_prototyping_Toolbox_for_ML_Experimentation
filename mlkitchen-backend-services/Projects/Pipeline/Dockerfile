FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y curl wget zip jq

COPY ./requirements/requirements_core.txt  /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./methods_repository /code/methods_repository
COPY ./src /code/src
COPY ./configuration /code/configuration
COPY aisandbox_server.py /code/aisandbox_server.py

EXPOSE ${AISANDBOX_PORT}
CMD python aisandbox_server.py