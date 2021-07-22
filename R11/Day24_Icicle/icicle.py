#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
import time

MEMSIZE = 2**16
REGNAMES = ["r%d"%i for i in range(16)]+['rip']
DEBUG = 0

def prd(*args):
	if DEBUG:
		print(*args)

class MemoryException(Exception):
	pass


# noinspection DuplicatedCode
class Memory:
	def __init__(self, size=MEMSIZE, mem=None, rnames=REGNAMES):
		if mem is not None:
			self.size = mem.size
			self.regs = {k:mem.regs[k] for k in mem.regs}
			self.ram = {k:mem.ram[k] for k in mem.ram}
			self.regs['rip'] = 0
		else:
			self.size = size
			self.regs = {r:0 for r in rnames}
			self.ram = {}

	def setRam(self, addr, val):
		if type(addr) != int:
			raise MemoryException("Attempting to access invalid memory address "+str(addr))
		if addr < 0 or addr >= self.size:
			raise MemoryException("Memory "+str(addr)+" out of bounds!")
		self.ram[addr] = val

	def getRam(self, addr):
		if type(addr) != int:
			raise MemoryException("Attempting to access invalid memory address "+str(addr))
		if addr < 0 or addr >= self.size:
			raise MemoryException("Memory "+str(addr)+" out of bounds!")
		if addr in self.ram:
			return self.ram[addr]
		self.ram[addr] = 0
		return 0

	def getVal(self, val):
		if type(val) != str or len(val) == 0:
			raise MemoryException("Bad value "+str(val)+" recieved!")
		if val.isdigit():
			return int(val)
		if val in self.regs:
			return self.regs[val]
		if val[0] == '[' and val[-1] == ']':
			return self.getRam(self.getVal(val[1:-1]))
		if val[0] == '"' and val[-1] == '"':
			return val[1:-1]
		if val[0] == "'" and val[-1] == "'":
			return val[1:-1]
		raise MemoryException("Bad value "+str(val)+" recieved!")

	def assign(self, loc, val):
		if type(loc) != str or len(loc) == 0:
			raise MemoryException("Bad location "+str(loc)+" recieved!")
		if loc in self.regs:
			self.regs[loc] = val
			return
		if loc[0] == '[' and loc[-1] == ']':
			self.setRam(self.getVal(loc[1:-1]), val)

	def rip(self):
		return self.regs['rip']

	def inc_rip(self):
		self.regs['rip'] += 1


