import re, requests, json, itertools as it
from base64 import b64decode as b64d, b64encode as b64e
from dataclasses import dataclass
from typing import Union, List, Optional as Opt, Callable
from datetime import datetime, date
from apikey import apikey

def dump(x, filter: Callable[[str], bool]=None):
	for k in dir(x):
		if not filter or filter(k):
			v = getattr(x, k)
			if callable(v):
				try: v = v()
				except: continue
			print(f"{k:16} | {v}")
	print()
	return x

def dumpPub(x): return dump(x, lambda k: not k.startswith('__'))

ENDIAN='little'
def SET_ENDIANNESS(edn):
	global ENDIAN
	ENDIAN = edn

def b2i(b, edn=None):
	edn = edn or ENDIAN
	return int.from_bytes(b, edn)

def i2b(i: int, edn=None, sz=None):
	edn = edn or ENDIAN
	if sz is not None: return i.to_bytes(sz, edn)
	sz = 0xff
	while True:
		try:
			ret = i.to_bytes(sz, edn)
			return ret.rstrip(b"\x00") if edn == 'little' else ret.lstrip(b"\x00")
		except OverflowError: sz <<= 1

xor = lambda a,b: bytes(x^y for x,y in zip(a,b))
xor_key = lambda a,b: xor(it.cycle(a),b)

flag_re = re.compile("ictf{.+?}", re.A)
flag_bre = re.compile(b"ictf{.+?}")

_BASE_URL = 'https://imaginaryctf.org'
_SUBMIT_ENDPOINT = '/api/flags/submit'
_RELEASED_ENDPOINT = '/api/challenges/released'
_API_KEY = "?apikey=" + apikey
_s = requests.session()
_res: requests.Response = None
_obj: dict = {}


# noinspection PyTypeChecker
class API:
	@dataclass
	class Get:
		__slots__ = ('id', 'title', 'category', 'description', 'attachments', 'author', 'points', 'release_date')
		id: int
		title: str
		category: str
		description: str
		attachments: str
		author: str
		points: int
		release_date: Union[datetime, str]
		def parseDate(self):
			self.release_date = datetime.fromisoformat(self.release_date)
			return self.release_date

	@staticmethod
	def submit(flag: Union[str, bytes, int]) -> dict:
		global _res, _obj
		if type(flag) == int: flag = i2b(flag)
		if type(flag) == bytes: flag = flag.decode()
		if '{ftci' in flag: flag = flag[::-1]
		elif 'ictf{' not in flag:
			try: flag = [x for x in [b64d(flag, validate=True)] if x.isascii()].pop()
			except: pass
		m = flag_re.search(flag)
		if m: flag = m.group()
		else: raise ValueError(f"Decoded {flag=} does not match regex.")
		_res = _s.post(_BASE_URL + _SUBMIT_ENDPOINT + _API_KEY, json={'flag': flag})
		try:
			_obj = json.loads(_res.text)
			print(_obj)
			return _obj
		except: print(_res)
		return _res

	@staticmethod
	def get(day=-1) -> Opt[Get]:
		ret = json.loads(_s.get(_BASE_URL + _RELEASED_ENDPOINT).text)
		ret = API.Get(**ret[((-1 - day) % len(ret))])
		if day == -1 and ret.parseDate().date() != date.today(): return None
		return ret

submit = API.submit