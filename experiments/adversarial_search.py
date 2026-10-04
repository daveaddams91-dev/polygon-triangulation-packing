"""Experiment E2: adversarial random searches for triangulation packings that
beat the predicted bound floor(n/2).  These are used to try to falsify the
main inequality; combined with the trivial counting bound they confirm tightness."""

import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from polygon_packings.exhaustive import random_greedy_pack  # noqa: E402

rows = []
rng = random.Random(1729)
for n, reps in [(6, 5), (8, 5), (10, 4), (12, 3), (14, 2), (16, 1)]:
    best = random_greedy_pack(n, rng, reps=reps)
    pred = n // 2
    status = "OK (never above bound)" if best <= pred else "WOULD DISPROVE"
    rows.append(dict(n=n, reps=reps, best_random_greedy_packing=best, bound=pred, status=status))
    print(f"n={n:2d}  best_random_packing={best}  predicted_max={pred}  {status}")

out = ROOT / "experiments" / "results" / "adversarial_search.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("wrote", out)
