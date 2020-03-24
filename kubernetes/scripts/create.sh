#!/bin/bash

# server
microk8s.kubectl create -f server-deployment.yml
microk8s.kubectl create -f server-service.yml

# redis
microk8s.kubectl create -f redis-deployment.yml
microk8s.kubectl create -f redis-service.yml

# web-server
microk8s.kubectl create -f web-server-deployment.yml
microk8s.kubectl create -f web-server-service.yml

# client
microk8s.kubectl create -f client-deployment.yml

