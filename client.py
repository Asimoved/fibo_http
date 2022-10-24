#!/usr/bin/python3

# a simple client for the fibonacci server

import sys
import time
import http.client

try:
    url = "/?n=%s" % sys.argv[1]
except:
    print('please provide an integer!')
    quit()

reloads = 0
default_result = 'calculating...'

connection = http.client.HTTPConnection('127.0.0.1', 5000)
try:
    connection.request("GET", url)
except ConnectionRefusedError:
    print("can't connect to server")
    quit()

response = connection.getresponse()
result = response.read().decode()

print('working...press CTRL+C to quit')

while result == default_result:
    reloads += 1
    connection = http.client.HTTPConnection('127.0.0.1', 5000)
    try:
        connection.request("GET", url)
        response = connection.getresponse()
        result = response.read().decode()
    except:
        print('connection lost, retrying...press CTRL+C to quit')

    if not reloads % 5:
        print('still working...')

    time.sleep(1)

print(result)

connection.close()
