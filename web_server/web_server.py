import os
from flask import Flask, send_from_directory
import redis

app = Flask(__name__)
conn = redis.StrictRedis(host='redis', port=6379)


@app.route('/')
def hello():
    return "sample gRPC streaming application. visit route /tweets"


@app.route('/analysis')
def print_analysis():
    output = ''
    try:
        value = str(conn.get("log.client-analytics.total"))
        output += 'Total number of tweets so far: ' + str(value) + '<br>'
        value = str(conn.get("log.client-analytics.3min"))
        output += 'Last 3 minutes sentiment: ' + str(value) + '<br>'
        value = str(conn.get("log.client-analytics.longest"))
        output += 'Longest tweet so far: ' + str(value) + '<br>'
    except Exception as ex:
        output = 'Error:' + str(ex)
    return output


@app.route('/tweets')
def print_tweets():
    output = ''
    try:
        for key in conn.scan_iter("log.client-analytics.*"):
            value = str(conn.get(key))
            output += str(key) + str(value) + '<br>'
    except Exception as ex:
        output = 'Error:' + str(ex)
    return output


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
