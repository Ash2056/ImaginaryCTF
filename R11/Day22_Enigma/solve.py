from collections import defaultdict, Counter

alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
d = defaultdict(list)

for ln in open("output.txt").readlines():
	for i,c in enumerate(ln.strip()):
		d[i].append(c)

d = { k: Counter(v) for k,v in d.items() }
# for k,v in d.items(): print(f"{k:2}: {v}")
for k,v in d.items(): print(f"{k:2}: {alphabet - v.keys()}")

print(''.join(''.join(v.keys() if len(v) == 1 else alphabet - v.keys()) for v in d.values()))
