FROM python:3.11.9 as requirements-stage

WORKDIR /code

RUN useradd -u 1001 -g 100 -ms /bin/bash sandbox
RUN chown -R 1001:100 /code

RUN apt-get update && apt-get install -y zip jq 
# libpq-dev

COPY ./requirements /code/requirements
RUN pip install -r /code/requirements/requirements_core.txt

COPY ./data_preparation /code/data_preparation
COPY ./tests /code/tests
COPY ./configuration /code/configuration
COPY main.py /code/main.py

EXPOSE ${DATA_PREPROCESSING_PORT}

USER 1001
CMD python main.py
