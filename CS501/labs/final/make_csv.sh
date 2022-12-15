#1/usr/bin/env bash

# This script runs author_parse.py with all of the text files of books, and then outputs them to their respective csv files in public_html/authors

NEWLINE=$'\n'
nums=(1 2 3 4 5)
letters=(a b)

for i in "${letters[@]}"; do
    for j in "${nums[@]}"; do
        echo "$(./author_parse.py https://cs.indstate.edu/~cs50121/authors/$i$j.txt > ~/public_html/authors/$i$j.csv)"
    done
done

for i in "${letters[@]}"; do
    echo "$(./author_parse.py https://cs.indstate.edu/~cs50121/authors/u$i.txt > ~/public_html/authors/u$i.csv)"
done