# noinspection DuplicatedCode
class VM:
	def __init__(self, program='', memory=None):
		self.program = self.parseStr(program)
		if memory is not None:
			self.mem = Memory(mem=memory)
		else:
			self.mem = Memory(size=MEMSIZE)

		self.insns_map = {"add": self.add,
											"sub": self.sub,
											"mult": self.mult,
											"div": self.div,
											"mod": self.mod,
											"xor": self.xor,
											"and": self.andd,
											"or": self.orr,
											"rev": self.rev,
											"mov": self.mov,
											"strint": self.strint,
											"intstr": self.intstr,
											"pr": self.pr,
											"readstr": self.readstr,
											"readint": self.readint,
											"j": self.jump,
											"jnz": self.jnz,
											"jz": self.jz,
											"jl": self.jl,
											} # also labels

	def quit(self, msg='', exitcode=1, test=False):
		if exitcode != 0:
			print("Error running line '", self.c_insn(), "' at insn pointer", self.mem.rip())
		if msg == '':
			print("Quitting...")
		else:
			print(msg)
		exit(exitcode)

	def parseStr(self, s):
		return [line.strip() for line in s.split('\n')]

	def parseInsn(self, insn):
		args = insn.split("#")[0].strip().split(" ")
		cmd = args[0]
		rest = " ".join(args[1:]).strip().split(", ")
		return [cmd]+rest

	def c_insn(self):
		return self.program[self.mem.rip()]

	def run(self):
		try:
			while self.mem.rip() < len(self.program):
				prd("Executing '"+self.c_insn()+"' at insn_pointer "+str(self.mem.rip()))
				self.execute_insn(self.c_insn())
				self.mem.inc_rip()
		except MemoryException as e:
			self.quit(str(e))
		except Exception as e:
			print("Unknown error occurred.")
			if DEBUG:
				raise e
			self.quit()

	def execute_insn(self, insn):
		if insn == '' or insn[-1] == ':' or insn[0] == "#":
			return
		args = self.parseInsn(insn)
		prd(args)
		self.insns_map[args[0]](*args[1:])

	def setRam(self, addr, val):
		return self.mem.setRam(addr, val)

	def getRam(self, addr):
		return self.mem.getRam(addr)

	def getVal(self, val):
		return self.mem.getVal(val)

	def assign(self, loc, val):
		return self.mem.assign(loc, val)

	def reset(self):
		self.mem = Memory()

	def add(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != type(a2):
			a1 = str(a1)
			a2 = str(a2)
		self.assign(args[0], a1+a2)

	def sub(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != int or type(a2) != int:
			self.quit("sub args not int!")
		self.assign(args[0], a1-a2)

	def mult(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) == str or type(a2) == str:
			self.quit("Both mult args are strings!")
		self.assign(args[0], a1*a2)

	def div(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != int or type(a2) != int:
			self.quit("div args not int!")
		self.assign(args[0], a1//a2)

	def mod(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != int or type(a2) != int:
			self.quit("mod args not int!")
		self.assign(args[0], a1%a2)

	def andd(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != int or type(a2) != int:
			self.quit("and args not int!")
		self.assign(args[0], a1&a2)

	def orr(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) != int or type(a2) != int:
			self.quit("or args not int!")
		self.assign(args[0], a1|a2)

	def xor(self, *args):
		a1 = self.getVal(args[1])
		a2 = self.getVal(args[2])
		if type(a1) == int and type(a2) == int:
			self.assign(args[0], a1^a2)
		else:
			a1 = long_to_bytes(a1).decode() if type(a1) == int else a1
			a2 = long_to_bytes(a2).decode() if type(a2) == int else a2
			self.assign(args[0], self.xorstr(a1, a2))

	def xorstr(self, s1, s2):
		l = max(len(s1), len(s2))
		s1 = s1.encode()
		s2 = s2.encode()
		ret = ''
		for i in range(l):
			ret += chr(s1[i%len(s1)]^s2[i%len(s2)])
		return ret

	def readint(self, *args):
		try:
			self.assign(args[0], int(input()))
		except ValueError as e:
			self.quit("Bad int input!")

	def readstr(self, *args):
		self.assign(args[0], input())

	def pr(self, *args):
		print(self.getVal(args[0]), flush=True)

	def strint(self, *args):
		a1 = self.getVal(args[1])
		if type(a1) != str:
			self.quit("Attempting to convert non-string to int!")
		self.assign(args[0], bytes_to_long(bytes([ord(i) for i in a1])))

	def intstr(self, *args):
		a1 = self.getVal(args[1])
		if type(a1) != int:
			self.quit("Attempting to convert non-int to string!")
		try:
			b = bytes.fromhex(hex(a1)[2:])
		except ValueError as e:
			if 'non-hexadecimal' not in str(e):
				raise e
			b = bytes.fromhex('0'+hex(a1)[2:])
		self.assign(args[0], ''.join([chr(i) for i in b]))

	def revint(self, i):
		sign = 0 if not i else (1 if i>0 else -1)
		return sign*int(str(abs(i))[::-1])

	def rev(self, *args):
		a1 = self.getVal(args[1])
		if type(a1) == int:
			ret = self.revint(a1)
		else:
			ret = a1[::-1]
		self.assign(args[0], ret)

	def mov(self, *args):
		self.assign(args[0], self.getVal(args[1]))

	def jump(self, *args):
		for i, insn in enumerate(self.program):
			if insn == args[0]+':':
				print(f"Jumping to {args[0]:10}, {self.getVal('rip')} -> {i}")
				if args[0] == "recurse": print(f"args: r12 = {long_to_bytes(self.getVal('r12'))}, r1 = {self.getVal('r1')}, [r2] = {self.getVal('[r2]')})")
				self.assign('rip', i)
				return
		self.quit("Could not find label "+args[0]+"!")

	def jz(self, *args):
		if self.getVal(args[0]) == 0:
			self.jump(args[1])

	def jnz(self, *args):
		if self.getVal(args[0]) != 0:
			self.jump(args[1])

	def jl(self, *args):
		if self.getVal(args[0]) < self.getVal(args[1]):
			self.jump(args[2])

"""
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("Usage: ./icicle.py [filename]")

    with open(sys.argv[1], 'r') as f:
        vm = VM(program=f.read())
        vm.run()
"""

prog = """


mov r15, 65535

mov r1, 1
mov r2, 4

read:
    pr "Enter a valid password: "
    readstr [r1]
    strint [r1], [r1]
    jl [r1], 1329227995784915872903807060280344576, short
    add r1, r1, 1
    jl r1, r2, read

sub r1, [1], [2]
jz r1, same
sub r1, [2], [3]
jz r1, same
sub r1, [3], [1]
jz r1, same

mov r1, 1

validateloop:
    mov r12, [r1]
    xor [r2], [r2], [r2]
    add r14, rip, 1
    j validate
    jnz r13, invalid
    add r1, r1, 1
    jl r1, r2, validateloop

j flag

validate:
    jnz r12, recurse
    mov r13, r12
    mov rip, r14

    recurse:
    mov [r15], r14
    sub r15, r15, 1
    mov [r15], r1
    sub r15, r15, 1

    mod r1, r12, 256
    xor [r2], [r2], r1
    jz [r2], invalid
    mov [r2], r1
    div r12, r12, 256
    intstr r12, r12
    rev r12, r12
    strint r12, r12
    mod r3, r12, 256
    div r12, r12, 256
    xor r1, r1, r3
    add r14, rip, 1
    j validate
    add r13, r13, r1

    add r15, r15, 1
    mov r1, [r15]
    add r15, r15, 1
    mov r14, [r15]
    mov rip, r14

short:
    pr "Password too short!"
    j end

invalid:
    pr "Invalid password!"
    j end

same:
    pr "Password was reused!"
    j end

flag:
    pr "[FLAG REDACTED]"

end:

"""


VM(prog).run()
