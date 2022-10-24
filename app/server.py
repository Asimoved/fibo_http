#!/usr/bin/python3

import sys

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

from flask_sock import Sock

from redis import Redis

from rq import Queue
from rq.job import Job

sys.set_int_max_str_digits(10000000)

r = Redis("myredis", 6379)
q = Queue(connection=r)

app = Flask(__name__)
sock = Sock(app)

@app.route('/', methods=['GET'])
def fibo_server():

    try:
        n = int(request.args.get('n'))
    except TypeError:
        return make_response('please provide an integer', 400)

    job = q.enqueue('fibo.fib', n, job_id=str(n), result_ttl=86400)
    job.refresh() # todo: why is there no result for very quick calculations?
    if job.result: # already calculated
        resp = make_response(str(job.result))
    else:
        resp = make_response('calculating...')
        resp.headers['Refresh'] = 1

    return resp


@app.route('/form')
def form():
    return render_template('form.html')


@sock.route('/fib')
def echo(sock):
    while True:
        n = sock.receive()
        try:
            n = int(n)
        except:
            res = 'please provide a valid integer!'
            n = ''
        if n:
            job = q.enqueue('fibo.fib', n, job_id=str(n), result_ttl=86400)
            while job.result == None:
                job.refresh()
            res = job.result
        sock.send(res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
