#!/usr/bin/env python3

import sys
import re
import urllib.request

args = sys.argv[1:]

def parse(file):

    # open link (book text file) as plain text for reading
    with urllib.request.urlopen(args[0]) as f:
        book = f.read().decode("utf-8")

    #Initialze some vars, including some regex to search the book for words

    book = book.lower()
    allregex = re.compile(r"[a-zA-Z]{4,}")     # regex for all words with len >= 3
    regex = re.compile(r"(should|could|would)") # regex for selected words
    wordcounts = {}     # dict to hold words and respective counts

    # lits of all words and total for all words
    words = allregex.findall(book)
    total = len(words)

    selectwords = regex.findall(book)

    # Iterate through selected words to create a dict of each word and its appearance (count)
    for item in selectwords:
        if item not in wordcounts.keys():
            wordcounts[item] = 1
        else:
            wordcounts[item] += 1

    #This line sorts a dictionary by its values, used to sort the dictionary by the frequencies of each word
    # Credit to Devin Jeanpierre on stackoverflow @ https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    #Edited slightly to reverse order
    wordcounts = {k: v for k, v in sorted(wordcounts.items(), key=lambda item: item[1], reverse=True)}

    # Turn values from counts into frequencies, convert to 4 decimal places
    for word in wordcounts.items():
        if type(word[1]) == int:
            wordcounts[word[0]] = (wordcounts[word[0]] / total)*100
            wordcounts[word[0]] = f'{wordcounts[word[0]]:.4f}'

    # Print to standard output in format: Word,Frequency
    colnames = "book"
    data = args[0][41:-4]
    for item in wordcounts.items():
        colnames += ","+item[0]
        data+=      ","+item[1]

    print(colnames)
    print(data)

#Call parse to do everything
parse(args[0])
