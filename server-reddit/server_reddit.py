"""The Python implementation of the GRPC srodi-gRPC server."""
from concurrent import futures
import grpc
import test_pb2
import time
import test_pb2_grpc
import csv
# from kaggle.api.kaggle_api_extended import KaggleApi
# import zipfile

class TestService(test_pb2_grpc.TestServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""
    def __init__(self):
        print("server running on port 9998")
        self.messages = []

        # # authenticate to kaggle make sure kaggle api is installed and
        # # your credentials file is in ~/.kaggle/kaggle.json
        # api = KaggleApi()
        # api.authenticate()
        # # download single file from kaggle
        # # Signature: dataset_download_file(dataset, file_name, path=None, force=False, quiet=True)
        # api.dataset_download_file('unanimad/dataisbeautiful', 'r_dataisbeautiful_posts.csv',
        #                           path='/Users/sk/Documents/src/srodi-gRPC/server-reddit/static')
        # # unzip and save to static folder
        # with zipfile.ZipFile('/Users/sk/Documents/src/srodi-gRPC/server-reddit/static/r_dataisbeautiful_posts.csv.zip',
        #                      'r') as zip_ref:
        #     zip_ref.extractall('/Users/sk/Documents/src/srodi-gRPC/server-reddit/static/')
        #
        # print("downloaded reddit dataset")

    def TestCall(self, request, context):
        # request.name to access value sent by client
        print('client: ', str(request.name))

        with open('static/r_dataisbeautiful_posts.csv') as csv_file:
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
                # print('Processed ', line_count, ' lines.')
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
    server.add_insecure_port("[::]:9998")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
