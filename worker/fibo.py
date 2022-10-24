#!/usr/bin/python3

# https://stackoverflow.com/questions/18172257/efficient-calculation-of-fibonacci-series

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a
