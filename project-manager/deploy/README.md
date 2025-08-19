## Commands to build, tag and push ladning page:

docker build -t fdz-landing-page ../landing-page

docker tag fdz-landing-page:latest <your-registry>/ki-fdz/fdz-landing-page:20230317

docker push <your-registry>/ki-fdz/fdz-landing-page:20230317

## Commands to build, tag and push project manager for k8s:

docker build -t fdz-project-manager -f DockerfileProd ../project-manager

docker tag fdz-project-manager:latest <your-registry>/ki-fdz/fdz-project-manager:20241121_prod

docker push <your-registry>/ki-fdz/fdz-project-manager:20241121_prod

## run project manager locally

cd service
uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8080

open:
http://localhost:8080/docs

## Generating new backend client

In folder ".app/src/app/" run the command "openapi-generator-cli generate -i ./openapi.json -o project-manager -g typescript-angular"
