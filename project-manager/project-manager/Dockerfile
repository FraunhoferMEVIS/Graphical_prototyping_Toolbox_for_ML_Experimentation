FROM python:3.11.9 as requirements-stage
WORKDIR /code
ENV ROOT_PATH ""

# configure non-root user
RUN useradd -u 1001 -g 100 -ms /bin/bash sandbox
RUN chown -R 1001:100 /code

# install python requirements
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# copy source code
COPY ./service /code/service
WORKDIR /code/service

USER 1001
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]