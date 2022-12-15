#!/usr/bin/env python3

import sys

args = sys.argv[1:]

look_for = input("What are you looking for? ")

print(args)

res = {}

for arg in args:
	sp = arg.split("=")
	if len(sp) > 1:
		res[sp[0].lstrip("-")] = sp[1]


print(res)