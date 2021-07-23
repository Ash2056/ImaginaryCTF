
from itertools import permutations

N = 4
for i,ls in enumerate(permutations(range(1,N+1))):
  open(f"perm{N}_{i}.inp", 'w').write(f"{N}\n" + '\n'.join(map(str,ls)))
