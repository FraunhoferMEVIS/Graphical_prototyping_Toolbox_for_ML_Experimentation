#! /bin/bash

export REGISTRY=registry.your-registry
export TAG=1.0
docker tag project-manager:latest ${REGISTRY}/project-manager:${TAG}
docker tag workflow-frontend:latest ${REGISTRY}/workflow-frontend:${TAG}
docker tag mlkitchen-backend:latest ${REGISTRY}/mlkitchen-backend:${TAG}
docker tag mlflow_tracking_server:latest ${REGISTRY}/mlflow-tracking:${TAG}
docker tag mlflow_runner:latest ${REGISTRY}/mlflow_runner:${TAG}
docker tag data-ingest:latest ${REGISTRY}/mimic-data-ingest:${TAG}
docker tag data-descriptor:latest ${REGISTRY}/mimic-data-descriptor:${TAG}
docker tag mlkitchen-frontend:latest ${REGISTRY}/mlkitchen-frontend:${TAG}
docker tag data-preparation:latest ${REGISTRY}/data-preparation:${TAG}
docker tag data-preparation-frontend:latest ${REGISTRY}/data-preparation-frontend:${TAG}
docker push ${REGISTRY}/project-manager:${TAG}
docker push ${REGISTRY}/workflow-frontend:${TAG}
docker push ${REGISTRY}/mlkitchen-backend:${TAG}
docker push ${REGISTRY}/mlflow-tracking:${TAG}
docker push ${REGISTRY}/mlflow_runner:${TAG}
docker push ${REGISTRY}/mimic-data-ingest:${TAG}
docker push ${REGISTRY}/mimic-data-descriptor:${TAG}
docker push ${REGISTRY}/mlkitchen-frontend:${TAG}
docker push ${REGISTRY}/data-preparation:${TAG}
docker push ${REGISTRY}/data-preparation-frontend:${TAG}