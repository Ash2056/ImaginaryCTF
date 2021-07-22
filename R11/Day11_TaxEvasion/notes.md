
This is the kind of thing where it's hard to think of on the spot, but once you see the answer, 
it's obvious in hindsight.

The first important thing to do: debug, debug, debug! <br>
Run the script manually, remove the `exit` so it doesn't always crash.
Print the `name` and `args` that the `audithook` takes as arguments, to see what it is working
with internally.

Then, play around with it and see what you can do.

The first thing I tried was removing the `audit` function, possibly by editing its code through 
`audit.__code__`. Turns out getting an object's attribute is banned.

Can we unset the `audit` function, with something silly like `audit=lambda *_: None`? <br>
Turns out the answer is yes, but because of how references work, audit events still refer to the
original `audit`.

Can we unset `exit`? <br>
Turns out the answer to this is yes, and that it also turns the event handler into mush! <br>
We still get messages that things are banned, but never really get kicked out.
We can do anything we want from here! Pick your poison:
```python
exit=int
import os
os.listdir()
print(open("flag.txt").read())
os.system("cat *")
os.system("/bin/sh")
```

And so we get the flag: `ictf{i11_t@x_th3_stre3t_t@x_y0ur_s3@t_t@x_th3_he@t_+ax_y0ur_f33t}`
