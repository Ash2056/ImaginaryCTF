#!/usr/bin/python3 -u

from icicle import *

def main():
  code = input("Enter a line of icicle code: ")
  blacklist = ["read", "write", "flag", "txt", "ictf"]
  for i in blacklist:
    if i in code:
      print("Don't hack me!")
      exit()
  vm = VM(program=code)
  vm.run()

if __name__ == '__main__':
  main()
