from base import b64e
def encode(file):
  try: print(b64e(open(file, 'rb').read()).decode())
  except: pass
encode("cat.txt")
encode("gcd.txt")
# encode("quicksort.txt")
encode("sort14_2.txt")