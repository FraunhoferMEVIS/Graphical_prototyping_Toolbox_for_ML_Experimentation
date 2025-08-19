#! /bin/bash

export PROJECT_FOLDER=$(pwd)
cd ${PROJECT_FOLDER}/project-manager/project-manager
docker build -t project-manager -f DockerfileProd .
cd ${PROJECT_FOLDER}/workflow-frontend/workflow-page
docker build -t workflow-frontend --build-arg ENV=production --build-arg BASE_PATH=/ -f Dockerfile .
cd ${PROJECT_FOLDER}/mlkitchen-backend-services/Projects/Pipeline
docker build -t mlkitchen-backend -f DockerfileProd .
docker build -t mlflow_tracking_server -f ../mlflow_tracking_server/Dockerfile .
docker build -t mlflow_runner -f ./build_experiment_runner/Dockerfile .
cp -r ./methods_repository ${PROJECT_FOLDER}/mlkitchen-backend-services/Projects/DataIngest
cd ${PROJECT_FOLDER}/mlkitchen-backend-services/Projects/DataIngest
docker build -t data-ingest -f DockerfileProd .
cd ${PROJECT_FOLDER}/mlkitchen-backend-services/Projects/DataDescriptor
docker build -t data-descriptor -f DockerfileProd .
cd ${PROJECT_FOLDER}/mlkitchen-frontend/mlkitchen
docker build -t mlkitchen-frontend --build-arg ENV=production --build-arg BASE_PATH=/mlkitchen/ -f Dockerfile .
cd ${PROJECT_FOLDER}/data-preparation
docker build -t data-preparation -f DockerfileProd .
cd ${PROJECT_FOLDER}/data-preparation-frontend/data-preparation
docker build -t data-preparation-frontend --build-arg ENV=production --build-arg BASE_PATH=/data-preparation/ -f Dockerfile .
cd ${PROJECT_FOLDER}/ai-sandbox-helm-chart
