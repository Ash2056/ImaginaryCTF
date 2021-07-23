
import os, sys, random

LEN = 24

def inp(d={}):
  return bytes(d[i] if i in d else 0 for i in range(LEN))

def add(x,y):
  return bytes((a + b) % 251 for a,b in zip(x,y))

def scale(k,x):
  return bytes(k * a % 251 for a in x)

def get_out(x):
  open("flag.txt", 'wb').write(x)
  os.system("./bullet_time")
  return open("output.txt", 'rb').read()



for i in range(24):
  with open(f"output{i}.txt", 'wb') as f:
    f.write(get_out(inp({i: 1})))
