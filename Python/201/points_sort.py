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

# Function for sorting by last names. Used for ties.
def isAlphabetical(word1, word2):
    i = 0
    while i < max(len(word1), len(word2)):

        if i+1 > len(word1) and i+1 <= len(word2):
            return True

        if i+1 <= len(word1) and i+1 > len(word2):
            return False

        if ord(word1[i]) < ord(word2[i]):
            return True

        elif  ord(word1[i]) > ord(word2[i]):
            return False

        i += 1
    return

def bubble_sort(arr):
    for i in range(n-1):
        for j in range(n-1-i):
            if arr[j]["points"] < arr[j+1]["points"]:
                arr[j], arr[j+1], = arr[j+1], arr[j]

            # If users' scores are tied, the program then sorts by last names
            if arr[j]["points"] == arr[j+1]["points"]:
                if not isAlphabetical(arr[j]["last"], arr[j+1]["last"]):
                    arr[j+1], arr[j], = arr[j], arr[j+1]


bubble_sort(users)

for i in range(n):
    print(users[i]["id"])
