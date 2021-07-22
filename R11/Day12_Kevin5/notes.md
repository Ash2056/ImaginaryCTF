
This one isn't that bad, as long as you read the question and don't miss a share!

First of all, run it through 
[Aperi'Solve](https://aperisolve.fr/7bf579bb7015c1c9416f97cedac5f377).

You'll immediately get 3 flags for free. It might be tempting to submit these, but if we read the
challenge description carefully, these aren't for submission; rather, they're numbers that are 
used for a [decryption algorithm](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing).

If you actually open the image, you'll find there's another flag sitting in plain sight:
`ictf{29106484658943023}`.

And finally, reading the bottom of the image, we see there's a hint about 
[IHDR chunks](https://en.wikipedia.org/wiki/Portable_Network_Graphics#Critical_chunks).
Reading up on this a little, we can guess what we need to edit on the png file.

Taking a look at the hexdump of the raw png,
```
00000000  89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52  |.PNG........IHDR|
00000010 [00 00 03 e8|00 00 02 bc]08 06 00 00 00 7c cb 95  |...è...¼.....|Ë.|
00000020  b1 00 00 00 21 74 45 58 74 43 6f 70 79 72 69 67  |±...!tEXtCopyrig|
```

I've surrounded the bytes of interest with square brackets. 
The left group of 4 bytes controls the width, and the right group of 4 bytes controls the height.

It seems we're missing some data off the bottom, <br> 
so I tried increasing the length to `00 00 03 bc`, and taking a look again. <br>
Here, we find a 
[pastebin link](https://chl.li/kevin5)
to a fifth share: `ictf{29106484896478680}`

Finally, it seems like we need to find an associated index to each share, to run it through
the wikipedia algorithm correcty.

Reading the challenge description, we can see that the author is keen on mentioning the dragons'
names, which are numbers in japanese. In case you're not a weeb, 
the numbers are in parentheses after.

We can see that the IHDR flag is labelled 4. 

We found a 5th flag, and going by the name of the challenge, `Kevin5`, we can guess its index is 5.

Zipping our flags with the correct indices and tossing them into the wikipedia algorithm gives us
our flag contents, `gh1dr@h`. <br>
Wrapping it correctly, we can submit the flag `ictf{gh1dr@h}`.
