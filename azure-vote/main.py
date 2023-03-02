from flask import Flask, request, make_response, render_template
import os
import redis
import socket
import multiprocessing as mp
import time
import uuid


app = Flask(__name__)
ver = "1.0.110"

button1 = "Maël"
button2 = "Florian"
host = socket.gethostname()
hostn = os.environ.get('HOSTNAME', str(uuid.uuid4()))
title = f"Azure Voting App v{ver} on {host}"
stress_time = float(os.environ.get('STRESS_SECS', 0))


class NoRedis():
    def __init__(self):
        self.db = {}

    def get(self, k):
        return str(self.db.get(k, '')).encode('utf-8')

    def set(self, k, v):
        self.db[k] = v

    def incr(self, k, n):
        self.db[k] += n


if 'REDIS' in os.environ:
# Redis configurations
    redis_server = os.environ['REDIS']
    redis_tls = os.environ.get('REDIS_TLS', 'OFF')

    if redis_tls == 'ON':
        redis_port = 6380
        redis_tls = True
    else:
        redis_port = 6379
        redis_tls = False


# Redis Connection
    try:
        if "REDIS_PWD" in os.environ:
            r = redis.StrictRedis(host=redis_server,
                                  port=redis_port,
                                  ssl=redis_tls,
                                  password=os.environ['REDIS_PWD'])
        else:
            r = redis.Redis(redis_server)
        r.ping()
    except redis.ConnectionError:
        exit('Failed to connect to Redis, terminating.')
else:
    r = NoRedis()


# Redis initialization
if not r.get(button1):
    r.set(button1, 0)
if not r.get(button2):
    r.set(button2, 0)


def stress(x):
    timeout = time.time() + stress_time  # X seconds from now
    while True:
        if time.time() > timeout:
            break
        x * x


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['vote'] == 'reset':
            # Empty table and return results
            r.set(button1, 0)
            r.set(button2, 0)
        else:
            # Insert vote result into DB
            r.incr(request.form['vote'], 1)

            if stress_time > 0:
                # Generate fake load
                mp.Pool(mp.cpu_count()).map(stress, range(mp.cpu_count()))

    vote1 = r.get(button1).decode('utf-8')
    vote2 = r.get(button2).decode('utf-8')

    resp = make_response(render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title))
    resp.headers.set('X-HANDLED-BY', hostn)
    resp.headers.set('X-APP-VERSION', ver)
    return resp


if __name__ == "__main__":
    app.run()
