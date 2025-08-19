# To be able to include the "methods_repository" in this docker, it needs to be built out of its own context.
# To build this docker image, please run 
# "docker build -t ki-fdz/fdz_mlflow_runner/fdz_mlflow_runner:latest -f ./build_experiment_runner/Dockerfile ."
# from the folder containing this folder.
FROM python:3.11-slim

WORKDIR /code
RUN useradd -u 65532 -g 100 -ms /bin/bash nonroot
RUN chown -R 65532:100 /code

EXPOSE 8888

RUN apt-get update && \
    apt-get  upgrade -y && \
    apt-get install -y build-essential \
                       git

COPY requirements /code/requirements
RUN pip install --no-cache-dir --upgrade -r requirements/requirements_core.txt && pip install --no-cache-dir --upgrade -r requirements/requirements_ml.txt

COPY ./methods_repository /code/methods_repository

USER 65532

ENV PYTHONPATH="${PYTHONPATH}:/code"

CMD ["/bin/sh", "-c" , "cd ${RECIPE} &&  echo ${PWD} && sh ./run_experiment.sh"]