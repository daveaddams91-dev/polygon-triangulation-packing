"""Experiment E5: produce the figures for the paper.

fig1: the double-fan decomposition of the 10-gon (diagonal packing into m pieces).
fig2: the odd packing of the heptagon, with the two leftover diagonals (the 'wedge').
fig3: diagonal-span profile of every piece of the 10-gon double-fan decomposition,
      illustrating the gap-balance lemma of Section 5.
"""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from polygon_packings import core, constructions  # noqa: E402

FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd",
           "#ff7f0e", "#17becf", "#8c564b", "#e377c2"]


def pos(n, i):
    ang = math.pi / 2 + 2 * math.pi * i / n
    return (math.cos(ang), math.sin(ang))


def draw_polygon(ax, n, lw=1.4):
    for i in range(n):
        p, q = pos(n, i), pos(n, (i + 1) % n)
        ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, zorder=3)
    for i in range(n):
        x, y = pos(n, i)
        ax.text(1.13 * x, 1.13 * y, str(i), ha="center", va="center", fontsize=10)


def draw_diags(ax, n, T, color, lw=1.4, ls="-"):
    for (a, b) in T:
        p, q = pos(n, a), pos(n, b)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=2)


# ---- figure 1: even packing of n=10 ----
n = 10
fig, axes = plt.subplots(1, 5, figsize=(16, 3.4))
pieces = constructions.double_fan_decomposition(list(range(n)))
fig.suptitle(r"Exact diagonal partition into $5$ triangulations of a convex $10$-gon (one piece per panel)", y=1.02)
for k, ax in enumerate(axes):
    draw_polygon(ax, n)
    draw_diags(ax, n, pieces[k], PALETTE[k], lw=2.0)
    ax.set_title(f"$T_{k}$ has {len(pieces[k])} diagonals")
    ax.set_aspect("equal"); ax.axis("off")
fig.savefig(FIG / "even_partition_n10.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# ---- figure 2: odd packing of n=7, leftover wedge ----
n = 7
fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
pack = constructions.odd_packing(3)
covered = set().union(*pack)
leftover = [d for d in core.all_diagonals(n) if d not in covered]
fig.suptitle(r"Odd case: 3 pairwise disjoint triangulations of the 7-gon, leaving the crossing wedge of two diagonals", y=1.02)
for k, ax in enumerate(axes):
    draw_polygon(ax, n)
    draw_diags(ax, n, pack[k], PALETTE[k], lw=2.0)
    draw_diags(ax, n, leftover, "#999999", lw=1.6, ls=(0, (4, 2)))
    ax.set_title(f"piece $T_{k}$")
    ax.set_aspect("equal"); ax.axis("off")
fig.savefig(FIG / "odd_packing_n7.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# ---- figure 3: span profile histogram for n=10 ----
n = 10
m = n // 2
fig, ax = plt.subplots(figsize=(7.2, 4.0))
width = 0.18
for i, T in enumerate(pieces):
    spans = {}
    for (a, b) in T:
        g = min(b - a, n - (b - a))
        spans[g] = spans.get(g, 0) + 1
    xs = sorted(spans)
    ax.bar([x + i * width for x in range(len(xs))], [spans[x] for x in xs],
           width=width, label=f"piece $T_{i}$", color=PALETTE[i])
ax.set_xticks([r + 2 * width for r in range(4)])
ax.set_xticklabels(["2", "3", "4", "5"])
ax.set_xlabel("span $g$ of diagonal (cyclic distance between endpoints)")
ax.set_ylabel("# diagonals in one piece")
ax.set_title(r"Each of the 5 pieces contains exactly two diagonals of span 2,3,4 and one diameter")
ax.legend(ncol=3, fontsize=8)
fig.savefig(FIG / "span_profiles_n10.png", dpi=160, bbox_inches="tight")
plt.close(fig)
print("figures written to", FIG)
