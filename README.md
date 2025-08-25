# Graphical prototyping Toolbox for ML Experimentation

The Graphical Prototyping Toolbox for ML Experimentation is a toolbox to design, prepare and implement Machine Learning (ML) experiments for tabular health data, which was developed within the KI-FDZ project. 
It is a composition of web applications which can be accessed from a central workflow page. It contains components for data preparation (maratus), experiment setup (mlkitchen), and algorithm tracking (tracking server, which comes with base library mlflow). 

The user creates a project and then follows the steps mentioned on the workflow page. Intermediate results are shared between the components, based on included import and export functionality. The user can perform various data preprocessing steps (load from file, filter, transform, create new features, etc.) to prepare one or multiple input tables and merge it into one table for proceeding ML analysis. The user can select ML algorithms from the visual interface of mlkitchen and start the experiments including hyperparameter search for some of the parameters. Resulting metrics as well as the parameterization of successfully passed experiments are stored and can be investigated on the tracking server. 

The software is provided on "AS IS" basis, i.e. it comes without any warranty, express or implied including (without limitations) any warranty of merchantability and warranty of fitness for a particular purpose.

Due to the completion of the project, we are not pursuing extensions or adaptations. If you are interested in a joint project or collaboration, we look forward to hearing from you. Please contact doerte.corr@mevis.fraunhofer.de

This work was funded based on a resolution of the German parliament by the German Federal Ministry of Health (BMG, Project KI-FDZ, Funding Code: 2521DAT01B)

# Kubernetes Setup

This document describes how to set up our "Graphical prototyping Toolbox for Machine Learning Experimentation" on a Kubernetes cluster. Please note that in some places the helm chart and code might refer to it as "AI-Sandbox", which was its internal project name.

### Requirements

1. 2 Ubuntu 2204 VMs (each 8 CPU cores, 32GB RAM and 200GB SSD)
2. Docker registry
3. A way to route traffic (DNS entry or reverse proxy) to one of the VMs (the control plane)
4. TLS certificate for the host domain

### Docker Images

There are 10 Docker images needed to run this project. This is how you build, tag and change them. 

1. Build docker images from source by running ./build_docker.sh from this folder
2. Edit push_docker.sh and set REGISTRY to your docker registry (make sure you are logged into it and the current user has access to the docker deamon)
3. In the later step "Helm Chart" make sure that the image names and tags inside the values.yaml matches

### RKE2 Cluster

For our deployments a RKE2 Cluster with enabled CIS profile was used. Theoretically most Kubernetes distributions should work, as long as you can install an nginx ingress controller and longhorn. For this manual we tried to simplify the process to only include the minimal amount of steps to get a working RKE2 cluster. One of the Ubuntu VMs will become a control plane node and will run most of our containers. It is important that the DNS entry of the future toolbox url points to it's ip and that you have tls certificates for that address. The second VM will become a worker node. mlkitchen will use it to schedule containers on demand.

### Control Plane Setup

Before starting you need to generate a 32 Byte token, that will be used by the worker to join the cluster. Here is an example how you could do this.

```bash
openssl rand -base64 32 | tr -- '+/' '-_'
```

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
curl -sfL https://get.rke2.io | sudo INSTALL_RKE2_VERSION=v1.31.2+rke2r1 INSTALL_RKE2_TYPE='server' sh -
sudo apt-get install nfs-common -y
# insert token in next line
sudo sh -c 'echo agent-token: {{ token }} >> /etc/rancher/rke2/config.yaml'
# insert control plane url in next line
sudo sh -c 'echo tls-san: https://{{ cp_url }} >> /etc/rancher/rke2/config.yaml'
sudo systemctl enable rke2-server.service
sudo systemctl start rke2-server.service
sudo cp /var/lib/rancher/rke2/bin/kubectl /usr/local/bin/kubectl
sudo mkdir -p /root/.kube
sudo cp /etc/rancher/rke2/rke2.yaml /root/.kube/config

