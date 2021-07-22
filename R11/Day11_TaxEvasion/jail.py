#!/usr/bin/env -S python3 -u

import sys

def audit(name, args):
	if name not in ["exec", "compile", "builtins.input", "builtins.input/result"]:
		print("you did a bad thing")
		print("stay in jail forever")
		exit(0)

# the same, except prints debug info and has exit changed...
def debug_audit(name, args):
	print(name, args)
	if name not in ["exec", "compile", "builtins.input", "builtins.input/result"]:
		print("you did a bad thing")
		print("stay in jail forever")

sys.addaudithook(debug_audit)

def jail():
	while True:
		try:
			code = input(">>> ")
			exec(code)
		except Exception as e:
			print("Error occurred")
			exit(0)
jail()
