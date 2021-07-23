from collections import Counter, defaultdict
from itertools import islice

from base import *
from png import *
from more_itertools import *
from math import *
from pwn import p32

img: PngImageFile = Image.open("smells_Like_Stereo_Bits.png")
pxl: PyAccess = img.load()

w, h = img.size

freq = defaultdict(list)

def dist(p1, p2):
  if type(p1) == int: return abs(p1-p2)
  return isqrt(sum((dist(x,y))**2 for x,y in zip(p1, p2)))

def sqr(x,y,sz=1):
  x -= x%sz
  y -= y%sz
  return tuple(tuple(pxl[x+i,y+j][:3] for i in range(sz)) for j in range(sz))

cycle_len = 161

def fit(x, y):
  if x < cycle_len: return 0
  d1 = dist(sqr(x, y), sqr((x-1)%cycle_len, y))
  d2 = dist(sqr(x, y), sqr((x+0)%cycle_len, y))

  return 255*(min(d1,d2) > 10)

# for x in range(0,w-2,3):
#   for y in range(0,h-2,3):
#     freq[sqr(x,y)].append((x,y))
"""
for x in range(w):
  for y in range(h):
    freq[dist(pxl[x,y], pxl[fit(x, y),y])].append((x,y))

mx = max(freq.keys())

print(mx)

def normalize(x):
  return min(max(1, round(255*x/mx)), 255)

"""

cpy = [
  [pxl[x,y] for y in range(h)]
  for x in range(w)
]

for x in range(cycle_len, w):
  for y in range(h):
    pxl[x,y] = tuple(16*abs(x-y) for x,y in zip(pxl[x,y], cpy[x-cycle_len][y]))[:3] + (255,)

img.save("diff.png")

diff_cpy = [
  [pxl[x,y][:3] for y in range(h)]
  for x in range(w)
]

diff_pxls_rows=list(zip(*diff_cpy))

combined = []
for r, ro in enumerate(zip(*cpy)):
  if r > 26: break
  for i, (R, G, B, A) in enumerate(ro):
    bits = [
      (G >> 1) % 2,
      (R >> 2) % 2,
      (R >> 1) % 2,
      B % 2,
    ]
    if r == 0 and i < 20: print(i, f"| R = {bin(R)}, G = {bin(G)}, B = {bin(B)} |", bits)
    combined.extend(bits)


combined_bytes = []
for i, ls in enumerate(chunked(combined, 8, strict=True)):
  sm = 0
  for b in ls:
    sm *= 2
    sm += b
  if i < 10:
    print(i, ''.join(map(str,ls)), f"{sm:02x}")
  combined_bytes.append(sm)

open("combined.bin", 'wb').write(bytes(combined_bytes))
