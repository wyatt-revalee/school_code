#!/usr/bin/env/python3

import sys

print(sys.argv)

args = sys.argv[1:]

print(args)

# find in array

try:
	i = args.index("-h")
except:
	print("-h not found.")
else:
	print("-h found")