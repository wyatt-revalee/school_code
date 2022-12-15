#!/user/bin/env python3

from functools import reduce
import sys
import re

args = sys.argv[1:]

def parse_file(file):
    with open(file, "r") as f:
        s = f.read()

    s = s.lower()

    s = re.sub(r"[^a-z\s]", "", s)
    words = re.split(r"\s+", s)


    counts = {}
    def reducer(acc, item):
        if item not in counts.keys():
            acc[item] = 1
        else:
            acc[item] += 1
        return acc
    counts = reduce(reducer, words, counts)



    length = len(words)
    freqs = [ (v/length, k) for k, v, in counts.items() if len(k) > 3]

    freqs.sort(reverse=False)
    print("-"*50)

    for f in freqs:
        print(f"{f[1]: <30} {f[0]*100: >6.4f}")

    # print(*freqs[:50], sep="\n")
    exit(0)

if __name__ == "__main__":

    print(args)
    parse_file(args[0])
