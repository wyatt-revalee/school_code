#!/usr/bin/env python3

import json

me = {
    "first": "Wyatt",
    "last": "Revalee",
    "account": "cs50121",
    "birthMonth": "6",
    "birthDay": "29",
}

with open('me.json', 'w') as f:
    json.dump(me, f, indent=4)
