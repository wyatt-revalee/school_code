#!/usr/bin/env python3

def my_for(fn, iterable):

    it = iter(iterable)
    while True:
        try:
            item = next(it)
        except StopIteration:
            break
        fn(item)
    pass

def add1(x):
    print(x+1)


my_for(add1, [0, 1, 2])

print("--------------------------")

for item in [0, 1, 2]:
    print(item + 1)
