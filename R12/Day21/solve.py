from base import *
from more_itertools import chunked
import re

N = 624
M = 397

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

with open("password.recovery.pt3.mbox") as f:
  ls = f.read().split("\n\n\n")
  samples = {}
  for lns in ls:
    l = lns.strip().splitlines()
    m = reIncident.match(l[7]) if l else None
    if m:
      idx = int(m.group(1))
      if 'your mobile phone on record' in l[-1]:
        samples[idx] = None
        samples[idx+1] = None
      else:
        decode = [int.from_bytes(x, 'big') for x in chunked(b64d(l[-1]), 4)]
        samples[idx] = inpMersenne(decode[0])
        samples[idx+1] = inpMersenne(decode[1])

# print(samples)

def f(st_idx, st_idx1, st_idxN):
  y = (st_idx & 0x80000000) + (st_idx1 & 0x7fffffff)
  next = y >> 1
  if (y & 1) == 1:
    next ^= 0x9908b0df
  return next ^ st_idxN

def inv(next):
  bot_bit = 0
  if next >= 0x80000000:
    next ^= 0x9908b0df
    bot_bit = 1
  next = (next << 1) | bot_bit
  return next & 0x80000000, next & 0x7fffffff

recovered = {}

def go():
  for m in sorted(samples):
    n = m-M+N
    if n-N not in recovered and m-1 in samples and n in samples and n-1 in samples:
      next0 = samples[m] ^ samples[n]
      next1 = samples[m-1] ^ samples[n-1]
      top, _ = inv(next0)
      _, bot = inv(next1)
      samples[n-N] = top | bot
      recovered[n-N] = outMersenne(top | bot).to_bytes(4,'big')

go()
go()
# call this any number of times to back-generate more

print(flag_bre.search(b"".join(recovered[k] for k in sorted(recovered))))

