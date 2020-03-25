#!/bin/bash


# redis
microk8s.kubectl create -f ../deployments/redis-deployment.yml
microk8s.kubectl create -f ../services/redis-service.yml

# web-server
microk8s.kubectl create -f ../deployments/web-server-deployment.yml
microk8s.kubectl create -f ../services/web-server-service.yml

# server
microk8s.kubectl create -f ../deployments/server-deployment.yml
microk8s.kubectl create -f ../services/server-service.yml

# client
microk8s.kubectl create -f ../deployments/client-deployment.yml

