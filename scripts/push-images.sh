#!/usr/bin/env bash

cd ../server
docker build -f server.Dockerfile -t=srodi/stream-server .
cd ../server-reddit
docker build -f server_reddit.Dockerfile -t=srodi/reddit-stream-server .
cd ../client
docker build -f client.Dockerfile -t=srodi/stream-client .
cd ../web_server
docker build -f web_server.Dockerfile -t=srodi/web-server .

docker push srodi/stream-server
docker push srodi/reddit-stream-server
docker push srodi/stream-client
docker push srodi/web-server