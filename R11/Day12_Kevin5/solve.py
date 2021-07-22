from math import prod
from base import *
import itertools as it
import wiki

ls = [
	29106484421874464,	# z-steg, copyright, Ni's flag
	29106484658943023,	# reading San's flag
	29106484896478680,	# changing IHDR, https://chl.li/kevin5, 4th flag
	29106485134492853,	# z-steg, extradata (5th flag ?! who knows)
]
# I never found the LSB flag my first time...
# I didn't know what it meant, and I didn't know to just toss the png into Aperi'Solve

print("\nBrute force:\n")
for indices in it.combinations(range(1,8), 4):
	l = list(zip(indices, ls))
	# computations from https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
	nums = list(y * prod(x2 for x2,_ in l if x2 != x) for x,y in l)
	dens = list(prod((x2-x) for x2,_ in l if x2 != x) for x,y in l)
	x = sum(n//d for n,d in zip(nums,dens))
	b = i2b(x,'big')
	if b.isascii(): print(indices, ':', b.decode())


# ------------------------------------------------------------------------------------------ #
# 																	The Clean Solution
# ------------------------------------------------------------------------------------------ #

print("\n\nUsing the 5th share, and info about the indices:\n")

ls = [
	(2, 29106484421874464),
	(1, 29106484185261585), # z-steg, LSB, Ichi's flag
	(3, 29106484658943023),
	(4, 29106484896478680),
	(5, 29106485134492853),
]

print(i2b(wiki.recover_secret(ls),'big').decode())
# ictf{gh1dr@h}
