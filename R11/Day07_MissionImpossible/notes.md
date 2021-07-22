
This was a delightful challenge.

Of course, the challenge isn't meant to be the hardest, but it did make a point:
don't run binaries you don't trust, and maybe you shouldn't trust CTFs.

The idea is that, if you're like me and used to just running and debugging a binary
before even doing rudimentary static analysis or containing it in a virtual machine,
you'll soon find that the binary overwrites itself and becomes unusable.

Of course, it's not so hard to redownload it, and afterwards I made sure to keep a copy 
of the binary that I didn't run.

<br>

Anyways, the actual challenge is a simple rev, you can do some static analysis 
(e.g, with Ghidra), and find the function `zzzAVerySecretMessage` that prints the flag
one character at a time. The reason it does this is so you can't _literally_ just run
`strings` on it and get the flag.

Or, you can go my route, and use GDB to abuse the binary during runtime to print the flag 
for you. Follow the input in `gdb.in` and output in `out_commentary` to see how you can find all the
info you need to be able to do this challenge.

