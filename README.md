# srodi-gRPC

## setup
```bash
git clone https://github.com/srodi/srodi-gRPC.git
cd srodi-gRPC
pip install -r requirements.txt
```

## generate python files
```bash
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/example.proto
```

## Start Server
```bash
python -m server
```

## Start Client
```bash
python -m client
```

## Start Multiple clients in sperate processes
```bash
python -m multiprocess
```