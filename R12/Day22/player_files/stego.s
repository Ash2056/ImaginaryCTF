main:
pr "Enter iii filename: "
readstr [420]
pr "Enter flag: "
readstr [1337]

intstr r15, 10

rev [1337], [1337]
strint [1337], [1337]

readf [7331], [420]
rev [7331], [7331]
strint [7331], [7331]   # save file as little endian int


mov r1, 8
mov r3, 0
headerloop:
and r2, [7331], 255       # r2 = file[0]
div [7331], [7331], 256   # file = file[1:]
add [9999], [9999], r2    # out = [r2] + out
mult [9999], [9999], 256
add r3, r3, 1             # r3 counter?

jl r3, r1, headerloop     # first 8 bytes are header

encrypt:
and r4, [1337], 255       # r4 = flag[0]
div [1337], [1337], 256   # flag = flag[1:]

mov r6, 4
innerloop:                # run innerloop 4 times
and r5, r4, 1             # r5 = r4 & 0b00000001  ## get bottom bit
div r4, r4, 2             # r4 = r4 >> 1
and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
div r7, r7, 2             # r7 = r7 >> 1
mult r7, r7, 2            # r7 = r7 << 1  ## remove the bottom bit
add r7, r7, r5            # r7 = r7 + r5
add [9999], [9999], r7
mult [9999], [9999], 256  # out = [r7] + out

and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
add [9999], [9999], r7    #
mult [9999], [9999], 256  # out = [r7] + out

and r5, r4, 1             # r5 = r4 & 0b00000001  ## get bottom bit
div r4, r4, 2             # r4 = r4 >> 1
mult r5, 4, r5            # r5 = r5 << 2
and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
and r8, r7, 3             # r8 = r7 & 0b00000011  ## get bottom 2 bits
div r7, r7, 8             # r7 = r7 >> 3
mult r7, r7, 8            # r7 = r7 << 3
add r7, r5, r7            # r7 = r7 + r5
add r7, r8, r7            # r7 = r7 + r8
add [9999], [9999], r7
mult [9999], [9999], 256  # out = [r7] + out

and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
add [9999], [9999], r7
mult [9999], [9999], 256  # out  = [r7] + out

and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
add [9999], [9999], r7
mult [9999], [9999], 256  # out  = [r7] + out

and r7, [7331], 255       # r7 = file[0]
div [7331], [7331], 256   # file = file[1:]
add [9999], [9999], r7
mult [9999], [9999], 256  # out  = [r7] + out


sub r6, r6, 1
jnz r6, innerloop
jnz [1337], encrypt

last:
and r1, [7331], 255
div [7331], [7331], 256
add [9999], [9999], r1
mult [9999], [9999], 256
jnz [7331], last

div [9999], [9999], 256
intstr [9999], [9999]
add [420], [420], ".enc"
writef [9999], [420]
