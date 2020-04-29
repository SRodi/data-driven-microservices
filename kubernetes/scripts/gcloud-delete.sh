#!/bin/sh

# web-server
kubectl delete -f ../deployments/web-server-deployment.yml
kubectl delete -f ../services/web-server-service.yml

# client
kubectl delete -f ../deployments/client-deployment.yml

# server
kubectl delete -f ../deployments/server-deployment.yml
kubectl delete -f ../services/server-service.yml

# reddit-server
kubectl delete -f ../deployments/reddit-server-deployment.yml
kubectl delete -f ../services/reddit-server-service.yml

#redis
kubectl delete -f ../deployments/redis-deployment.yml
kubectl delete -f ../services/redis-service.yml