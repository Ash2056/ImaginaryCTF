#!/bin/env python3

import requests as r
from base import dump

url = 'https://spider.031337.xyz'

def reqDump(): dump(r.get(url))

# It's important to debug!
reqDump()

def go():
  s = ''
  for i in range(999):
    s += r.get(f"{url}/{i}").headers['x-flag']
    print("\r" + s, end='')
    if '}' in s:
      print()
      return s

go()

# ictf{f0ll0w_th3_numb3rs}
