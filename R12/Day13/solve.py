b = bytes.fromhex("e649fd7458fb36acb341346324635da87427d8d25f5c8b7665b921052727bf730f1c0273d00c23217873")
b5 = b[:5]

start = 10**7
new_start = start+((b[0] ^ b"i"[0]) - (start % 0x100))

def go(key, b=b):
  out = []
  for c in b:
    out.append(c ^ (key&0xff))
    key = key**2 // 1_0000 % 1_0000_0000
  return bytes(out)

for key in range(new_start, 10**8, 0x100):
  if b"ictf{" == go(key, b5): print(go(key).decode())
