
gdb -q mission 2>&1 <gdb.in | tee >out2.txt

# I highly recommend looking at `out_commentary.txt` and learning GDB!

grep -o 'ictf{.*}' out.txt

# ictf{n3v3r_run_@_bin@ry_y0u_d0nt_+ru5t!}
