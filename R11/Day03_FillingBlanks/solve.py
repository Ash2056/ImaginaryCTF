from pwn import *
from ctypes import CDLL, c_int

exe = ELF('./predict', checksec=False)
libc = CDLL('libc.so.6')

# p = process(exe.path)
p = remote('20.94.210.205', 1337)

constants = [libc.rand() for i in range(4)]

p.recvuntil('flag: \n')

seed = libc.time(0) // 10
libc.srand(seed)

for i in range(4):
	random = libc.rand()
	constants[i] = c_int(constants[i] * (random % 1000))

constants = [i.value for i in constants]

guess = c_int(sum(constants)).value

p.sendline(str(guess))
print(p.recv().decode().strip())

# ictf{exp3r1menting_w1th_ch@lleng3_f0rmat$_f0r_$c1ence}
