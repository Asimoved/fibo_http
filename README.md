
# Async Fibonacci Server

This simple server given integer n will calculate the nth Fibonacci number. Since this calculation can take significant time, the task is passed to a queue and ran by a worker, so it does no hang the server process. The task and the results are stored in a redis db. The components are separated into three docker containers which are are orchestrated by docker compose.

Advantages:
- the services are separated, so even if the server or worker go down, existing tasks and results are kept
- the started tasks and previously calculated results are kept (for a day) so these results can be returned immediately for new queries
- if a second client asks for a calculation that has already been started, no new task will be created and the result will be provided once it is complete
    + this is possible, because the job ID is the integer itself, so if another client requests it, that job already exists
- both from the browser and the client the result will be checked in 1 second intervals

Disadvantages:
- the worker does not immediately return the result, even if the calculation is almost instant, so at least one refresh is required (this can probably be improved)
- due to the stateless nature of http the client has to check for the result, which can be improved by using sockets

## Prequisites

- git
- docker

## Installation

- download or clone this repository from github: git clone https://github.com/Asimoved/fibo_server_test.git
- from the main directory run: docker compose up -d
    + docker will download the official redis image, build the app and worker images from their respective directories

The web server will start listening on http://localhost:5000

You can immediately test from the command line with: python client.py 1 (or: python3 client.py 1)

## Usage


### From the browser (http)
- visit http://localhost:5000 and provide an integer in the URL
    + The server will require a valid n integer as a parameter in the format: ?n=1
- the browser will keep refreshing until the result is returned

### From the browser (socket, js)
- visit http://localhost:5000/form
- submit a valid integer, the form will start a socket connection
- the result will be returned when the calculation is complete

### From the test client
- run python fibo_client.py N from the main directory, N being a valid 0 or positive integer
- for example: python fibo_client.py 42 (or python3 fibo_client.py 42)
- the test client will wait for the result

If the connection is lost (you can simulate it by stopping the web server app container) the client will let you know and it will keep retrying. If the connection is back, the result will be returned, or it will keep waiting. If the worker and redis containers are still running the result will still be calculated in the background, so it will not have to be started again.

# Packages

- Flask
- flask_sock
- rq (Python RQ)
- redis

# References

https://stackoverflow.com/questions/283752/refresh-http-header
