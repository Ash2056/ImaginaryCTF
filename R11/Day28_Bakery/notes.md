From the challenge description:
> but robots are banned from the bakery.

Check `robots.txt`, and find: 
```
User-agent: *
Disallow: /topsecret/alldiscountcodes.txt
Disallow: /secret_menu.html
```

Check `/topsecret/alldiscountcodes.txt` to find a list of discount codes that updates every 5 seconds.

Check `/secret_menu.html` to find a joyful, elaborate pun on SHA256 hashes, as well the hash of 
a particular value, that also changes every 5 seconds. Putting this through some databases reveals
nothing, even though the text claims that there is "no salt added".

Check the homepage, and find that there's a button that performs a `POST` request
with the value filled in in `discount_code` (and ONLY that value),
and that it takes a `customer_type`.

Trying just a single, or the first few, discount codes as post requests alone don't work.

Changing the request cookie to `baker` or `admin` or `shawn` or `robot` or `xxe robotics` or `partner`
or the hash value or a multitude of other strings seems to have no affect on the response 
[it'll ALWAYS say `invalid discount code :(`].

Finally, open a support ticket, have Robin point out that:
> Robin - Jun 29, 2021 11:28 AM
> > there's only 1 valid code in the list

and immediately understand that the hash is meant to validate exactly one of the discount codes.

Implement that, and get a different error, that mentions discounts can only be applied to the baker.
Re-try setting the cookie to `baker` as above, and get the flag.
