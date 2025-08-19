FROM python:3.11-slim

WORKDIR /code
RUN apt-get update && apt-get install -y zip jq

COPY ./requirements/requirements_core.txt  /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /code/src
COPY ./config /code/config
COPY serve.py /code/serve.py

EXPOSE ${DATADESCRIPTOR_PORT}
CMD python serve.py