Hello world!

Welcome to my writeups!
Since this is a beginner-friendly CTF competition,
I did my best to go through the challenges and explain my thought process in working through them
in as much detail as I could (at least, for the writeups that I've completed so far).

I hope they make sense, and that you enjoy them!

Once again, I'd like to thank the ICTF Board for making my first (two!) month(s) here so enjoyable :)

<br>

------

<br>

For many of the python solves, you may have to run the script like so:
```shell
user@machine:/path/to/clone/ImaginaryCTF$ python -m R11.Day01_Spider.solve
```
in case the script uses the toplevel `base.py` file.

Sometimes this doesn't work either, because the script uses both `base.py`
and some other files in its own nested directory. 

In these cases, good luck :) I use PyCharm for development and it automagically manages the working directory
in a way that allows me to both import toplevel modules yet open files in the inner directory.
