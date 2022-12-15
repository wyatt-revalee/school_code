#!/usr/bin/env python3

import sys

fin = open("args.py", "r")
data = fin.read()
fin.close()

print(data)

with open("args.py", "r") as f:
	data = f.read()