
This challenge proved how important reading documentation correctly is `:)`

Start with the runner code:

```python
  code = input("Enter a line of icicle code: ")
  blacklist = ["read", "write", "flag", "txt", "ictf"]
  for i in blacklist:
    if i in code:
      print("Don't hack me!")
      exit()
  vm = VM(program=code)
  vm.run()
```

My first thought is, it doesn't sound too hard to get `flag.txt` through the blacklist:
we can disguise an argument to an instruction using `intstr` on the appropriate int representation
of `"flag.txt"`.

But, what about the `readf` instruction itself? Surely we can't do the same, since the previous
idea was about turning an `int` into a `string` _argument_, not into runnable code! <br>
And as far as I know, these instructions don't have byte representations of themselves, like
Intel x86 instructions do... <br>
But reading a tiny bit into the new [spec](spec_v3.md), we can find another new instruction: `exec`. <br>
This sounds like exactly what we need!

We can build a payload like so:
```python
from base import SET_ENDIANNESS, b2i
SET_ENDIANNESS('big')
intarg = b2i(b'readf r1, "flag.txt"')
print(intarg)

prog = f"""
intstr [0], {intarg}
exec [0]
pr r1
"""
```

And I tried it on remote, aaaaaaaaand... it didn't work. Apparently, we're only allowed to send one line
of input. <br>
Here I get kinda stumped. I need two instructions, one to turn the int argument into a string,
and another to execute that string. <br>
But at some point, I decide to read through the docs again. And I find that `exec` takes an `int` argument,
and converts it to a string before running! They have blacklist bypass built into the system!

So our final payload looks like:

```python
from base import SET_ENDIANNESS, b2i
SET_ENDIANNESS('big')
intarg = b2i(b'''
readf r1, "flag.txt"
pr r1
''')
print(intarg)

prog = f"exec {intarg}"
```

And we get the flag: `ictf{3x3cut!v3_3x3cu+0r_3x3cut3s_3x3c}`
