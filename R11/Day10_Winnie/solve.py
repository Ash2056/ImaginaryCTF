# "Copy special -> bytecode" on Ghidra
bytecode = bytes.fromhex("b9 69 00 00 00 e8 7f 16 00 00 b9 63 00 00 00 e8 75 16 00 00 b9 74 00 00 00 e8 6b 16 00 00 b9 66 00 00 00 e8 61 16 00 00 b9 7b 00 00 00 e8 57 16 00 00 b9 73 00 00 00 e8 4d 16 00 00 b9 31 00 00 00 e8 43 16 00 00 b9 6c 00 00 00 e8 39 16 00 00 b9 6c 00 00 00 e8 2f 16 00 00 b9 79 00 00 00 e8 25 16 00 00 b9 5f 00 00 00 e8 1b 16 00 00 b9 30 00 00 00 e8 11 16 00 00 b9 6c 00 00 00 e8 07 16 00 00 b9 64 00 00 00 e8 fd 15 00 00 b9 5f 00 00 00 e8 f3 15 00 00 b9 62 00 00 00 e8 e9 15 00 00 b9 65 00 00 00 e8 df 15 00 00 b9 61 00 00 00 e8 d5 15 00 00 b9 72 00 00 00 e8 cb 15 00 00 b9 7d 00 00 00 e8 c1 15 00 00")

offset = bytecode.find(b'i')
cycle = bytecode.find(b'c') - offset
assert bytecode.find(b't') == offset + 2 * cycle
assert bytecode.find(b'f') == offset + 3 * cycle

print(bytecode[offset::cycle].decode())
# ictf{s1lly_0ld_bear}
