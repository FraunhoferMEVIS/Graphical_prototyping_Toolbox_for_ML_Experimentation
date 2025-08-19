FROM node:18.18-alpine AS build

ARG ENV
ARG BASE_PATH

RUN apk add --no-cache \
    gettext \
    libintl \
    sed

WORKDIR /code
COPY package.json package.json
RUN npm i --loglevel=verbose --prefer-offline --no-audit --progress=false
COPY . .

RUN npm run build -- --configuration ${ENV} --base-href ${BASE_PATH} --deploy-url ${BASE_PATH} --output-hashing=all

### 2nd stage
FROM nginxinc/nginx-unprivileged:1.27-alpine

LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.title="mlkitchen"
LABEL org.opencontainers.image.description="KI-FDZ mlkitchen"
LABEL org.opencontainers.image.vendor="Fraunhofer MEVIS"

## Copy webapp into nginx serve folder
USER root
COPY --from=build /code/dist/mlkitchen /usr/share/nginx/html
RUN chown -R 101:101 /usr/share/nginx/html/assets
USER 101
COPY --from=build /code/package-lock.json /etc/package-lock.json

## Copy nginx config into container
COPY nginx.conf /etc/nginx/nginx.conf

# When the container starts, replace the env.js with values from environment variables
CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js && exec nginx -g 'daemon off;'"]
