
Time to actually dig into the implementation.

First, 
[view](https://github.com/python/cpython/blob/2c2055884420f22afb4d2045bbdab7aa1394cb63/Modules/_randommodule.c)
the official implementation of the Mersenne Twister in CPython.

Another good reference: 
[jame's blog](https://jazzy.id.au/2010/09/25/cracking_random_number_generators_part_4.html)
(Love the shoutout to Scala!)


Here's the relevant code:

```cpp
/* generates a random number on [0,0xffffffff]-interval */
static uint32_t
genrand_uint32(RandomObject *self)
{
    uint32_t y;
    static const uint32_t mag01[2] = {0x0U, MATRIX_A};
    /* mag01[x] = x * MATRIX_A  for x=0,1 */
    uint32_t *mt;

    mt = self->state;
    if (self->index >= N) { /* generate N words at one time */
        int kk;

        for (kk=0;kk<N-M;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        for (;kk<N-1;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1U];

        self->index = 0;
    }

    y = mt[self->index++];
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680U;
    y ^= (y << 15) & 0xefc60000U;
    y ^= (y >> 18);
    return y;
}
```

Here, we can see there are 2 steps.

One of the steps is that, when `self->index` goes past `N = 624`, the function
has to do a buttload of computation and manage the entire `mt` matrix.

The next step, the easier one, is that `mt[index]` gets obfuscated a little by some 
bit operations, and then returned.

We can build a lookup table for that second step.

Just kidding! That results in memory errors. Time to reverse it manually.

<br>

Let's think about the `y ^= y >> 11` first.

Let's imagine the case, instead, where we do a right shift by `b`, and the bitlength of `y` is `3 * b`.

Let `y = ABC`, where `A, B, C` represent `b`-length bits that are concatenated.

Then, this is what the operation does:
```
y = ABC
y >> b = 0AB

  y ^ (y >> b) 
   ABC
   0AB
-^-----
   AXY
```

We get some obfuscated result `AXY`, where `X = A^B` and `Y = B^C`. 
Note that `Y = B^C` is different from and has nothing to do with `y = ABC`.

So, let's start reversing this! First, we can recover `A` easily. 
We can also recover `B` like so: `X ^ A = B`. This gives us the following idea:
compute `AXY ^ (AXY >> b)`

```
   AXY
   0AX
-^-----
   ABZ
```

Now, `Z = X ^ Y = A ^ B ^ B ^ C = A ^ C`. If we repeat the same operation as above,
we can recover `C` too.

```
   ABZ
   00A
-^-----
   ABC
```

Nice!

Let's try the same approach with left shifts!
Assume that `ABC0 & PQR = ST0`.

```
y = ABC
y << b = ABC0
ABC0 & PQR = ST0

   ABC
   ST0
-^----
   XYC
```

This time, we know exactly what `C` is.

Note that `Y = (C & Q) ^ B`, <br>
and that  `X = (B & P) ^ A`.

We can... deal with the bitshifts manually this time.
Figure out each block, one at a time, until we've found all the blocks.

<br>

Next, we have to figure out the state transitions:
```java
int y = (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7fffffff);
int next = y >>> 1;
if ((y & 1L) == 1L) {
  next ^= 0x9908b0df;
}
next ^= state[(i + 397) % 624];
```

By doing a bit of analysis on the missing states and the states that were duplicated, <br>
we find that we're missing states `[18, 28)` and we have duplicates of `[244, 254)`.

Coincidentally, `(245 + 397) % 624 == 18`, where `397` and `624` are both magic numbers
from the code above...

<br>

This gives us the idea:

We have an initial state at `245`, and we have a next state at `245`.
We know that the computation of the next state uses the state at `245`,
the state at `246`, and the state at `245 + 397 = 18`.

so, `state2[245] = f(state[245], state[246], state[18])`, where `f` is a function that produces
the next state.

We have all of `state2[245], state[245], state[246]`. We need to compute `state[18]`.

We can see in the code above that there's some computation of `state[245]` and `state[246]`,
and as a final step, XORs the result with `state[18]` to get `state2[245]`.

Implement the initial computation, and `xor` it with `state2[245]` to get `state[18]`.

Do this for all the numbers.

---

I spent at least 3 hours debugging the next step. I was wondering why my solution worked with 
python's built in `random`, but not with the challenge. 

Guess what? I forgot to use `outMersenne` on my predicted values to get bytes for the flag.

Don't do this. I recommend getting to know the `ictf` flag prefix well, such as what it looks like
in base64, what it looks like under `ret47` or `rot13`, what it looks like as a big endian or little endian
integer, and last but not least, what it looks like under `inpMersenne`.

Had I known what the output of `SET_ENDIANNESS('big'); i2b(inpMersenne(b2i(b"ictf")))` looked
like from the start, I would have immediately recognized that I already had the flag.

---

But anyways, after you apply `outMersenne` to all of the integers, 
you get the flag: `ictf{St4t3_i+397_is_7rivi4lly_c0mpu73d}`