# install longhorn
sudo helm repo add longhorn https://charts.longhorn.io
sudo helm repo update
sudo helm install longhorn longhorn/longhorn --namespace longhorn-system --create-namespace --version 1.7.0
```

### Worker Node Setup

```bash
curl -sfL https://get.rke2.io | sudo INSTALL_RKE2_VERSION=v1.31.2+rke2r1 INSTALL_RKE2_TYPE='agent' sh -
sudo apt-get install nfs-common -y
# insert control plane url in next line
sudo sh -c 'echo server: https://{{ cp_url }}:9345 >> /etc/rancher/rke2/config.yaml'
# insert token in next line
sudo sh -c 'echo token: {{ token }} >> /etc/rancher/rke2/config.yaml'
sudo systemctl enable rke2-agent.service
sudo systemctl start rke2-agent.service
```

### Checking Cluster Status

To check if everything is running use "sudo kubectl get nodes" on the control plane VM and make sure that both nodes are showing up as ready. Everything beyond that requires more in depth kubernetes knowledge.

# Helm Chart

The following steps can either be executed on the control plane VM or on a separate machine, as long as kubectl + helm have been installed and configured to use the cluster's kubeconfig file.

### Build Helm Chart

In the helm-chart folder run:

- helm dependency update ./ai-sandbox/charts/mlkitchen
- helm dependency update ./ai-sandbox/charts/data-descriptor
- helm dependency update ./ai-sandbox/charts/data-provider
- helm dependency update ./ai-sandbox/charts/data-preparation
- helm dependency update ./ai-sandbox/charts/project-manager
- helm dependency update ./ai-sandbox/charts/workflow-page
- helm dependency update ./ai-sandbox/charts/mlflow-tracking
- helm package ./ai-sandbox
- (optional) helm registry login ...
- (optional) helm push ...


### values.yaml

The helm chart only requires a values.yaml file as an input. 
1. <<your_domain>>: the url under which your control plane can be reached e.g. "ai-sandbox.intern.mevis.fraunhofer.de"
2. <<your_registry>>: the address of the docker registry. 

### Apply Helm Chart

```bash
sudo kubectl create namespace ai-sandbox --dry-run=client -o yaml | sudo kubectl apply -f -
# insert path to tls cert files in next line
sudo kubectl create secret tls ai-sandbox-cert-tls --key {{ tls_cert_key }}.key --cert {{ tls_cert_crt}}.crt --namespace ai-sandbox --dry-run=client -o yaml | sudo kubectl apply -f -
// insert values to connect to docker registry in next line
sudo kubectl create secret docker-registry harborcred --docker-server={{ registry_url }} --docker-username='{{ registry_user }}' --docker-password={{ registry_user_pw }} -n ai-sandbox --dry-run=client -o yaml | sudo kubectl apply -f -
sudo helm upgrade -i ai-sandbox ./ai-sandbox-1.1.13.tgz --values ./fdz-values.yaml --namespace ai-sandbox
sudo kubectl get pods -n ai-sandbox
```

### Upload data

It is important to note that the opensource variant of this tool is distributet without any preinstalled data sets. To try it out you need take a csv file of your choice and upload it to the shared longhorn storage of our containers. The "kubectl cp" command can be used to place a folder containing the new csv tables into "/gaia/csv_datasets/" of the data-preparation-api container. Make sure that the csv files have their own subfolder and are not placed directly into "csv_datasets". After placing the csv file, restart the data-preparation-api container and delete any csv import module in Maratus.

# Component Sources

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/ai-sandbox-helm-chart
Manifests: ai-sandbox-helm-chart

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/workflow-frontend
Container: workflow-page

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/project-manager
Container: project-manager

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/mlkitchen-frontend
Container: mlkitchen-frontend

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/mlkitchen-backend-services
Container: mlkitchen-backend, mlflow-runner, mlflow-tracking, data-descriptor, data-ingest

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/data-preparation-frontend
Container: data-preparation-frontend (aka Maratus)

https://github.com/FraunhoferMEVIS/Graphical_prototyping_Toolbox_for_ML_Experimentation/data-preparation
Container: data-preparation-backend

### mlreport

There is a "hidden" prototype called "mlreport", that wasn't developed further. It can be found on the workflow page under the url ".../assets/report/report.html".

# Non MEVIS open-source Containers

https://hub.docker.com/_/postgres
Container: postgres:16.2

# Debugging

### Container

For debugging containers a combination of "kubectl get pods -n ai-sandbox" and "kubectl get logs ..." can be used. Please note that many containers don't include a shell.

### Storage

To manually manipulate the longhorn volumes used to store data, the mlflow-tracking-server container should preferably be used as an entry point, since all other backend services don't contain a shell. Use either the command line or a kubernetes GUI tool of your choice to open a shell in the container and then navigate to the folder "/gaia/". The gaia folder contains the csv data in "/gaia/csv_datasets/" and also contains a "projects" subfolder where toolbox components store the state of each project. To debug a specific project check there. 

### Known Bugs

- Maratus: Using an invalid operator in a module causes internal server error
- Maratus: Update issues with modules Aggregate and Transform
