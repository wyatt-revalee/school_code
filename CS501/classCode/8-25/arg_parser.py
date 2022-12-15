#!/usr/bin/env python3

import os
import json

script_dir = os.path.realpath(os.path.dirname(__file__))
config_path = os.path.join(script_dir, "arg_parser_config.json")

with open(config_path) as f:
	cfg_s = f.read()

cfg = json.loads(cfg_s)

class ArgParser:
	def __init__(self, x):
		self.x = x
		print(self.x)
		print(x)
		print(id(self.x), id(x))

	def print_item(self, item):
		print(item)

if __name__ == "__main__":
	print(f"Running tests for {__file__}.")

	ap = ArgParser(5)

	print("------------------------")

	exit(0)

	print(ap)
	print(type(ap))
	print(*dir(ap), sep="\n")
