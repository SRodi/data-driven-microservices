#!/bin/sh

# web-server
microk8s.kubectl delete -f ../deployments/web-server-deployment.yml
microk8s.kubectl delete -f ../services/web-server-service.yml

# client
microk8s.kubectl delete -f ../deployments/client-deployment.yml

# server
microk8s.kubectl delete -f ../deployments/server-deployment.yml
microk8s.kubectl delete -f ../services/server-service.yml

# reddit-server
microk8s.kubectl delete -f ../deployments/reddit-server-deployment.yml
microk8s.kubectl delete -f ../services/reddit-server-service.yml

#redis
microk8s.kubectl delete -f ../deployments/redis-deployment.yml
microk8s.kubectl delete -f ../services/redis-service.yml