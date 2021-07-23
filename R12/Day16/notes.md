
The first giveaway is `(?=...)`: this is what's called a `positive lookahead` in regular expressions.

I've seen this kind of challenge before, specifically, in 
[ångstromCTF](https://ctftime.org/task/15339).

Related but not quite: [Advent of Code](https://adventofcode.com/2020/day/19).

The idea is that the given regular expression is a list of positive lookaheads that, when combined,
match _only_ the flag, and just about nothing else.

Time to start revving the ~~regrets~~ regexes!

```regexp
^ictf{
01. (?=.*4.0.*R.*G.*)
02. (?=.*(?=\d\D{6}\d.+\d{2}\D\d.$))
03. (?=[^}]{42}5}$)
04. (?=.+\Dn0\D(?:.*[A-Z][2-8][A-Z]){1,}.*\D4r.[^_]+$)
05. (?=.*u.{5}u.+ss[n0-5]+})
06. (?=(?=[NC0-9]{3}\W).*(?=[ale].._[n-x301]{10}.{2}$))
07. (?=[^689ABDEFH-MO-QS-Z]{43})
08. (?=(?:[^_]+_){6}[^_]+})
09. (?=[A-Z4]+'[b-w_0-7]+\+[l-xG_R0-5]+.$)
10. (?=[C3P0]+4[NSA].[7of9]_.+_[um]+[abc][help](?:_[^_]{5}.*){3}})
11. (?=.+\w\w\dw(?:_\d_).*(?=.3[r4-9_xp]{3}3\w{2}[15][40].{2}}))
12. (?=.+\D2.[mango][rum][hooch]+\w\d.{13}\dxp[^_xp]{9})
13. (?=.{5}_[ak47].*\db\d.+\+_[D-Z3]{3}[BuMP69][l4ser]{3,6})
.*}$
```

Note that I added newlines and numbering for readability.

```regexp
(?=[^689ABDEFH-MO-QS-Z]{43})
```

This one is one of the most helpful: it lets us remove some of the numbers and capital letters
from the flag. Specifically, the only numbers used throughout are `[0-57]`, and the only
capital letters used throughout are `[CGNR]`.

We can cut down some of our rules using this:

```regexp
^ictf{
01. (?=.*4.0.*R.*G.*)
02. (?=.*(?=\d\D{6}\d.+\d{2}\D\d.$))
03. (?=[^}]{42}5}$)
04. (?=.+\Dn0\D(?:.*[CGNR][2-57][CGNR]){1,}.*\D4r.[^_]+$)
05. (?=.*u.{5}u.+ss[n0-5]+})
06. (?=(?=[NC0-9]{3}\W).*(?=[ale].._[n-x301]{10}.{2}$))
08. (?=(?:[^_]+_){6}[^_]+})
09. (?=[CGNR4]+'[b-w_0-7]+\+[l-xG_R0-5]+.$)
10. (?=[C30]+4N.[7of]_.+_[um]+[abc][help](?:_[^_]{5}.*){3}})
11. (?=.+\w\w\dw(?:_\d_).*(?=.3[r4-9_xp]{3}3\w{2}[15][40].{2}}))
12. (?=.+\D2.[mango][rum][hooch]+\w\d.{13}\dxp[^_xp]{9})
13. (?=.{5}_[ak47].*\db\d.+\+_[GNR3]{3}u[l4ser]{3,6})
.*}$
```

Using rule 03, we can get a foothold on our flag:

```
ictf{..........................................5}
```

Using the rule 06, and counting backwards by 10, we can continue:

```
ictf{..............................._..........5}
```

From using the tail of rule 06 and rule 11, we can find some info on the last 4 characters: <br>
Rule 06 gives us `[n-x301]{10}.{2}`,
rule 11 gives us `[15][40].{2}`, <br>
the intersection gives us `10.s`.

```
ictf{..............................._.......10.5}
```

Rule 11 gives us more information if we count backward a little bit:

```
ictf{..............................._3...3..10.5}
```

Let's revisit our regular expressions and simplify them, knowing what we do now.

```regexp
^ictf{
01. (?=.*4.0.*R.*G.*)
02. (?=.*(?=\d\D{6}\d.+10\D5}$))
04. (?=.+\Dn0\D(?:.*[CGNR][2-57][CGNR])+.*\D4r.[^_]+$)
05. (?=.*u.{5}u.+ss[n0-5]+})
06. (?=(?=[NC0-57]{3}\W).*(?=[ale].._3[n-x301]{7}10.5$))
08. (?=(?:[^_]+_){6}[^_]+})
09. (?=[CGNR4]+'[b-w_0-7]+\+[l-xG_R0-5]+}$)
10. (?=[C30]+4N.[7of]_.+_[um]+[abc][help](?:_[^_]{5}.*){3}})
11. (?=.+\w\w\dw(?:_\d_).*(?=.3[r457_xp]{3}3\w{2}10.5}))
12. (?=.+\D2.[mango][rum][hooch]+\w\d.{13}\dxp[^_xp]{9})
13. (?=.{5}_[ak47].*\db\d.+\+_[GNR3]{3}u[l4ser]{3,6})
.*}$
```

Using rule 05, since `ss` can't fit inside `10.5`, it must be the case that `[n0-5]+` matches `10.5`.

Specifically, by rule 02, we know that `.` must be `n`.

```
ictf{..............................._3...3..10n5}
```

Finally, converting some leetspeak to normal letters, we can guess/brute force the entire last word
using rule 11:
```shell
$ grep -iE '^e[r457ast_xp]{3}e..ions$' words.txt
expressions
ictf{..............................._3xpr3ss10n5}
```

Now that we know the entire last word, we can use rule 04:

```
ictf{.............................4r_3xpr3ss10n5}
```

Rule 06 practically confirms that this is the word "regular" in leetspeak. 
Makes sense, this is a challenge about regular expressions.

```
ictf{............................l4r_3xpr3ss10n5}
```

Finally, rule 13 seems to fit _too_ nicely. Let's just guess that it does fit. <br>
This confirms the `u` in `ul4r`. Furthermore, the three letters previous must be from `[GNR3]`. <br>
It's probably exactly `R3Gul4r`. Rule 13 also gives us a `+_` prefix.

```
ictf{......................+_R3Gul4r_3xpr3ss10n5}
```

Switch tactics for a bit and work on the beginning.

First, our usual simplification stage:

```regexp
^ictf{
01. (?=.*4.0.*R.*G.*)
02. (?=.*\d\D{6}\d.+10n5}$)
04. (?=.+\Dn0\D(?:.*[CGNR][2-57][CGNR])+.*l4r_3xpr3ss10n5$)
05. (?=.*u.{5}u.+ss10n5})
06. (?=[NC0-57]{3}\W.*l4r_3xpr3ss10n5)
08. (?=(?:[^_]+_){5}R3Gul4r_3xpr3ss10n5})
09. (?=[CGNR4]+'[b-w_0-7]+\+_R3Gul4r_3xpr3ss10n5}$)
10. (?=[C30]+4N.[7of]_.+_[um]+[abc][help](?:_[^_]{5}.*){2}_3xpr3ss10n5})
11. (?=.+\w\w\dw_\d_.*_3xpr3ss10n5)
12. (?=.+\D2.[mango][rum][hooch]+\w\d.{9}l4r_3xpr3ss10n5})
13. (?=.{5}_[ak47].*\db\d.+\+_R3Gul4r)
.*}$
```

Let's start! <br>
Once again, rule 13 proves invaluable: it sets an easy underscore into place.
Combining 09 and 10 confirms our first `.+` letters must be `C`.

```
ictf{C...._................+_R3Gul4r_3xpr3ss10n5}
```

Then, rule 10 gives us the next couple letters: `4N`. <br>
Rule 06 and 09 confirm that we have a single quote after, too.

```
ictf{C4N'._................+_R3Gul4r_3xpr3ss10n5}
```

Guess the next letter completes the word "can't", so it must be `7` from rule 10's `[7of]`.

```
ictf{C4N'7_................+_R3Gul4r_3xpr3ss10n5}
```

I did the next part through a bunch of guessing too. <br>
There's a `\Dn0\D` in rule 04, there's a `\w\w\dw` in rule 11, and there's a `k` in `[ak47]` 
(especially obvious after removing the `[47]` using `\D` and the `[a]` using rule 09).

The next entire word is probably `kn0w`. Fill in the stuff after with rule 11.

```
ictf{C4N'7_kn0w_._.........+_R3Gul4r_3xpr3ss10n5}
```

Rule 11 also tells us the `.` in `_._` is a `\d`.

Let's simplify all the regular expressions with what we learned / guessed.

```regexp
^ictf{
01. (?=.*4.0.*R.*G.*)
02. (?=.*\d\D{6}\d.+10n5}$)
04. (?=.+kn0w(?:.*[CGNR][2-57][CGNR])+.*l4r_3xpr3ss10n5$)
05. (?=.*u.{5}u.+ss10n5})
08. (?=C4N'7_kn0w_\d_(?:[^_]+_){2}R3Gul4r_3xpr3ss10n5})
09. (?=C4N'[b-w_0-7]+\+_R3Gul4r_3xpr3ss10n5}$)
10. (?=C4N'7_.+_[um]+[abc][help](?:_[^_]{5}.*){2}_3xpr3ss10n5})
11. (?=.+kn0w_\d_.*_3xpr3ss10n5)
12. (?=.+\D2.[mango][rum][hoc]+\w\d.{3}\+_R3Gul4r_3xpr3ss10n5})
13. (?=C4N'7_k.*\db\d.+\+_R3Gul4r)
.*}$
```

Rule 12 seems like the only thing that could even give us a hint about the single digit word. <br>
It's probably `2`.

```
ictf{C4N'7_kn0w_2_.........+_R3Gul4r_3xpr3ss10n5}
```

Then by rule 12, the next word must match `[mango][rum][hoc]+`. <br>
By Rule 10, if there are two words in between the `_[um]+[abc][help]_` and `_3xpr3ss10n5`, <br>
then `[um]+[abc][help]` must match the same word as rule 12.

Brute forcing the search thru grep, we get:

```shell
$ egrep '^[mango][rum][hooch]+' words.txt | egrep '^[um]+[abc][help]$'
much
ictf{C4N'7_kn0w_2_much_....+_R3Gul4r_3xpr3ss10n5}
```

Since the `\w` in rule 12 is `_`, then the next word must start with a `\d`. <br> 
Rule 01 and 13 combine to probably give us `4b0.+`, and rule 05 confirms the `u`. <br>

We get the flag:
```
ictf{C4N'7_kn0w_2_much_4b0u+_R3Gul4r_3xpr3ss10n5}
```
