from Crypto.Util.number import getPrime, bytes_to_long, inverse
from math import prod, gcd

ps = [getPrime(128) for _ in range(5)]
N1 = prod(ps[:3])
N2 = prod(ps[2:])
e = 0x10001

flag = bytes_to_long(b"ictf{test_flag}")

c1 = pow(flag, e, N1)
c2 = pow(flag, e, N2)

print(f"{N1 = }")
print(f"{N2 = }")
print(f"{c1 = }")
print(f"{c2 = }")

y1 = prod(p-1 for p in ps[:3])
d1 = inverse(e, y1)

p2 = gcd(N1, N2)
