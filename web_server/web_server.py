# coding=utf-8
import os
from flask import Flask, render_template, send_from_directory, request
import redis

app = Flask(__name__)
redis_host = 'localhost'
flag = 'reddit'

def get_context(flag_, conn):
    output = []

    if flag_ == 'reddit':
        value = 'REDDIT COUNT: ' + str(conn.get("log.client-analytics.reddit-total"))
        output.append(value)
        value = 'LATEST REDDIT: ' + str(conn.get("log.client-analytics.reddit-latest"))
        output.append(value)
        value = 'SENTIMENT FOR LAST 3 MIN: ' + str(conn.get("log.client-analytics.reddit-3min"))
        output.append(value)
        value = 'LONGEST REDDIT: ' + str(conn.get("log.client-analytics.reddit-longest"))
        output.append(value)
    if flag_ == 'tweets':
        value = 'TOTAL COUNT: ' + str(conn.get("log.client-analytics.total"))
        output.append(value)
        value = 'LATEST TWEET: ' + str(conn.get("log.client-analytics.latest"))
        output.append(value)
        value = 'SENTIMENT FOR LAST 3 MIN: ' + str(conn.get("log.client-analytics.3min"))
        output.append(value)
        value = 'LONGEST TWEET: ' + str(conn.get("log.client-analytics.longest"))
        output.append(value)

    return output

@app.route('/', methods=['GET','POST'])
def print_tweets():
    output = []
    global flag
    # try and read from redis to then pass
    # items and translations to html (index.html)
    try:
        conn = redis.StrictRedis(host=redis_host, port=6379)
        if request.method == "GET":
            output = get_context(flag, conn)
        if request.method == "POST":
            url_from_client = request.form['url']
            """
                * static/r_dataisbeautiful_posts.csv
                * static/training.1600000.processed.noemoticon.csv
            """
            url = ''
            if url_from_client == 'dib':
                flag = 'reddit'
                url = 'static/r_dataisbeautiful_posts.csv'
                output = get_context(flag, conn)

            if url_from_client == 'tweets':
                flag = 'tweets'
                url = 'static/training.1600000.processed.noemoticon.csv'
                output = get_context(flag, conn)

            print(url)
            conn.delete('url')
            conn.set('url', url)
            conn.close()

    except Exception as ex:
        output.append('Error:' + str(ex))

    return render_template("index.html", items=output)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
