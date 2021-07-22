def sz(x): return (len(x) - 8).to_bytes(4, 'big')

dat = open("How_Long_Is_It.png", 'rb').read()
fst, *rst = dat.split(b"\0"*4)
open("fixed.png", 'wb').write(fst + b"".join(sz(x)+x for x in rst))

# realize I missed the flag

print(b"".join(sz(x).strip(b"\0") for x in rst))
# ictf{R3m3mb3r__Th3r3_1s_N0_L3ngth}
