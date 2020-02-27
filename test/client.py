"""The Python implememntation of the GRPC srodi-gRPC client"""

import grpc
import test_pb2
import test_pb2_grpc


def run():
    """The run method, that sends gRPC conformant messages to the server"""
    with grpc.insecure_channel("tweet_stream_server:9999") as channel:
        stub = test_pb2_grpc.TestServiceStub(channel)
        total_length = 0
        for response in stub.TestCall(test_pb2.TestRequest(name='Simone')):
            total_length += len(response.message)
            print("real-time character count: " + str(total_length))
            print("Client received: " + str(response.message))


def close(channel):
    """Close the channel"""
    channel.close()


if __name__ == "__main__":
    run()
