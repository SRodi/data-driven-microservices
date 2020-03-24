# coding=utf-8
"""The Python implememntation of the GRPC srodi-gRPC client"""

import grpc
import test_pb2
import test_pb2_grpc
import datetime
import redis
import sys
from textblob import TextBlob

longest_tweet = ''
overall_sentiment = {'positive': 0,'negative': 0}
redis_host = 'redis'
server_host = 'tweet-stream-server'
rolling_metrics_array = []

def calc_fraction(a, b):
    tot = a + b
    print('total: ',tot)
    pos_pc = a/tot
    neg_pc = b/tot
    return pos_pc, neg_pc

def eval_sentiment(blob):
    # current tweet sentiment
    sentiment_tweet = blob.sentences[0].sentiment.polarity
    print(sentiment_tweet)

    # we assume the there is a new tweet in the stream every 2 seconds
    # so there can be a max of 90 tweets in 3 min
    if len(rolling_metrics_array) >= 90:
        del rolling_metrics_array[0]
    rolling_metrics_array.append(sentiment_tweet)

    # check if avg sentiment for last 90 tweets is pos/neg
    if sum(rolling_metrics_array)/len(rolling_metrics_array) < 0:
        sentiment = 'negative'
    else:
        sentiment = 'positive'

    return sentiment + ' (' + str(len(rolling_metrics_array)) + ' tweets in last 3 min) CURRENT TWEET: ' + str(sentiment_tweet)


def eval_len(tweet):
    global longest_tweet
    if len(tweet) > len(longest_tweet):
        longest_tweet = tweet
    return longest_tweet


def run():
    count = 0
    global overall_dict
    """The run method, that sends gRPC conformant messages to the server"""
    with grpc.insecure_channel(server_host+":9999") as channel:
        stub = test_pb2_grpc.TestServiceStub(channel)
        total_length = 0
        for response in stub.TestCall(test_pb2.TestRequest(name='Simone')):
            total_length += len(response.message)
            print("real-time character count: " + str(total_length))
            print("Client received: " + str(response.message))
            message = str(response.message)
            blob = TextBlob(message)
            sent_3min = eval_sentiment(blob)
            sys.stdout.flush()
            try:
                conn = redis.StrictRedis(host=redis_host, port=6379)

                time = datetime.datetime.now()
                #   store tweet
                conn.set("log.client-analytics." + str(time), message)
                #   evaluate  total
                conn.set("log.client-analytics.total", count)
                # current tweet
                conn.set("log.client-analytics.latest", message)
                #   sentiment of current tweet
                conn.set("log.client-analytics.3min", sent_3min)

                #   longest tweet
                if count == 0:
                    conn.set("log.client-analytics.longest", message)
                else:
                    conn.set("log.client-analytics.longest", eval_len(message))
                # increment tweet count
                count = count + 1

                conn.close()
            except Exception as ex:
                print('Error:', ex)


def close(channel):
    """Close the channel"""
    channel.close()


if __name__ == "__main__":
    run()
