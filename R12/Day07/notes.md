
We love a good template string injection challenge :) 

Here's the juicy part of the source:
```python
return render_template_string('{{ flag == "%s" }}'%query, flag=flag)
```

This is a little hard to read if you're like me and never used Python 2 
or its format strings. 

But, the idea is simple: the query paramter is injected into the template at position `%s`, 
and then the string is interpreted and evaluated by `render_template_string`,
and returned back to us.

As usual, I love me some dynamic analysis. So, I copied over all the code, 
simplified it to remove checks that weren't really too relevant, and
ran the code locally so that I can actually _see_ the inputs and exceptions 
that might happen while I build the exploit.

Then came testing.

My first attempt was stupid simple: `/check?flag={flag}`. Needless to say, this didn't work.

Next came the actual ideas. I had to escape the string context, so that means adding an `"`
to the payload. After that, maybe just adding the flag will work?

So I tried `/check?flag="+flag+"`. <br>
But, we get an error: `expected token 'end of print statement', got 'flag'`. <br>
I'm not sure exactly what this means, but I guess `+` has some other meaning 
within `render_template_string`. 

Anyways, if we think about it for a little bit, we might realize this wouldn't work anyways.
The server would do a check, `flag == "" + flag + ""`, and return `True`, and we would have
no additional information.

Part of the problem here is operator precedence: `x + y` is evaluated first before `a == b`.
<br> This means that `"" + flag + ""` is computed _before_ the `==` check.

What are some operators that have low enough precedence that they'll be computed _after_
the `==` check? Also, we have to make sure that such an operator can take a boolean as
its left argument.

There are two that came to mind for me: `,` (the operator that creates a tuple), and ` or `.

Combining what we had above, both of these payloads work: `", flag, "` and `" or flag or "`.

<br>

Just as an exercise, let's step through what the first payload looks like in the code:
```python
query = '", flag, "'
render_template_string('{{ flag == "%s" }}'%query, flag=flag)

# replace the %s with the query                       ==>

render_template_string('{{ flag == "", flag, "" }}', flag=flag)

# evaluate the expression, given the flag variable    ==>

render_template_string('{{ "ictf{the_flag}" == "", "ictf{the_flag}", "" }}')

# simplify                                            ==>

render_template_string('{{ False, "ictf{the_flag}", "" }}')
```

<br>

Finally, working our way through the checks, we need to wrap the payload 
in `ictf{` and `}`, and then also pad the string to a certain length 
(we can find the length through brute force).

Our final exploits are:
1. [puzzler7.imaginaryctf.org:4000/check?flag=ictf{AAAAAA",flag,"}](http://puzzler7.imaginaryctf.org:4000/check?flag=ictf{AAAAAA",flag,"})
2. [puzzler7.imaginaryctf.org:4000/check?flag=ictf{" or flag or "}](http://puzzler7.imaginaryctf.org:4000/check?flag=ictf{%22%20or%20flag%20or%20%22})

