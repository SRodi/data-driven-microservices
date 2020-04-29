import redis
def get_from_redis(event, context):
  try:
    conn = redis.StrictRedis(host='redis', port=6379)
    res =  conn.get('test')
  except redis.exceptions.ConnectionError:
    res = 'error occurred'
  return res

"""
kubeless function deploy test --runtime python2.7 \
    --from-file test.py \
    --handler redis-test.get_from_redis --dependencies requirements.txt

kubeless function call test

kubeless function delete test

"""