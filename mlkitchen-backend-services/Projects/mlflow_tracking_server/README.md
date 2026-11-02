# mlflow version

2.16.*

# Commands to start tracking server locally:

```bash
mlflow ui --backend-store-uri "postgresql://postgres:only_for_kifdz_project!@10.142.3.101:26415/mlflowdb" --host 127.0.0.1 --default-artifact-root "/code/base_folder/metadata/mlflow/mlartifacts"
```

# Commands to build, tag and push tracking server:

Build image locally

```bash
docker build -t fdz-mlflow-tracking .
```

Tag image

```bash
docker tag fdz-mlflow-tracking:latest <your-registry>/ki-fdz/fdz-mlflow-tracking:20221124
```

Push image to  registry

```bash
docker push <your-registry>/ki-fdz/fdz-mlflow-tracking:20221124
```
