#!/bin/sh

# server
microk8s.kubectl delete -f ../deployments/server-deployment.yml
microk8s.kubectl delete -f ../services/server-service.yml

#redis
microk8s.kubectl delete -f ../deployments/redis-deployment.yml
microk8s.kubectl delete -f ../services/redis-service.yml

# web-server
microk8s.kubectl delete -f ../deployments/web-server-deployment.yml
microk8s.kubectl delete -f ../services/web-server-service.yml

# client
microk8s.kubectl delete -f ../deployments/client-deployment.yml