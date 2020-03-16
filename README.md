# srodi-gRPC streaming
gRPC example to implement data streaming and simulate real-time analytics

#### Prerequisites
* Python version 2.7 or higher
* Docker version 19.03 or higher
* Add `.csv` file with relative path `server/static/training.1600000.processed.noemoticon.csv`

File `training.1600000.processed.noemoticon.csv` can be downloaded from this [link](https://www.kaggle.com/kazanova/sentiment140/data)

#### Architecture
Docker compose will bring up 4 containers following the architecture below.

![architecture](static/architecture.png)

# Docker - Compose
This steps allow to create and run the containerized micro-services.
Following commands must be executed within `srodi-gRPC/test/` directory.

#### Build and run containers:
```bash
docker-compose up
```

#### Clean up
Stop execution and remove containers:
```bash
docker-compose stop
docker-compose rm
```
You will also have to remove docker images by running `docker images` and `docker rmi [IMAGE_ID]`

# Run locally with no Docker 
This refers to server and gRPC-stream client only

#### Clone repo and prepare environment
Initial steps
```bash
git clone https://github.com/srodi/srodi-gRPC.git
cd srodi-gRPC
pip install -r test/requirements.txt
```

View and edit `protos/test.proto` as required, `server.py` and `client.py` will have to match changes in `test.proto`

Generate interfaces (Only if you edited `protos/test.proto`) 
Generate the gRPC client and server interfaces from .proto service definition
```bash
cd server
python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/test.proto
cd ../client
python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/test.proto
```

Start Server
```bash
python -m server
```

Start Client
```bash
python -m client
```

# Docker
Below steps allow to containerize the microservices with Docker and run docker images locally.

Following commands must be executed from project root directory `srodi-gRPC/`.

#### Build images 
build server docker image
```bash
docker build -f server/server.Dockerfile -t=grcp-stream-server .
```
build client docker image
```bash
docker build -f client/client.Dockerfile -t=grcp-stream-client .
```

#### Run Containers
run server container
```bash
docker run -it --name server -p 9999:9999 grcp-stream-server
```
run client container
```bash
docker run -it --name client --network="host" grcp-stream-client
``` 

#### Clean up
remove containers
```bash
docker stop server && docker rm server client
```
remove images
```bash
docker rmi grcp-stream-server grcp-stream-client
```

#### Redis

Run the latest `bitnami/redis` image
`docker run --name redis -e ALLOW_EMPTY_PASSWORD=yes bitnami/redis:latest`

Open redis-cli
```bash
docker exec -it [CONTAINER_ID] redis-cli
```

#### Web Server

#### Build images 
build web-server docker image
```bash
docker build -f web_server/web_server.Dockerfile -t=grcp-web-server .
```

#### Run Containers
run server container
```bash
docker run -it --name web-server -p 8080:5000 grcp-web-server
```
