"""The Python implementation of the GRPC srodi-gRPC server."""
from concurrent import futures
import grpc
import test_pb2
import time
import test_pb2_grpc


class TestService(test_pb2_grpc.TestServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.messages = ["Hello ", "Greetings ", "All the best ", "Nice to meet you "]

    def TestCall(self, request, context):
        for g in self.messages:
            time.sleep(2)
            yield test_pb2.TestResponse(message=g + request.name)


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestServiceServicer_to_server(TestService(), server)
    server.add_insecure_port("[::]:9999")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
