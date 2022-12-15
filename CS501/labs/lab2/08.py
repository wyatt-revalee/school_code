#!/usr/bin/env python3

import re
import urllib.request

#Get file and place contents in string called req_data
with urllib.request.urlopen("https://cs.indstate.edu/~lmay1/assets/rig.txt") as req:
    req_data = req.read().decode("utf-8")

#split req_data into list of lines to make it easier to loop through
req_data = req_data.split("\n")

#create regex object that matches our query and initialize integer match counter
regex = re.compile(r"^[0-9]{1} .* (Blvd|Ln|Terr|Ave)$")
matchCount = 0

#iterate through req_data, line by line
#if a line matches our regex search, print it, and add one to our counter
for i in range(len(req_data)):
    if(regex.search(req_data[i])):
        matchCount += 1
        j = -1
        while(j < 3):
            print(req_data[i+j])
            j += 1
        print()

#after all of the matching lines are printed, print the number of matches
print(matchCount)
