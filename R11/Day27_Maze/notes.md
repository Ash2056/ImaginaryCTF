
This one was fun, and a really impressive concept!

First, explore the different files we got.

There a `maze.py` with a function named `solve` from `solver.py` missing.
Scrolling through the use site, we find a base64 encoded string under a `verbose` check.

Decrypting the string gives us the implementation of a function called `solve(maze)`.
Put it in the expected file, and make sure the callsite is working. <br>
We're half way there!

Finally, we can see that `client.py` is meant to make a connection to the locally running 
server. However, a quick edit can easily make it run against the real thing.

If we scroll down to `if __name__ == "__main__":`, we can see a few calls to `input`, 
probably asking us to manually solve the maze. We can guess that we should wwap these out for 
the given `solve` function, which hopefully produces output in the format they expect.

Running the code works like a charm, and prints the flag: `ictf{W0w!_th3re_4r3_s0_m4ny_w4y5_t0_g37_the_fl4g,_r1ght?}`

