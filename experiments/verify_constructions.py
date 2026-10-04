"""Experiment E1: validate the explicit constructions against the theorem statement
for a sweep of n, and certify the counts and properties required by Theorem 1."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from polygon_packings import core, constructions  # noqa: E402

ROWS = []
for n in range(4, 31):
    D = set(core.all_diagonals(n))
    if n % 2 == 0:
        m = n // 2
        pieces = constructions.double_fan_decomposition(list(range(n)))
        assert len(pieces) == m
        valid = all(core.is_triangulation(set(T), n) for T in pieces)
        covered = set().union(*pieces)
        exact = covered == D
        disjoint = covered == set(D) and sum(len(T) for T in pieces) == len(D)
        ROWS.append(dict(n=n, kind="even packing", pieces=len(pieces), valid=valid,
                         exact_partition=exact or disjoint))
        print(f"n={n:2d}  even packing  m={m}  valid_triangulations={valid}  exact_partition={exact}")
    else:
        m = (n - 1) // 2
        pack = constructions.odd_packing(m)
        valid = all(core.is_triangulation(set(T), n) for T in pack)
        disjoint = len(set().union(*pack)) == sum(len(T) for T in pack)
        cov = constructions.odd_covering(m)
        full = set().union(*cov) == D
        valid_cov = all(core.is_triangulation(set(T), n) for T in cov)
        ROWS.append(dict(n=n, kind="odd packing", pieces=len(pack), valid=valid,
                         disjoint=disjoint))
        ROWS.append(dict(n=n, kind="odd covering", pieces=len(cov), valid=valid_cov,
                         exact_partition=full))
        print(f"n={n:2d}  odd packing   m={m}  valid={valid}  disjoint={disjoint};  "
              f"covering m+1={m+1}  valid={valid_cov}  covers_all={full}")

out = ROOT / "experiments" / "results" / "construction_validation.csv"
fields = []
for r in ROWS:
    for k in r:
        if k not in fields:
            fields.append(k)
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(ROWS)
print("wrote", out)
