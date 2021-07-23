
from base import b64d, List
from more_itertools import chunked
from randcrack import RandCrack

with open("password.recovery.mbox") as f:
  ls = f.read().split("\n\n\n")

def p(x): print(x); return x

ls = [int.from_bytes(x, 'big') for i in ls[1:-2] for x in chunked(b64d(i.split()[-1]), 4)]
print([hex(x) for x in ls])

print(len(ls), ls)

rc_even = RandCrack()
rc_odd = RandCrack()
try:
  for x in ls[6:]: rc_even.submit(x)
except: pass
try:
  for x in ls[5:]: rc_odd.submit(x)
except: pass


def out(rc) -> List[int]: return [rc.predict_randrange(0, 4294967296) for _ in range(9)]

print(b"".join(x.to_bytes(4, 'big') for x in out(rc_even)))
print(b"".join(x.to_bytes(4, 'big') for x in out(rc_odd))[4:])

"ictfd1cts3nn_S3t_St4"
"{Pr3_M3r3_Byt1ng8\xc6\xc3" # maybe "te}", to end off the word St4te ?
"ictf{Pr3d1ct_M3rs3nn3_By_S3tt1ng_St4te}"
