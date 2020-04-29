"""
    UNIT TESTS


    - https://stackoverflow.com/questions/51792592/how-to-write-unit-tests-for-your-grpc-server-in-python

    - https://github.com/grpc/grpc/issues/17453

"""

import unittest
import redis
import grpc
import test_pb2_grpc, test_pb2

class GenericTests(unittest.TestCase):

    # this tests redis on "localhost" on default port "6379"
    def test_redis(self):
        redis_test = redis.StrictRedis()
        self.assertTrue(redis_test.ping(),True)

    # define values for testing tweet and reddit gRPC services
    server_tweets = 'localhost:9999'
    url_tweeets='static/training.1600000.processed.noemoticon.csv'
    server_reddit = 'localhost:9998'
    url_reddit='static/r_dataisbeautiful_posts.csv'

    # test tweet gRPC service
    def test_tweet_server(self):
        res = ''
        with grpc.insecure_channel(self.server_tweets) as channel:
            stub = test_pb2_grpc.TestServiceStub(channel)
            result_generator = stub.TestCall(test_pb2.TestRequest(name=self.url_tweeets), wait_for_ready=True)
            for response in result_generator:
                res += response.message
                break
            channel.close()
        self.assertEqual(res, '@switchfoot http://twitpic.com/2y1zl - Awww, that\'s a bummer.  You shoulda got David Carr of Third Day to do it. ;D')

    # test Reddit gRPC server
    def test_reddit_server(self):
        res = ''
        with grpc.insecure_channel(self.server_reddit) as channel:
            stub = test_pb2_grpc.TestServiceStub(channel)
            result_generator = stub.TestCall(test_pb2.TestRequest(name=self.url_reddit), wait_for_ready=True)
            for response in result_generator:
                res += response.message
                break
            channel.close()
        self.assertEqual(res, 'removed_by')

if __name__ == '__main__':
    unittest.main()
