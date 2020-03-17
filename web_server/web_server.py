# coding=utf-8
import os
from flask import Flask, render_template, send_from_directory
import redis

app = Flask(__name__)
redis_host = 'redis'

@app.route('/', methods=['GET'])
def print_tweets():
    output1 = []

    # try and read from redis to then pass
    # items and translations to html (index.html)
    try:
        conn = redis.StrictRedis(host=redis_host, port=6379)
        value = 'TOTAL COUNT: '+str(conn.get("log.client-analytics.total"))
        output1.append(value)
        value = 'LATEST TWEET: '+str(conn.get("log.client-analytics.latest"))
        output1.append(value)
        value = 'SENTIMENT FOR LAST 3 MIN: ' + str(conn.get("log.client-analytics.3min"))
        output1.append(value)
        value = 'LONGEST TWEET: ' + str(conn.get("log.client-analytics.longest"))
        output1.append(value)

        conn.close()
    except Exception as ex:
        output1.append('Error:' + str(ex))

    return render_template("index.html", items=output1)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
