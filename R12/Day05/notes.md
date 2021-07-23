
This round's first "real" challenge :)


There's the easy, 3-minute solve way, and then there's my way.

The 3 minute solve: know that CTF people love 
[dcode.fr](https://www.dcode.fr/vigenere-cipher). <br>
Notice that while the challenge says "caeser", since the key is _cyclic_ and not _constant_, <br>
it's really just a Viginere cipher. Find the cipher on dcode, input the text, and you're done.

<br>

The second way: implement the solver yourself.

First, the challenge flavourtext and the fact that the file being read from is "message.txt" are
both hints: whatever the message is, it's not _exactly_ a flag. We can surmise that it includes
`"ictf"` (to convey which part of the message should be submitted), and from flavourtext, that it
will include the words `"apple"` and `"tart"`. 

Having a crib plaintext is good: we can come up with a key _such that_ the decoded text
contains the crib at a certain index.

In other words, pick an index `i`, find the encoded message at the index (`enc[i:i+4]`), and 
pick the key such that `decode(key)[i:i+4] == "ICTF"`. <br>
You can find the details of this computation in the source for `part1()`.

Finally, you're going to get _thousands_ of outputs, since you need to take into account that 
the key length is anywhere between 5 and 10.

The next part was kind of manual: I looked through the entire `out.txt` for any other recognizable
words. After some trial-and-error with `Ctrl + F`, I found a partially decrypted message
containing both `"TART"` and `"APPL"`.

Although, the word in that decrypted message was `"APPLG"`. This actually gives us some information:
we know it probably should be `"APPLE"`, so we've discovered one more value in our key: after our 
initial key values, we know there should be an `"E" - "G"`.

Finally, we only have 2 key digits left. We can brute force this and search for partial words
we found in previous partial decodes: I was fixated on a `"THOUG"`, so I was personally looking
for `"THOUGHT"` (but it actually ended up being part of `"even though there are"`). <br>
Turns out you can see a large part of `"SUCCESS(FULL)"`, or even search for `"FLAG"` instead.

Finally, looking at `"ICTF"` again, we find the flag: `ictf{MORELIKEVIGENERETART}`.
