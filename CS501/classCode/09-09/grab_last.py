#!/usr/bin/env python3

import sys

args = sys.argv[1:]

fs = args[0] if len(args) else " "

for line in sys.stdin:
    l = line
    if line[-1:] == "\n":
        l = line[:-1]
    li = l.split(fs)
    print(li[-1])
