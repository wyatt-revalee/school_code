#!/usr/bin/env python3

class MyList:
    def __init__(self):
        self.data = []

    def append(self, *args, **kwargs):
        self.data.append(*args, **kwargs)

def foo(x=5, y=4):
    print(x*y)

foo()

foo(1)

foo(y=8)

foo(x=2)
