# srodi-gRPC

## setup
```bash
git clone https://github.com/srodi/srodi-gRPC.git
cd srodi-gRPC
pip install -r requirements.txt
```

## modify the proto file
view and edit `protos/test.proto` as required,
`server.py` and `client.py` will have to match the changes
## generate the gRPC client and server interfaces from .proto service definition
```bash
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


# Build images
## to build server docker image
`docker build -f server.Dockerfile -t=grcp-stream-server .`
## to build client docker image
`docker build -f client.Dockerfile -t=grcp-stream-client .`

# Run Containers
## to run server container
`docker run -it --name server -p 9999:9999 grcp-stream-server`
## to run client container
`docker run -it --name client --network="host" grcp-stream-client` 

# Clean up
## remove containers
```bash
docker stop server && docker rm server client
```
## remove images
```bash
docker rmi grcp-stream-server grcp-stream-client
```