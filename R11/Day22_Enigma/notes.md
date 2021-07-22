
This entire challenge is an off-by-one error.

If you read `more_hidden.py` carefully, you can find that the key only uses random ints 
from `1` up to `25` (including both endpoints).

But this is fishy: There are only 25 possible values for the `key`, yet there are `26` possible values
for the alphabet. Doing some frequency analysis on the columns leads us (almost) nowhere, except... 
almost every column is missing one letter from the alphabet, namely, the letter from the plaintext.

Putting each of the "missing" characters together gives us the flag: `ICTF{THE_MISSING_MYSTERY}`
