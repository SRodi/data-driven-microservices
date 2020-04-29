"""The Python implementation of the GRPC srodi-gRPC server."""
from concurrent import futures
import grpc
import test_pb2
import time
import test_pb2_grpc
import csv

class TestService(test_pb2_grpc.TestServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""
    def __init__(self):
        print("server running on port 9999")
        self.messages = []

    def TestCall(self, request, context):
        # request.name to access value sent by client
        print('client: ', str(request.name))

        with open('static/training.1600000.processed.noemoticon.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            try:
                for row in csv_reader:
                    for col in range(len(row)):
                        if col == 4:  # and line_count < 100:
                            # row[col] is the sender
                            # row[col + 1] is the tweet
                            self.messages.append(row[col + 1])
                    line_count += 1
            except UnicodeDecodeError:
                print('UnicodeDecodeError')

        for g in self.messages:
            time.sleep(2)
            if len(g) > 0:
                yield test_pb2.TestResponse(message=g)

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
