# Workflow Frontend

This repository contains the code for the workflow page.


## Frontend Development

Code and README is located in `workflow-page` folder.


## Updating the project-manager client

npm install @openapitools/openapi-generator-cli
cd ./workflow-page/src/app/api
openapi-generator-cli generate -i ./project-manager-openapi.json -o project-manager -g typescript-angular --skip-validate-spec --additional-properties=ngVersion=16.2.12