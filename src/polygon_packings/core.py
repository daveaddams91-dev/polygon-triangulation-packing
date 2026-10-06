"""Core concepts: triangulations of a convex n-gon, triangulaton packings/coverings.

Conventions
-----------
Vertices of the convex n-gon are 0,1,...,n-1 in clockwise order.
A *diagonal* is a pair {a,b} of non-adjacent vertices, always stored
as a sorted tuple (a, b) with a < b and (a, b) != (0, n-1).
A *triangulation* is a set of exactly n-3 pairwise non-crossing diagonals.
"""

from __future__ import annotations

from itertools import combinations
import functools



def all_diagonals(n: int) -> list[tuple[int, int]]:
    """All diagonals of the convex n-gon with vertices 0..n-1."""
    out = []
    for a in range(n):
        for b in range(a + 2, n):
            if (a, b) == (0, n - 1):
                continue
            out.append((a, b))
    return out


def cross(d1: tuple[int, int], d2: tuple[int, int]) -> bool:
    """True if diagonals d1, d2 cross strictly (proper interleaving)."""
    a, b = d1
    c, d = d2
    return (a < c < b < d) or (c < a < d < b)


def is_diagonal(d: tuple[int, int], n: int) -> bool:
    """Is diagonal.
    
    Args:
        d:
        n:
    
    Returns:
        bool: Result of type bool
    
    """
    a, b = d
    if not (0 <= a < b < n):
        return False
    if b - a == 1:
        return False
    if (a, b) == (0, n - 1):
        return False
    return True


def is_triangulation(T: set[tuple[int, int]], n: int) -> bool:
    """A triangulation of the convex n-gon: n-3 diagonals, pairwise non-crossing."""
    if len(T) != n - 3:
        return False
    for d in T:
        if not is_diagonal(d, n):
            return False
    for d1, d2 in combinations(sorted(T), 2):
        if cross(d1, d2):
            return False
    return True


@functools.lru_cache(maxsize=None)
def triangulations(n: int) -> list[frozenset[tuple[int, int]]]:
    """All triangulations of the convex n-gon as sets of diagonals (base marked 0,n-1)."""
    if n == 3:
        return [frozenset()]
    out: list[frozenset[tuple[int, int]]] = []
    for k in range(1, n - 1):
        left = triangulations(k + 1) if k + 1 >= 3 else [frozenset()]
        right = triangulations(n - k) if n - k >= 3 else [frozenset()]
        for L in left:
            for R in right:
                Rs = frozenset((a + k, b + k) for (a, b) in R)
                T = set(L) | Rs
                if k != 1:
                    T.add(tuple(sorted((0, k))))
                if k != n - 2:
                    T.add(tuple(sorted((k, n - 1))))
                out.append(frozenset(T))
    return list(set(out))


def apex_on_boundary_edge(T: frozenset[tuple[int, int]] | set[tuple[int, int]],
                          n: int, edge: tuple[int, int]) -> int:
    """The apex vertex c of the unique triangle (u, v, c) of the triangulation T that
    contains the boundary edge edge=(u,v).  u,v must be adjacent on the n-gon (cyclically)."""
    u, v = edge
    assert is_triangulation(set(T), n), "T must be a triangulation"

    def on_edge(e) -> bool:
        """On edge.
        
        Args:
            e:
        
        Returns:
            The computed result
        
        """
        a, b = e
        return (e in T) or (b - a == 1) or (a, b) == (0, n - 1)

    for c in range(n):
        if c in (u, v):
            continue
        uc = tuple(sorted((u, c)))
        vc = tuple(sorted((v, c)))
        if on_edge(uc) and on_edge(vc):
            return c
    raise ValueError("no triangle found on edge")
