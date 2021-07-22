import requests as r
from base import flag_re

b = r.post("https://button.max49.repl.co/noflag.htm")
print(*flag_re.findall(b.text))
# ictf{f1ag_1n_th3_c0mm3nts!}
