# -*- coding: utf-8 -*-

# just a huge red herring... but one that I got stuck in for 40 minutes :)

from numpy import base_repr
import requests
s = requests.Session()

res = s.get("https://button.max49.repl.co/noflag.html")

def encode(s): return ''.join([chr(int(c)+8203) for c in ''.join(['0000' + base_repr(ord(x), base=5) for x in s])])

def decode(s):
  ls = ''.join(str(ord(i) - 8203) for i in s if ord(i) > 8000)
  return ''.join(chr(int(x, 5)) for x in ls.rsplit('0000') if x)

def test(s="ictf{f1ag_1n_th3_c0mm3nts!}"): print(decode(encode(s)))

print(decode(res.text))
