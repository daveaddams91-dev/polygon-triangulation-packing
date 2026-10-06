"""Experiment E3: table of exact extremal numbers (exhaustively confirmed for
n <= 9) and the triad (n, diagonals, bound) for the general theory."""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from polygon_packings.exhaustive import max_pack_exact  # noqa: E402


def catalan(k: int) -> int:
    """Return the k-th Catalan number."""
    import math
    return math.comb(2 * k, k) // (k + 1)


def main() -> None:
    """Compute exact values and write CSV results."""
    rows: list[dict[str, object]] = []
    for n in range(4, 10):
        t0 = time.time()
        p, _ = max_pack_exact(n)
        dt = time.time() - t0
        row: dict[str, object] = {
            "n": n,
            "diagonals": n * (n - 3) // 2,
            "per_tri": n - 3,
            "tau_exact_bruteforce": p,
            "theorem_formula": n // 2,
            "time_s": round(dt, 3),
        }
        rows.append(row)
        print(row)

    for n in range(10, 16):
        row: dict[str, object] = {
            "n": n,
            "diagonals": n * (n - 3) // 2,
            "per_tri": n - 3,
            "tau_exact_bruteforce": "--",
            "theorem_formula": n // 2,
            "time_s": "--",
            "num_triangulations_catalan": catalan(n - 2),
        }
        rows.append(row)
        print(row)

    out = ROOT / "experiments" / "results" / "exact_values.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Determine field names preserving insertion order (Python 3.7+)
    fields: list[str] = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)

    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("wrote", out)


if __name__ == "__main__":
    main()
