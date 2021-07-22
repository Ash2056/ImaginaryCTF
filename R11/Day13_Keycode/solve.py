from base import *

# Once again, some easy Ghidra rev

# read data and code as bytes from the program
flag_data = "3c 2b fd 83 33 fe 15 a8 3c d2 62 c1 cf 9b a0 21 bc 1a b0 98 74 cc 63 6b 5f 21 8d 1c ff 2d cf 17 0f e0 2b e0 1a d1 3b 5e a4 67 85 4f e0 76 85 77 1e"
checkFlag_bytecode = "55 48 89 e5 48 89 7d e8 48 8d 05 f1 ff ff ff 48 89 45 f0 c7 45 fc 00 00 00 00 eb 43 8b 45 fc 48 63 d0 48 8b 45 f0 48 01 d0 0f b6 10 8b 45 fc 48 63 c8 48 8b 45 e8 48 01 c8 0f b6 00 89 d1 31 c1 8b 45 fc 48 98 48 8d 15 bf 2e 00 00 0f b6 04 10"

print(xor(bytes.fromhex(flag_data), bytes.fromhex(checkFlag_bytecode)).decode())
# ictf{wh@t_g00d_i5_@_10ck_!f_th3_l0ck_!s_th3_k3y?}
