
My first approach was to rev the math to actually be able to undo the "cryptography".

But then I saw TheBadGod did the challenge in 9 minutes.

<br>

###### It was time for brute force.

<br>

---

The idea behind the brute force is simple.

The initial key is an integer inside `range(10**7, 10**8)`.

From the very first `out += bytes([c ^ (key&0xff)])`, we can see that the `i` in `ictf{`
is xored with the least significant byte of the key.

We can work our way backwards: the first byte in the output is `0xe6`. The first byte in the flag
is `i = 0x69`. This means the first byte of the key is the xor, i.e, `0xe6 ^ 0x69 = 0x8f`.

We can start our search with the first number after `10**7` that has `0x8f` as the least significant byte.
This is exactly `new_start`. Also, each time we move to the next key, we add `0x100` to make sure 
we don't change the least significant byte.

Next, we only decode the first 5 bytes of the flag using a possible key, and we check if it's what
we're expecting: `ictf{`. If it's not, move on to the next key. 

If it is, then it must be the flag. Print the entire flag: <br>
`ictf{f0r_l00p5_r1ght_th3r3_4nd_3v3ryWh3r3}`
