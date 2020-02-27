"""The Python implememntation of the GRPC srodi-gRPC client"""

import grpc
import test_pb2
import test_pb2_grpc
import datetime
import redis
longest_tweet_key = ''


def run():
    conn = redis.StrictRedis(host='redis', port=6379)
    count = 0
    """The run method, that sends gRPC conformant messages to the server"""
    with grpc.insecure_channel("tweet_stream_server:9999") as channel:
        stub = test_pb2_grpc.TestServiceStub(channel)
        total_length = 0
        for response in stub.TestCall(test_pb2.TestRequest(name='Simone')):
            total_length += len(response.message)
            print("real-time character count: " + str(total_length))
            print("Client received: " + str(response.message))
            try:
                time = datetime.datetime.now()
                key = "log.client-analytics." + str(time)
                #   store tweet
                conn.set("log.client-analytics." + str(time), "TWEET: " + response.message)
                #   evaluate  total
                conn.set("log.client-analytics.total", count)
                #   sentiment within last 3 minutes
                conn.set("log.client-analytics.3min", eval_sentiment(response.message))
                #   longest tweet
                print ("log.client-analytics.longest", eval_len(conn, response.message, key, time))
                conn.set("log.client-analytics.longest", eval_len(conn, response.message, key, time))
                count = count + 1
            except Exception as ex:
                print('Error:', ex)


def eval_sentiment(tweet):
    return 0


def eval_len(conn, tweet, key, time):
    global longest_tweet_key
    longest_tweet = str(conn.get("longest_tweet_key"))
    if len(tweet) > len(longest_tweet):
        longest_tweet_key = key
        out = 'Current longest tweet is ' + longest_tweet
        if time.min < datetime.datetime.now():
            out += ' ===> !! and the tweet arrived less than 3 min ago!!'
        return out
    else:
        return longest_tweet


def close(channel):
    """Close the channel"""
    channel.close()


if __name__ == "__main__":
    run()
