# mlflow version

2.16.*

# Commands to build, tag and push and locally start docker image:

# ! from parent folder !

docker build -t fdz_mlflow_runner -f ./build_experiment_runner/Dockerfile .

docker tag fdz_mlflow_runner:latest <your-registry>/ki-fdz/fdz_mlflow_runner:20221129
docker tag fdz_mlflow_runner:latest <your-registry>/ki-fdz/fdz_mlflow_runner:latest

docker push <your-registry>/ki-fdz/fdz_mlflow_runner:20221129
docker push <your-registry>/ki-fdz/fdz_mlflow_runner:latest

# Run locally

docker run -it -p 8888:8888 -m 4096mb -e PROJECT_ID=test_project fdz_mlflow_runner:latest
