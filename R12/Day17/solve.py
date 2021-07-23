from base import *
from more_itertools import chunked
import re

N_624 = 624
M_397 = 397

def outMersenne(y):
  y ^= (y >> 11)
  y ^= (y <<  7) & 0x9d2c_5680
  y ^= (y << 15) & 0xefc6_0000
  y ^= (y >> 18)
  return y

def undoR(out, shift):
  inp = out
  top = out >> shift
  while top:
    inp ^= top
    top >>= shift
  return inp

def undoL(out, shift, mask):
  bot_ones = (1 << shift) - 1
  prev = 0
  inp = 0
  for i in range(0,32,shift):
    prev = ((mask & prev) ^ out) & bot_ones
    inp |= prev << i
    out >>= shift
    mask >>= shift
  return inp

def inpMersenne(y):
  y = undoR(y, 18)
  y = undoL(y, 15, 0xefc6_0000)
  y = undoL(y,  7, 0x9d2c_5680)
  y = undoR(y, 11)
  return y


reIncident = re.compile("Subject: Password Recovery Incident #(\d+)")

with open("password.recovery.mbox") as f:
  ls = f.read().split("\n\n\n")
  samples = []
  target = set()
  for lns in ls:
    l = lns.strip().splitlines()
    m = reIncident.match(l[7]) if l else None
    if m:
      idx = (int(m.group(1)) - 72506) * 2
      if 'michaelscottpaper.company' in lns: target.update({idx, idx+1})
      if 'your mobile phone on record' in l[-1]:
        samples.extend([None, None])
      else:
        decode = [int.from_bytes(x, 'big') for x in chunked(b64d(l[-1]), 4)]
        samples.extend(map(inpMersenne, decode))

print(samples)

def f(st_idx, st_idx1, st_idxN):
  y = (st_idx & 0x80000000) + (st_idx1 & 0x7fffffff)
  next = y >> 1
  if (y & 1) == 1:
    next ^= 0x9908b0df
  return next ^ st_idxN

for i in range(N_624):
  try:
    print(outMersenne(f(samples[i], samples[i+1], samples[i + N_624])).to_bytes(4, 'big').decode(), end='')
  except: pass
print()

from random import getrandbits
st = [inpMersenne(getrandbits(32)) for _ in range(N_624 + 11)]

# recover any large index in the first state, using small indices in both states
for i in range(len(st) - N_624 - 1):
  a = f(st[i], st[i+1], st[i + N_624])
  b = st[i + M_397]
  assert a == b

