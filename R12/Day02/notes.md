
This one was actually hard, at least, until the hint was released :(

I stared at the attachment for a while, not knowing what to look for.

It seemed like it could possibly be scrambled javascript: one can notice there are some `==`
and `_ ? _ : _` (the ternary operator), multiplication, assignment, numbers, etc.
The only problem was, other people had solved the challenge within seconds,
and there's no way the scrambling of the pseudo-javascript would be that obvious. <br>
Also, it'd be really difficult to hide an entire flag in such a small javascript expression.

Anyways, I tossed it into CyberChef, looking for something like `Base85` maybe,
and at some point I noticed `ROT47` and tried it and got the flag: `ictf{e@sY_chAll3ng3ls_ftw}`.

I still haven't found a tool that automatically solves this. <br>
`CyberChef`'s Magic failed, and something else I tried was `ciphey`, but that failed too.

If you randomly tried something like `bytes(y-x for x,y in zip(b, b"ictf{"))`, that would
have been one way to get close to the answer: 
```python
>>> bytes((y+x)%256 for x,y in zip(b, itertools.cycle(b"/")))
b'ictf{e\x9esY_ch\x9fll\x91ng\x91ls_ftw}'
```

You'd just get some scrambled bytes, but it's definitely bruteforceable.
