#!/usr/bin/env python3

import os
import sys

class ArgParser():

    def __init__(self, desc, version="v0.0.1", file="__file__"):

        self.description = desc
        self.version = version

        self.argv = sys.argv[:]
        self.args = self.argv[1:]

        self.prog_path = os.path.realpath(__file__)
        self.prog_dir = os.path.dirname(self.prog_path)
        self.prog_name = os.path.basename(self.prog_path)

        print(self.prog_path)
        print(self.prog_dir)
        print(self.prog_name)


        self.fns = {}
        self.aliases = {}
        self.arg_help = [
        "--help, -h: Prints this help.",
        "--version, -v: Prints the version."
        ]
        self.parsed = {
        "_": [], #positional arguments
            # "-n": [4, 6, 9],
            # "--foo": "bar",
            # "--spam": "eggs",
        }

        self.add_arg_option(["--help", "-h"], "Prints this help text.")
        self.add_arg_option(["--version", "-v"], "Prints the version.")

    def print_help(self):
        msg = f"{self.prog_name} {self.version}\n\n{self.description}\n"
        msg += "\n".join(self.arg_help)
        print(msg)
        exit(0)


    def add_arg_option(self, names, desc, fn=None, n_values=0, value_types=None):
        if type(names) is not list:
            names = [names]
        if type(names[0]) is not str:
            print("Argument options must have string names.", file=sys.stderr)
            exit(1)

        for alias in names:
            self.aliases[alias] = [names[0]]
        self.arg_help.append(f"{', '.join(names)}: {desc}")

if __name__ == "__main__":
    print(f"Running tests for {os.path.basename(os.path.realpath(__file__))}.")

    print("------------------------------------")
    ap = ArgParser(__file__)

    print("------------------------------------")

    ap.add_arg_option(["--number", "-n"], "Number of items.", )
    ap.print_help()
