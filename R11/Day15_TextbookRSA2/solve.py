
from pwn import *
from base import *

prog = remote("oreos.imaginaryctf.org", 6789)

def intAfter(msg):
	prog.recvuntil(msg)
	return int(prog.recvline())

prog.sendline(b"1")				# get the encrypted flag

flag_enc = intAfter(b"message: ")
e 			 = intAfter(b"e = ")
n 			 = intAfter(b"n = ")

two_enc = pow(2,e,n)

double_flag_enc = (flag_enc * two_enc) % n
prog.sendline(f"3\n{double_flag_enc}")		# decrypt twice flag

double_flag = intAfter(b"message is ")
prog.close()

print(i2b(double_flag // 2, 'big').decode())
# ictf{y0u_m@d3_+!mmy_cry_y0u_3v!1_h@ck3r}
