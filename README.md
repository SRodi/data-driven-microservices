# srodi-gRPC streaming
gRPC example to implement data streaming and simulate real-time analytics

## Prerequisites
* Python version 2.7 or higher
* Docker version 19.03 or higher

## Clone repo and prepare environment
```bash
git clone https://github.com/srodi/srodi-gRPC.git
cd srodi-gRPC
pip install -r test/requirements.txt
```

## Modify proto file
View and edit `protos/test.proto` as required, `server.py` and `client.py` will have to match changes in `test.proto`

## Generate interfaces (Only if you edited `protos/test.proto`) 
Generate the gRPC client and server interfaces from .proto service definition
```bash
cd test
python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/test.proto
```

## Start Server
```bash
python -m server
```

## Start Client
```bash
python -m client
```

# Docker
Below steps allow to containerize the microservices with Docker and run docker images locally.

## Build images 
build server docker image
```bash
docker build -f server.Dockerfile -t=grcp-stream-server .
```
build client docker image
```bash
docker build -f client.Dockerfile -t=grcp-stream-client .
```

## Run Containers
run server container
```bash
docker run -it --name server -p 9999:9999 grcp-stream-server
```
run client container
```bash
docker run -it --name client --network="host" grcp-stream-client
``` 

## Clean up
remove containers
```bash
docker stop server && docker rm server client
```
remove images
```bash
docker rmi grcp-stream-server grcp-stream-client
```