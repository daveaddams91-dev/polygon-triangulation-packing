"""Experiment E4: scaling -- verify the constructive theorem for large n and
report the corresponding validation cost; also the growth of their
is_triangulation checks, which is O(n^5) all-pairs over all pieces."""

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from polygon_packings import core, constructions  # noqa: E402

rows = []
for n in [4, 8, 12, 16, 24, 32, 48, 64]:
    t0 = time.time()
    if n % 2 == 0:
        pieces = constructions.double_fan_decomposition(list(range(n)))
        ok = all(core.is_triangulation(set(T), n) for T in pieces)
        covered = set().union(*pieces)
        ok = ok and (covered == set(core.all_diagonals(n)))
        label = f"double-fan packing, {len(pieces)} pieces"
    else:
        m = (n - 1) // 2
        pack = constructions.odd_packing(m)
        ok = all(core.is_triangulation(set(T), n) for T in pack)
        label = f"odd packing, {len(pack)} pieces"
    dt = time.time() - t0
    rows.append(dict(n=n, construction=label, valid_and_exact=ok, wall_time_s=round(dt, 3)))
    print(rows[-1])

out = ROOT / "experiments" / "results" / "scaling.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("wrote", out)
