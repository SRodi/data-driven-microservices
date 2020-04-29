import redis
def redis_set(event, context):
    res = event['data']
    try:
      conn = redis.StrictRedis(host='redis', port=6379)
      conn.set('test', event['data'])
    except redis.exceptions.ConnectionError:
      res = 'error occurred'
    return res

"""
kubeless function deploy redis-set --runtime python2.7 \
    --from-file redis-write.py \
    --handler redis-write.redis_set --dependencies requirements.txt

kubeless function call redis-set --data 'test-value1'

kubeless function delete redis-set

"""

