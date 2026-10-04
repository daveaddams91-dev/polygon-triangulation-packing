"""Experiment E3: table of exact extremal numbers (exhaustively confirmed for
n <= 9) and the triad (n, diagonals, bound) for the general theory."""

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from polygon_packings import core  # noqa: E402
from polygon_packings.exhaustive import max_pack_exact  # noqa: E402

rows = []
for n in range(4, 10):
    t0 = time.time()
    p, _ = max_pack_exact(n)
    dt = time.time() - t0
    rows.append(dict(n=n, diagonals=n * (n - 3) // 2, per_tri=n - 3,
                     tau_exact_bruteforce=p, theorem_formula=n // 2,
                     time_s=round(dt, 3)))
    print(rows[-1])

# expected count of triangulations: Catalan
def catalan(k):
    import math
    return math.comb(2 * k, k) // (k + 1)

for n in range(10, 16):
    rows.append(dict(n=n, diagonals=n * (n - 3) // 2, per_tri=n - 3,
                     tau_exact_bruteforce="--", theorem_formula=n // 2,
                     time_s="--",
                     num_triangulations_catalan=catalan(n - 2)))
    print(rows[-1])

out = ROOT / "experiments" / "results" / "exact_values.csv"
fields = []
for r in rows:
    for k in r:
        if k not in fields:
            fields.append(k)
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print("wrote", out)
