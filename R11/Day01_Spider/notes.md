
First of all, take a look at the `url`.
It's not what I typed in, it got redirected to `/0`.

What does this mean? 
My first instinct is of course to try different numbers, like 2, 3, 4, -1, 
see how large it can go, try some basic sql injection.

And once I was done playing around with that, and getting nowhere, 
I came back to the result of `reqDump()` to see if I missed anything.

Turns out python requests track a history of all the redirects, so I tried looking in there; to no avail.

Finally, coming back to the dump for a third time, I grep'd for 'flag',
and found the `X-Flag` header. 
Noticing that its character was `i`, I wanted to see what the header was set to at `f'{url}/1'`.
Turns out, it's `c`. This pretty much confirms for me that the number gets used as an index for the flag strings.

Writing the small script below takes us through all the indices and gets the flag.
