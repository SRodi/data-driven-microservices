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
server_tweets = 'tweet-stream-server'
server_reddit = 'reddit-stream-server'
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

    try:
        conn = redis.StrictRedis(host=redis_host, port=6379)
        # wait for connection
        while not conn.get('url'): continue
        while conn.get('url'):
            url = conn.get('url')

            if url == 'static/training.1600000.processed.noemoticon.csv':
                with grpc.insecure_channel(server_tweets + ":9999") as channel:
                    total_length = 0
                    stub = test_pb2_grpc.TestServiceStub(channel)
                    result_generator = stub.TestCall(test_pb2.TestRequest(name=url))
                    # if not url: url = 'static/training.1600000.processed.noemoticon.csv'
                    for response in result_generator:
                        print(response.message)
                        total_length += len(response.message)
                        print("tweets real-time character count: " + str(total_length))
                        print("Client received from tweets server: " + str(response.message))
                        message = str(response.message)
                        blob = TextBlob(message)
                        sent_3min = eval_sentiment(blob)
                        sys.stdout.flush()

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

                        if url != conn.get('url'):
                            channel.close()
                            break

            if url == 'static/r_dataisbeautiful_posts.csv':
                with grpc.insecure_channel(server_reddit + ":9998") as channel:
                    total_length = 0
                    stub = test_pb2_grpc.TestServiceStub(channel)
                    result_generator = stub.TestCall(test_pb2.TestRequest(name=url))
                    # if not url: url = 'static/training.1600000.processed.noemoticon.csv'
                    for response in result_generator:
                        print(response.message)
                        total_length += len(response.message)
                        print("reddit real-time character count: " + str(total_length))
                        print("Client received from reddit server: " + str(response.message))
                        message = str(response.message)
                        blob = TextBlob(message)
                        sent_3min = eval_sentiment(blob)
                        sys.stdout.flush()

                        time = datetime.datetime.now()
                        #   store reddit
                        conn.set("log.client-analytics.reddit"+str(time), message)
                        #   evaluate  total
                        conn.set("log.client-analytics.reddit-total", count)
                        # current tweet
                        conn.set("log.client-analytics.reddit-latest", message)
                        #   sentiment of current tweet
                        conn.set("log.client-analytics.reddit-3min", sent_3min)

                        #   longest tweet
                        if count == 0:
                            conn.set("log.client-analytics.reddit-longest", message)
                        else:
                            conn.set("log.client-analytics.reddit-longest", eval_len(message))
                        # increment tweet count
                        count = count + 1

                        if url != conn.get('url'):
                            channel.close()
                            break

        conn.close()
    except Exception as ex:
        print('Error:', ex)

def close(channel):
    """Close the channel"""
    channel.close()


if __name__ == "__main__":
    run()
