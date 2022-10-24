#!/usr/bin/python3

from redis import Redis
from rq import Queue, Worker

r = Redis("myredis", 6379)
q = Queue(connection=r)
w = Worker([q], connection=r)
w.work()
