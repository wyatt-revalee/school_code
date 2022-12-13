#!/usr/bin/env python3

import sys
import csv

args = sys.argv[1:]
args = str(args[0])

with open(args, mode='r') as infile:
    reader = csv.reader(infile)
    reader = list(filter(None, reader))
    k = None
    v = None
    users = []
    user_rows = []
    for i in range(1, len(reader)):
        user_rows.append(reader[i])
    for i in user_rows:
        dict = {k:v for (k,v) in zip(reader[0],i)}
        users.append(dict)

n = len(users)
for i in range(n):
    print(users[i]["id"])
