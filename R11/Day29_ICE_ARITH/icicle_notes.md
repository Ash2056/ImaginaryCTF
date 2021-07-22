
Once again, it just goes to show you how it's _so, so important_ to be able to debug code
well.

The key to this challenge for me was to extend the `TRACE` to suppress all of the verbose
output that didn't matter, and to focus on the output that did.

For reference, the main body for tracing now looks like this: 

```python
op = self.instructions[rip]
self.regs["rip"] += 1
s = str(op)
if TRACE and s.startswith('j') and s != 'j newline':
    print(f"Executing {op}")
    print("\n".join(f"{k}: {v}" for k, v in sorted(self.regs.items())))
    print(self.memory[self.regs["r14"]:self.regs["r14"] + 50]) # Dumping the stack frame :)
    if s == 'jnz r0, _fail_canary':
        print(f' [r15] = [{self.regs["r15"]-1}] = {self.memory[self.regs["r15"]-1]}')
        print('[7331] =', self.memory[7331])
    print(flush=True)
op()
```

It only prints the context on `jump`-like instructions, except for `j newline` because that
function call doesn't matter. And, on a specific stack canary check, 
(the one I hit first when sending an overflow), it prints the address and value of the canary, 
and the expected value of the canary.

Now come the literal hours of debugging and trying different inputs and seeing what outputs 
we get.

First, we need a buffer overflow. Human-emulated binary search starting with a sizeable initial
string length of `512`, leads us to find that we need to send about `41` bytes of data to get 
an overflow. To leave some buffer for the rest of the exploit, I decided to focus on strings 
of length `46` (it was nice to fix the length of input when debugging).

Then, we need to find how to control the value that gets written to the canary.

I did this entirely by trial and error. I kept searching for the output canary value in my 
input string, but could never find it; soon enough, I realized that maybe it's in the output
number. Turning the number into a list of bytes, we can find the canary value easily as the 
`40`th byte. Do note that the `41`st byte is the return pointer (or so I guessed).

Finally, we have to figure out how the encryption algorithm works, just enough to be able to 
control the `40`th byte with enough trial and error.

Some tests:
```python
run(b"\x01" * 46, 0)
#==> [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 33, 32, 35, 34, 37, 36, 39, 38, {41}, 40, 43, 42, 45, 44, 46]

run(b"\x01" * 46, 1)
#==> [3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 33, 32, 35, 34, 37, 36, 39, 38, 41, 40, {43}, 42, 45, 44, 47, 47]

run(b"\x01" * 46, 130)
#==> [131, 130, 133, 132, 135, 134, 137, 136, 139, 138, 141, 140, 143, 142, 145, 144, 147, 146, 149, 148, 151, 150, 153, 152, 155, 154, 157, 156, 159, 158, 161, 160, 163, 162, 165, 164, 167, 166, 169, 168, {171}, 170, 173, 172, 175, 174, 176]


run(b"\x01" * 46, 250)
#==> [251, 250, 253, 252, 255, 254, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 33, 32, {35}, 34, 37, 36, 39, 38, 40]
```

It seems the key is not much more than an inital offset. Good!
We can set the key so that the canary is correct. Specifically, a key of `(23 - 41) % 256 = 238`
will work well.

```python
run(b"\x01" * 46, 238)
#==> [239, 238, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, {23}, 22, 25, 24, 27, 26, 28]
```

And if we scroll up in the jump trace, we can find that we succesfully passed the original 
stack canary, and probably jumped to about line `22`, the next address after the canary.

Next, we'll try adjusting a single byte of the input, to see what happens.

```python
run(replace(b"\x01" * 46, 7, b"\xff"), 238)
#==> [239, 238, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 235, 20, 23, 22, 25, 24, 27, 26, 28]

run(replace(b"\x01" * 46, 4, b"\xff"), 238)
#==> [239, 238, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 232, 25, 24, 27, 26, 28]
```

We lucked out here. 
(Honestly, it's kind of hard to write a hash function with an avalanche effect in assembly)
But for our case, it seems like changing a single byte of input changes a predictable, single 
byte of output.

By some trial and error, we can find that we need to change the byte at position `4` to `0x9c`.

```python
run(replace(b"\x01" * 46, 4, b"\x9c"), 238)
#==> [239, 238, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 139, 25, 24, 27, 26, 28]
# ictf{an_1C3_c0ld_buff3r_0v3rfl0w}
```
