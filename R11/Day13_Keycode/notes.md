
Don't look at `solve.sh` or `gdb.in`, those are attempts at me learning how to use
python in gdb to xor segments of memory together.

The challenge is much easier if you just open it up in Ghidra.

You'll find a `checkFlag` function that `xor`s the user input with the function's bytecode itself, 
and checks if the result is equal to some segment in memory.

Therefore, to rev the flag, you just have to `Copy Special -> Copy bytestrings` the `checkFlag`
function and the `flg` data, then run it through a basic python script to get the flag:
`ictf{wh@t_g00d_i5_@_10ck_!f_th3_l0ck_!s_th3_k3y?}`.
