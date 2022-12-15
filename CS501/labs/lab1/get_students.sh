#!/usr/bin/env bash

if [ $1 == "--help" ] || [ $1 == "-h" ];
then
    echo $'--help, -h: Prints this help message.\n--version, -v: Prints the program version.'
    exit 0
fi

if [ $1 == "--version" ] || [ $1 == "-v" ];
then
    echo $'get_students.sh Version 0.0.1'
    exit 0
fi

ls /u1/class | grep -E 'cs{1,2}[0-9]{5}$'

#list contents of /u1/class, grep it using regex for 'c' followed by 1-2 's's, then exactly 5 digits.
