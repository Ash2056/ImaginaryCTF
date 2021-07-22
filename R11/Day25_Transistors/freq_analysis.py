from base64 import *
from itertools import *

s = """tpHV4ElUeQ8AbABIRTJJASpISUTMkklpABlzDw91GFAPBXUTHHpfMYyxMSdEeLzritiB1f+2u8y2ttX/trvMtrbV/7a7zLa21f+2u8y2ttX/trvMtrbV/7a76EkKK1UTHksgMcGCy6/MtrbV/7a7zLa21f+2u8y2ttX/trvMtrbV/7a7zLa21f+2u8y2ttX/trvMtrbV/7a7zLa21f+2hDNYQSooSfAwSGsqAlhFMFhI1cRJXDNISCsBSEQzSUkqAElEM0lJKgJKRTe2jSooWUQxS0srA0pHNklJKgBJRDNJSCgRSlYSWnhrIhg1NwsoPjJ6FrK2jSoWSEUySEkqAElEM0lJKgBJRDNJSCj/jUQpWEgrAUlHMklJKgBJRDNJSSoASFUxW2hr/5NEP0pIKgJYRyJJdirxSu4e75vLd3FEJ+huB1I+qEYq2rmKH5UHCUmKChjXfuwgXSRJftGdHYGGOUQZed2FVT3poUlUY7cAHwhVO7frX6w6ThNbdJx3s0g47TniyF5UEVg74fo6+S8glGxfi/wKYybf6uwo62vXUGFeG/MROANKl+HzDgBP/JHsQPXj1ip4gKC0ikIQ5H0psUntvE6Do2fHFNkq+pjCt7PNGR3encHXcq115sRr/F3GLo6D8HiJ8vdkH01a67ubRG0K3+36g+SIpuo9E+vboLW7PcU8Hu/dROFekq6V5PQR2svGZFHCEZw2gOIk8xVjBABxdDCQqQRufdyeWl5oHfH5qdO+BSGbwaPebPC2KqZwIRWwy6XC6xjXtffcVxor1zvb20XbgWybvrWfAA10mGDvJ2IJZlBwgvPCLIx11XnaIKCKbQIUozEBUNdxeNn/nwEE9afKZ/ibuQXYSjBz344SD7f6oFZSg5Cunn6Z/DzYYdNqClSeFvA4IKnaI2TfO9CTpK14cjcXH99iYjT33tY8/qhw5PaEJhzhs3AP3sTh0TY4DZebPFfGRLUN4oA95ZDmWpcGw2fbdkI+Xmbq3dZafgaTL12B+R6921yXiFfnzxHhug/vhi5jX0KFam70DxTbqLjDySugSUQzSUkqAElEM0lJKgBJRDNJSSoASUQytpA="""

xor = lambda a,b: bytes(x^y for x,y in zip(cycle(a),b))
b = b64decode(s)

d = { i: 0 for i in range(256) }
for j in b: d[j] += 1

print(*[f'{x:02x}:{y:4}  | {x^0xff:3x}:{d[x^0xff]:3}' for x,y in islice(d.items(), 128)],sep='\n')

# with open("not_trans.bin",'wb') as f: f.write(xor(b"\xff",b))
key = b"Do you believe in magic?"

def go(key=key):
  for i in range(len(key)):
    print(key, xor(key, b), sep='\n')
    key = key[1:] + key[:1]

def blocks(ls, n, C:type = tuple):
  it = iter(ls)
  return iter(lambda: C(islice(it, n)), C())

print(*blocks(b"\x00"*5 + b, 7, bytes),sep='\n')

"""
> It is a very common circuit pattern with transistors. 
> It sounds like you may also be missing one other hint in the image itself.
What else does "magic" refer to in the context of files?
"""
