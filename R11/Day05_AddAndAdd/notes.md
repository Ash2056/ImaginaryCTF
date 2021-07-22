
This one was just a programming challenge.

The idea is that the encryption picks a random byte to start with, in this case, `0xbd = 189`.

Then, add the next byte to the initial to get the first byte of the encrypted flag.

This means it calculates 
```python
bytes([(0xbd + b'i'[0]) % 0xff]) #==> b'&'   # 0x26
```

Next, sum the previous two bytes (`[0xbd, 0x26]`) with the next two bytes `b'ct' == [0x63, 0x74]`
to get `[0x20, 0x9a]`.

One more time: take the previous _four_ bytes, `[0xbd, 0x26, 0x20, 0x9a]`, <br>
with the next 4 bytes from the flag `b'f{??' == [0x66, 0x7b, X1, X2]` <br>
to get `[0x23, 0xa1, Y1, Y2]`.

Taking a look at `output.txt`, we can see that this is exactly the output we got: 
the first 5 bytes are `[0x26, 0x20, 0x9a, 0x23, 0xa1]`, 
which are the first 10 characters of `output.txt`.

In fact, we can use the next 4 characters in `output.txt` to get that `Y1 = 0x54` and `Y2 = 0xfe`.

We know that `(0x20 + X1) % 0xff = Y1 = 0x54`, so `X1 = (Y1 - 0x20) % 0xff`, i.e, `X1 = 0x34 = b'4'`.

Similarly, `X2 = 0xfe - 0x9a = 0x64 = b'd'`. So far, our flag so far is the random byte `0xbd` plus `ictf{4b`.

<br>

This is the entire idea behind `solve`: looking at the encrypted flag in chunks of increasing powers of two,
subtract the first half from the second half to get the decoded second half, and print it.

This gets us the flag: `ictf{4dd1ng_4nd_casc4d1ng_and_adding_4nd_c4scad1ng}`
