import ast, operator, random, string, sys
from itertools import cycle
from typing import List
from base import *

TRACE = False

loadStrs = []

readstr = lambda: loadStrs.pop() if loadStrs else sys.stdin.buffer.readline()[:-1]
readint = lambda: loadStrs.pop() if loadStrs else int(input())
pr = lambda x: print(as_b(x()).decode(), end="")

def as_b(x):
	if isinstance(x, bytes): return x
	return str(x).encode()

def bytes_to_long(a):
	return int.from_bytes(a, "big")
def long_to_bytes(a):
	return a.to_bytes((a.bit_length() + 7) // 8, "big") or b"\x00"

def equalize(a, b, conv=as_b):
	if type(a) == type(b):
		return a, b
	if not isinstance(a, bytes):
		return conv(a), b
	if not isinstance(b, bytes):
		return a, conv(b)
	return a, b

def safesplit(s, sep=None, n=None):
	def sepstart(x):
		if sep is not None:
			return x.startswith(sep), len(sep)
		y = x
		while y and y[0] in string.whitespace:
			y = y[1:]
		return len(y) != len(x), len(x) - len(y)
	instr = False
	parts = []
	i = 0
	start = 0
	while i < len(s):
		if s[i] == '"':
			instr = not instr
		elif s[i] == '\\' and s[i+1] == '"':
			i += 1
		elif not instr:
			is_sep, L = sepstart(s[i:])
			if is_sep:
				parts.append(s[start:i])
				i += L
				start = i
				if n is not None:
					n -= 1
					if n <= 0:
						break
				continue
		i += 1
	parts.append(s[start:])
	return parts

class Val:
	def __init__(self, vm, arg):
		self.vm = vm
		self.arg = arg
		self.child = None
		if arg.startswith("["):
			assert arg.endswith("]")
			self.child = Val(vm, arg[1:-1])

	def __call__(self):
		if self.arg.startswith("r"):
			return self.vm.regs[self.arg]
		elif self.arg.startswith("["):
			return self.vm.memory[self.child()]
		r = ast.literal_eval(self.arg)
		if not isinstance(r, int): return as_b(r)
		return r

	def store(self, val):
		assert self.arg.startswith("r") or self.arg.startswith("[")
		if self.arg.startswith("r"):
			self.vm.regs[self.arg] = val
		else:
			self.vm.memory[self.child()] = val

	def loc(self):
		if self.arg in self.vm.labels:
			return self.vm.labels[self.arg]
		else:
			return self()

	def __str__(self):
		return self.arg

def wrap(f):
	return lambda self, r, a, b: r.store(f(*equalize(a(), b())))
def cjump(cond):
	def f(self, *args):
		if cond(*args[:-1]):
			self._vm.regs["rip"] = args[-1].loc()
	return f
def store_left_evaled(f):
	return lambda self, r, *args: r.store(f(*[x() for x in args]))

def xor(a, b):
	a, b = equalize(a, b, long_to_bytes)
	if isinstance(a, int):
		return a ^ b
	a, b = sorted([a, b], key=len)
	return bytes(x ^ y for x, y in zip(cycle(a), b))

class Op:
	def __init__(self, vm, op, args):
		self._vm = vm
		self._op = op
		self._args = [Val(vm, arg) for arg in args]

	def __call__(self):
		return getattr(self, f"op_{self._op}")(*self._args)

	def __str__(self):
		return f"{self._op} {', '.join(map(str, self._args))}"

	op_add = wrap(operator.add)
	op_sub = wrap(operator.sub)
	op_mult = wrap(operator.mul)
	op_div = wrap(operator.floordiv)
	op_mod = wrap(operator.mod)
	op_and = wrap(operator.and_)
	op_or = wrap(operator.or_)

	op_xor = store_left_evaled(xor)
	op_rev = store_left_evaled(lambda a: type(a)(as_b(a)[::-1]))
	op_mov = store_left_evaled(lambda a: a)
	op_strint = store_left_evaled(bytes_to_long)
	op_intstr = store_left_evaled(long_to_bytes)

	def op_pr(self, x): pr(x)

	op_readstr = store_left_evaled(readstr)
	op_readint = store_left_evaled(readint)

	op_j = cjump(lambda: True)
	op_jnz = cjump(lambda x: x() != 0)
	op_jz = cjump(lambda x: x() == 0)
	op_jl = cjump(lambda a, b: a() < b())

	op_randbyte = store_left_evaled(lambda: random.randrange(256))
	def op_flag(self, r):
		with open("flag.txt", "rb") as f:
			r.store(f.read())

class VM:
	def __init__(self, instructions: List[Op]):
		self.instructions = instructions
		self.regs = {f"r{i}": 0 for i in range(16)} | {"rip": 0}
		self.memory = [0 for _ in range(1<<16)]
		self.labels = {}

	@classmethod
	def from_file(cls, file):
		res = VM([])
		res._parse(file.readlines())
		return res

	def _parse_line(self, line):
		line = safesplit(line, "#", 1)[0]
		if not line.strip():
			return None
		line = " ".join(safesplit(line.strip()))
		op, args = safesplit(line + " ", " ", 1)
		if line.strip().endswith(":"):
			self.labels[line[:-1]] = len(self.instructions)
			return None
		return Op(self, op, safesplit(args.strip(), ", "))

	def _parse(self, lines):
		for line in lines:
			if (op := self._parse_line(line)) is not None:
				self.instructions.append(op)

	def run(self):
		prev, op = None, None
		while True:
			rip = self.regs["rip"]
			if not 0 <= rip < len(self.instructions):
				break
			prev = op
			op = self.instructions[rip]
			self.regs["rip"] += 1
			s = str(op)
			if TRACE and s.startswith('j') and s != 'j newline':
				print(f"Executing {op}")
				print("\n".join(f"{k}: {v}" for k, v in sorted(self.regs.items())))
				print(self.memory[self.regs["r14"]:self.regs["r14"] + 50]) # Dumping the stack frame :)
				if s == 'jnz r0, _fail_canary':
					print(f' [r15] = [{self.regs["r15"]-1}] = {self.memory[self.regs["r15"]-1]}')
					print('[7331] =', self.memory[7331])
				print(flush=True)
			op()


random.seed(0x31337 + 42)
"""
if __name__ == "__main__":
	if len(sys.argv) > 1:
		f = open(sys.argv[1])
	else:
		f = sys.stdin
	if "TRACE" in sys.argv[2:]:
		TRACE = True
	VM.from_file(f).run()
"""

def run(m=b"\x00", i=0):
	global TRACE, loadStrs, pr
	TRACE = True
	loadStrs = [i, m]
	outs = []
	pr = lambda x: outs.append(as_b(x()).decode())
	vm = VM.from_file(open("exploitme.txt"))
	vm.run()
	print(list(i2b(int(outs[7]), 'big')))
	print('\n'.join(outs))
	print(f"flag fn at {hex(vm.labels['flag'])}")

# my first payload
# run(b"\x01"*4 + b"\x89" + b"\x16" + b"\x01"*40, 217)

def replace(b, i, k): return b[:i] + k + b[i+1:]

run(replace(b"\x01" * 46, 4, b"\x9c"), 238)
