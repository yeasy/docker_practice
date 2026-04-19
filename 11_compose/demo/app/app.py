import os
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=int(os.environ.get('REDIS_PORT', 6379)))

@app.route('/')
def hello():
    try:
        count = redis.incr('hits')
        return 'Hello World! 该页面已被访问 {} 次。\n'.format(count)
    except redis.RedisError:
        return 'Hello World! 无法访问计数器。\n', 500

@app.route('/health')
def health():
    try:
        redis.ping()
        return 'OK', 200
    except redis.RedisError:
        return 'Redis unavailable', 503

if __name__ == "__main__":
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host="0.0.0.0", debug=debug)
