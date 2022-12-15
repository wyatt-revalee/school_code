#1/usr/bin/env bash

nums=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17)
for i in "${nums[@]}"; do
    echo "$i. $(./$i.py)"
done
