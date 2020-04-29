# coding=utf-8
"""The Python implememntation of the GRPC srodi-gRPC client"""
import threading
import time

import grpc
import test_pb2
import test_pb2_grpc
import datetime
import redis
import sys
from textblob import TextBlob

longest_tweet = ''
longest_reddit = ''
redis_host = 'redis'
server_tweets = 'tweet-stream-server:9999'
server_reddit = 'reddit-stream-server:9998'
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


def eval_len(text, flag):
    global longest_reddit
    global longest_tweet
    out = ''
    if flag == 'tweet':
        if len(text) > len(longest_tweet):
            longest_tweet = text
        out = longest_tweet
    if flag == 'reddit':
        if len(text) > len(longest_reddit):
            longest_reddit = text
        out = longest_reddit
    return out

def check_redis():
    redis_test = redis.StrictRedis()  # non-default ports could go here
    try:
        return redis_test.ping()
    except redis.exceptions.ConnectionError:
        return 'err'

def stream_tweet(conn, url):
    with grpc.insecure_channel(server_tweets) as channel:
        total_length = 0
        count = 0
        stub = test_pb2_grpc.TestServiceStub(channel)
        result_generator = stub.TestCall(test_pb2.TestRequest(name=url), wait_for_ready=True)

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
                conn.set("log.client-analytics.longest", eval_len(message, 'tweet'))
            # increment tweet count
            count = count + 1

            if url != conn.get('url'):
                channel.close()
                break

def stream_reddit(conn, url):
    with grpc.insecure_channel(server_reddit) as channel:
        total_length = 0
        count = 0
        stub = test_pb2_grpc.TestServiceStub(channel)
        result_generator = stub.TestCall(test_pb2.TestRequest(name=url), wait_for_ready=True)

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
            conn.set("log.client-analytics.reddit" + str(time), message)
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
                conn.set("log.client-analytics.reddit-longest", eval_len(message, 'reddit'))
            # increment tweet count
            count = count + 1

            if url != conn.get('url'):
                channel.close()
                break

def run():
    # wait till redis is available
    while check_redis() == 'err': continue
    conn = redis.StrictRedis(host=redis_host, port=6379)

    print('successfully connected to redis')

    # wait until dataset url is populated in redis
    while not conn.get('url'): continue

    print('successfully fetched a value from redis')

    while conn.get('url'):
        url = conn.get('url')
        print(url)
        try:
            if url == b'static/training.1600000.processed.noemoticon.csv':
                print('connected to tweet stream service')
                t1 = threading.Thread(target=stream_tweet(conn, url))
                t1.start()
        except grpc.RpcError as e:
            print('grpc error', e)

        try:
            if url == b'static/r_dataisbeautiful_posts.csv':
                print('connected to reddit stream service')
                t2 = threading.Thread(target=stream_reddit(conn, url))
                t2.start()
        except grpc.RpcError as e:
            print('grpc error', e)

        time.sleep(1)

if __name__ == "__main__":
    run()
