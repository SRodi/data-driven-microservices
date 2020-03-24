#!/bin/sh

# server
microk8s.kubectl delete -f server-deployment.yml
microk8s.kubectl delete -f server-service.yml

#redis
microk8s.kubectl delete -f redis-deployment.yml
microk8s.kubectl delete -f redis-service.yml

# web-server
microk8s.kubectl delete -f web-server-deployment.yml
microk8s.kubectl delete -f web-server-service.yml

# client
microk8s.kubectl delete -f client-deployment.yml