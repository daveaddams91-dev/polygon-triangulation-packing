import itertools
import random

from .core import all_diagonals, cross, is_triangulation, triangulations


def max_pack_exact(n: int) -> tuple[int, list[frozenset]]:
    """Exact maximal number of pairwise diagonal-disjoint triangulations of the
    convex n-gon, by explicit backtracking.  Only feasible for n <= 11."""
    tris = triangulations(n)
    best: int = -1
    bestsol: list[frozenset] = []

    def bt(i, cur, used):
        nonlocal best, bestsol
        if len(cur) + (len(tris) - i) <= best:
            return
        if i == len(tris):
            if len(cur) > best:
                best, bestsol = len(cur), list(cur)
            return
        T = tris[i]
        if T.isdisjoint(used):
            cur.append(T)
            bt(i + 1, cur, used | T)
            cur.pop()
        bt(i + 1, cur, used)

    bt(0, [], frozenset())
    return best, bestsol


def min_cover_exact(n: int) -> int:
    """Exact minimum number of triangulations whose diagonal sets cover every
    diagonal of the n-gon.  Only feasible for n <= 10."""
    tris = triangulations(n)
    need = set(all_diagonals(n))
    best = [None]

    def bt(i, cur, covered):
        if best[0] is not None and len(cur) >= best[0]:
            return
        if covered >= need:
            best[0] = len(cur)
            return
        if i == len(tris):
            return
        T = tris[i]
        c1 = cur + [T]
        bt(i + 1, c1, covered | T)
        bt(i + 1, cur, covered)

    bt(0, [], set())
    return best[0]


def random_greedy_pack(n: int, rng: random.Random, reps: int = 1) -> int:
    """Adversarial sanity check: repeatedly greedily build a triangulation packing
    with randomised tie-breaking; returns the best size seen.  Should never exceed
    floor(n/2) (which is then tight because of the construction)."""
    tris = triangulations(n)
    best = 0
    for _ in range(reps):
        order = tris[:]
        rng.shuffle(order)
        used = set()
        cnt = 0
        for T in order:
            if T.isdisjoint(used):
                used |= T
                cnt += 1
        best = max(best, cnt)
    return best
