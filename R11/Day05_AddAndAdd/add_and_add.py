import random

flag_enc = open("output.txt", 'r').read().strip()

# basically the original function, with some variables abstracted out
def encrypt_flag(flag, init=random.randrange(256)):
	x = bytes([init])
	while flag:
		y = flag[:len(x)]
		flag = flag[len(x):]
		x += bytes([(a + b) % 256 for a, b in zip(x, y)])
	return x[1:].hex()

# with open("output.txt", "w") as f: f.write(encrypt_flag(b"ictf{example}"))

def find_possible_inits():
	inits=[]
	for i in range(256):
		out = encrypt_flag(b"ictf{", i)
		print(out, end='\t')
		if out in flag_enc: inits.append(i)
	print(inits)
	return inits

# Another valid solution: just try all possibilities
# def find_possible_inits(): return range(256)

def solve(out):
	# the flag is encoded in chunks that increase in size by powers of 2
	for j in range(9):
		i = 2 ** j
		# the encoding was adding them together under mod 256;
		# so the inverse is just subtracting under mod 256
		segment = bytes((y-x) % 256 for x,y in zip(out[:i], out[i:2*i]))
		if segment.isascii(): print(segment.decode(), end='')
	print()

for init in find_possible_inits():
	solve([init] + list(bytes.fromhex(flag_enc)))

# ictf{4dd1ng_4nd_casc4d1ng_and_adding_4nd_c4scad1ng}
