---
layout: post
title: Google Cloud Resource Management
categories: [blog]
tags: [cloud, gcp]
---

Taking steps to learn more about GCP (Google Cloud Platform) services and thinking about what I can do with it. Here are some notes. It's mostly based on [Qwiklab](https://google.qwiklabs.com) challenges.  

Github repo 👉: [gcp-cloud-resources-mgt](https://github.com/maryletteroa/gcp-cloud-resources-mgt)


### Set zone / region, project
```sh
gclud auth list
gcloud projects list
gcloud config set compute/zone us-east1-b
gcloud config set compute/region us-east1
gcloud config set project my-project
```

### Create a virtual machine instance
```sh
gcloud compute instances create nucleus-jumphost --machine-type f1-micro
```

### Kubernetes

#### Create a kubernetes cluster
```sh
gcloud container clusters create my-cluster
gcloud container clusters get-credentials my-cluster
```
#### Deploy an image
```sh
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:2.0
```
#### Expose the app on port 8080 
```sh
kubectl expose deployment hello-server --type=LoadBalancer --port 8080
watch -n 1 kubectl get service ## check until an external ip has been assigned
```
#### HTTP load balancer

And a bit nuanced but here's how to set up an HTTP load balancer (e.g. on instances running nginx web server)

### Create startup script
```sh
cat << EOF > startup.sh
#! /bin/bash
apt-get update
apt-get install -y nginx
service nginx start
sed -i -- 's/nginx/Google Cloud Platform - '"\$HOSTNAME"'/' \
	/var/www/html/index.nginx-debian.html
EOF
```
### Create an instance template
```sh
gcloud compute instance-templates create nginx-template \
	--metadata-from-file startup-script=startup.sh
```

### Create a target pool
```sh
gcloud compute target-pools create nginx-pool
```

### Create managed instance group
```sh
gcloud compute instance-groups managed create nginx-group \
	--base-instance-name nginx \
	--size 2 \
	--template nginx-template \
	--target-pool nginx-pool
gcloud compute instances list
```
### Create firewall rule to allow traffic (80/tcp)
```sh
gcloud compute firewall-rules create www-firewall \
	--allow tcp:80
gcloud compute forwarding-rules create nginx-lb \
	--ports=80 \
	--target-pool nginx-pool
gcloud compute forwarding-rules list
```
### Create a health check
```sh
gcloud compute http-health-checks create http-basic-check
gcloud compute instance-groups managed set-named-ports nginx-group \
	--named-ports http:80
```
### Create a backend service, and attach the managed instance group
```sh
gcloud compute backend-services create nginx-backend \
	--protocol HTTP \
	--http-health-checks http-basic-check \
	--global
gcloud compute backend-services add-backend nginx-backend \
	--instance-group nginx-group \
	--global
```
### Create a URL map, and target the HTTP proxy to route requests to your URL map
```sh
gcloud compute url-maps create web-map \
	--default-service nginx-backend
gcloud compute target-http-proxies create http-lb-proxy \
	--url-map web-map
```
### Create a forwarding rule
```sh
gcloud compute forwarding-rules create http-content-rule \
	--global \
	--target-http-proxy http-lb-proxy \
	--ports 80
gcloud compute forwarding-rules list
```

