#!/usr/bin/env python3

import sys

args = sys.argv[1:]

look_for = "-n" # input("What are you looking for?")

if look_for in args:
	i = args.index(look_for)
	print(f'The key"{look_for}" was found at index {i}.')
	if len(args) < i+1:
		print("No value given to \"-n\" option.")
	x = args[i+1]

else:
	print(f"The key {look_for} was not found.")
