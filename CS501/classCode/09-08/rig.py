#!/usr/bin/env python3

import os
import re
from subprocess import run

# run(["ls", "-l"])

# run("echo $USER", shell=True)


res = run("cat /etc/passwd", capture_output=True, text-"utf-8", shell=True)
print(res.stdout)

regex = re.compile(r'NY|CA')

# print(regex.search(res.stdout))
