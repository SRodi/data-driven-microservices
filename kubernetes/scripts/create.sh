#!/bin/bash


# redis deployment
microk8s.kubectl create -f ../deployments/redis-deployment.yml
# wait till redis is running
while [[ $(microk8s.kubectl get pods -l app=redis -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
# redis service
microk8s.kubectl create -f ../services/redis-service.yml

# web-server deployment
microk8s.kubectl create -f ../deployments/web-server-deployment.yml
# wait till web-server is running
while [[ $(microk8s.kubectl get pods -l app=web-server -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
# web-server service
microk8s.kubectl create -f ../services/web-server-service.yml

# server deployment
microk8s.kubectl create -f ../deployments/server-deployment.yml
# wait till server is running
while [[ $(microk8s.kubectl get pods -l app=tweet-stream-server -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
# server service
microk8s.kubectl create -f ../services/server-service.yml

# reddit-server deployment
microk8s.kubectl create -f ../deployments/reddit-server-deployment.yml
# wait till reddit-server is running
while [[ $(microk8s.kubectl get pods -l app=reddit-stream-server -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
# reddit-server service
microk8s.kubectl create -f ../services/reddit-server-service.yml

# client deployment
microk8s.kubectl create -f ../deployments/client-deployment.yml

