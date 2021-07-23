
b = open("chall.iii.enc", 'rb').read()

iii = iter(b[8:])

out = []

try:
  while True:
    acc = ""
    for _ in range(4):
      a, _, c, *_ = [next(iii) for _ in range(6)]
      acc += str(a & 1)
      acc += str((c >> 2) & 1)
    acc = int(acc[::-1],2)
    print(f"here! {acc}")
    assert 0 <= acc <= 128
    out.append(acc)
except Exception as e:
  print(e)

print(bytes(out))
