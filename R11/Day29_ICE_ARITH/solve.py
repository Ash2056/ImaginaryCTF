import functools
import itertools

from base import *
from base64 import *
from do_some_arithmetic import *
import math

y = 9257825281186994975293932225990833333687004701533041690893578004875012711244886832004664412138708079254358907748659670419915357506323370316768863626850043786144714349529420781165360784389627239094471108717969601480504187189675332752827981538694283153653075213866043724080241155405714354611903526255079114717811381719657361225775384363748895646036749766507587969956468622743172486566730304707583502226227652077703329513949960220612856998165177572993790285132028855364336845769648987023636525322290194530177657101831789571626927172221706977300366596353503462291237401117034656070435634830893419347456516171315816093159
r = 46678938637090657018250559235516670444375598094628565149005284271211692545267
s = 60972123778932439205204267477612028396779511498418172692249834569998646364918

"""

Do look at the `computations.png` to get an idea of how the verification works.

In the last step, we can see that we have a relationship between two secret variables, `k` and our `flag`.

I spent 4 hours trying to find any second relationship to have 2 equations with 2 unknowns. 
It was not possible, as far as I know.

Then, A~Z leaked a hint on discord: 
> A~Z — Today at 5:46 PM
> Also don't make stupid assumptions that something or the other has been chosen in a secure way because it could very well have not been

Clearly, `g2` was a variable that was never used (it's used in the calculation of another secret, `k`,
but then, why wasn't `k` generated by `random`?), and so `g2` was the vulnerability or a major red herring.

Turns out it was the vulnerability, and in an obvious way. 
g2 ^ 10794  ==  1   mod q, 
which means we can brute force g2 ^ i for all 1 <= i <= 10794.

"""

w = pow(s, -1, q)
u1 = (H(m) * w) % q
u2 = (r * w) % q
v0 = ((pow(g, u1, p) * pow(y, u2, p)) % p) % p
v = v0 % q
Hm = H(m)

def k_buster():
	for i in range(1, 10794):
		k = pow(g2, i, q)
		flag = i2b(((k - u1) * pow(u2, -1, q)) % q, 'big')
		if flag_bre.match(flag): return print(flag.decode())

# just like brute forcing website directories!
k_buster()

# ictf{unsafe_nonces_strike_again}
