
def insertion_sort(ls):
  out = []
  def insert(x, out):
    if out and out[0] < x: return out[:1] + insert(x, out[1:])
    return [x] + out
  for x in ls: out = insert(x, out)
  return out
