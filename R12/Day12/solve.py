
from base import *
from R12.Day12.icicle import *

SET_ENDIANNESS('big')
print(b2i(b'''readf r1, "flag.txt"
pr r1'''))

try:
  test = VM("""
  exec 183827312370185651168152020034418275188078876928815084123222577
  """)

  test.run()

  print()
  print(test.mem.ram)
except: pass