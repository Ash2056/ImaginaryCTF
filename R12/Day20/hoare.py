
from random import shuffle

def X(ls):
  ls = list(ls)
  shuffle(ls)
  print(f"{ls = }")
  return ls

def highlight(A, *idxs):
  s = set(idxs)
  # print(s)
  print(', '.join(f"[{x}]" if i in s else str(x) for i, x in enumerate(A)))

def quicksort(A):
  def rec(lo=0,hi=len(A)):
    if 1 < hi - lo:
      p = part(lo,hi)
      highlight(A, p)
      assert max(A[:p]) <= min(A[p:])
  def part(lo,hi):
    pivot = A[(lo + hi)//2]
    print(f"{pivot = }")
    i = lo-1
    j = hi
    while True:
        i += 1
        while A[i] < pivot: i += 1
        j -= 1
        while pivot < A[j]: j -= 1
        highlight(A, i, j)
        if i < j:
          A[i], A[j] = A[j], A[i]
        else:
          return i
  rec()

from itertools import permutations
# for ls in permutations([0,1,2]):
#   print()
#   print(list(ls))
#   quicksort(list(ls))
