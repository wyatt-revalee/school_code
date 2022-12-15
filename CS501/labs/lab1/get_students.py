#!/usr/bin/env python3

import os
import sys

args = sys.argv[1:]

def printHelp():
    print("This program simply takes the directory '/u1/class/', filters to only the student accounts, and then prints those out. No arguments are necessary.")
    sys.exit(0)

def printVersion():
    print("get_students.py version 0.0.1")
    sys.exit(0)

if(len(args) >= 1):
    if(args[0] == "-h" or args[0] == "--help"):
        printHelp()
    if(args[0] == "-v" or args[0] == "--version"):
        printVersion()

#create sorted list of everything in /u1/class
list = os.listdir('/u1/class/')
list.sort()

#loop through it
for i in list:
    if(os.path.isdir('/u1/class/' + i)):
        if(i[0:2] == "cs"):
            if(i[2:7].isdigit() and (len(i) == 7)):
                print(i)
        if(i[0:3] == "css"):
            if(i[3:8].isdigit() and (len(i) == 8)):
                print(i)
        if(i[0:4] == "ECON"):
            if(i[4:9].isdigit() and (len(i) == 9)):
                print(i)

#check if each item is a directory, if so, check if they begin with either "cs", "css", or "ECON"
#if they do, make sure they are followed only 5 letters (check if next 5 characters are digits, and if those 5 plus the respective letters of the different strings add up to correct length)
