"""Explicit constructions for triangulation packings and coverings.

Let the convex n-gon have vertices on a circle.
"""

from __future__ import annotations

from .core import is_diagonal


def key(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def fan_triangulation(cycle: list[int], start: int, m: int) -> frozenset[tuple[int, int]]:
    """The fan triangulation of the (m+1)-gon on vertices cycle[start..start+m],
    umbelled at the second vertex cycle[start+1].  'cycle' must have length 2*m
    (even double-fan context) or -1 for wrapping arithmetic mod the cycle length."""
    n_cyc = len(cycle)
    center = cycle[(start + 1) % n_cyc]
    diags = set()
    for k in range(3, m + 1):
        j_idx = (start + k) % n_cyc
        diags.add(key(center, cycle[j_idx]))
    return frozenset(diags)


def double_fan_decomposition(cycle: list[int]) -> list[frozenset[tuple[int, int]]]:
    """Partition the diagonals of the convex 2m-gon on the cyclic vertex sequence
    'cycle' into m triangulations.

    Piece T_i (i = 0..m-1) consists of:
      * the diameter  {cycle[i], cycle[i+m]},
      * the fan of one half  cycle[i..i+m]   umbelled at cycle[i+1],
      * the fan of the other half cycle[i+m..i+2m] umbelled at cycle[i+m+1].
    """
    n_cyc = len(cycle)
    assert n_cyc % 2 == 0
    m = n_cyc // 2
    pieces = []
    for i in range(m):
        d = key(cycle[i], cycle[(i + m) % n_cyc])
        H1 = fan_triangulation(cycle, i, m)
        H2 = fan_triangulation(cycle, (i + m) % n_cyc, m)
        T = set(H1) | set(H2) | {d}
        pieces.append(frozenset(T))
    return pieces


def odd_packing(m: int) -> list[frozenset[tuple[int, int]]]:
    """Packing of m pairwise diagonal-disjoint triangulations of the convex
    (2m+1)-gon with vertices 0..2m.

    Construction: use the double-fan packing of the 2m-gon on vertices 1..2m,
    then, for the piece T_i we add the single diagonal {0, c_i}, where c_i is the
    apex of the T_i-face sitting on the boundary edge {2m, 1} of the even polygon.
    Distinctness of the c_i implies the added diagonals are distinct, so the
    pieces remain pairwise disjoint.  Each piece gains exactly one diagonal,
    reaching the required 2(m+1)-3 = 2m-2 diagonals for a (2m+1)-gon.
    """
    even_cycle = list(range(1, 2 * m + 1))
    even_pieces = double_fan_decomposition(even_cycle)
    out = []
    for T in even_pieces:
        c = _apex_on_even_edge(T, (2 * m, 1), even_cycle)
        T_new = set(T)
        T_new.add(key(0, c))
        out.append(frozenset(T_new))
    return out


def fan_at_vertex(n: int, v: int) -> frozenset[tuple[int, int]]:
    """The fan triangulation of the convex n-gon on vertices 0..n-1 at vertex v:
    all diagonals incident to v."""
    out = set()
    for u in range(n):
        d = key(v, u)
        if d[0] != d[1] and d[1] - d[0] > 1 and d != (0, n - 1) and is_diagonal(d, n):
            out.add(d)
    return frozenset(out)


def odd_covering(m: int) -> list[frozenset[tuple[int, int]]]:
    """Covering of the diagonals of the convex (2m+1)-gon (vertices 0..2m) by m+1
    triangulations.

    Construction: take the double-fan decomposition of the even 2m-gon on vertices
    1..2m, adjoin {2m, 1} (a diagonal of the odd polygon) to every one of its pieces
    -- that stays non-crossing, since {2m, 1} is a hull edge of the even polygon --
    and add one extra piece, the fan at vertex 0, which covers all diagonals
    incident to 0.
    """
    n = 2 * m + 1
    even_cycle = list(range(1, 2 * m + 1))
    even_pieces = double_fan_decomposition(even_cycle)
    pieces = [frozenset(set(T) | {key(2 * m, 1)}) for T in even_pieces]
    pieces.append(fan_at_vertex(n, 0))
    return pieces


def _apex_on_even_edge(T: frozenset[tuple[int, int]], edge: tuple[int, int], cycle: list[int]) -> int:
    """Apex of the triangle on boundary edge `edge` of a triangulation T of the
    even polygon whose cyclic vertex order is given by `cycle`.

    An auxiliary segment {u, v} is an edge of the even polygon iff u and v are
    cyclically adjacent in `cycle`; it is a chord already in T iff {u, v} in T.
    """
    u, v = edge
    n = len(cycle)
    adj = {}
    for i in range(n):
        a, b = cycle[i], cycle[(i + 1) % n]
        adj[tuple(sorted((a, b)))] = True

    def on_edge(e: tuple[int, int]) -> bool:
        return e in T or tuple(sorted(e)) in adj

    for c in cycle:
        if c in (u, v):
            continue
        uc, vc = tuple(sorted((u, c))), tuple(sorted((v, c)))
        if on_edge(uc) and on_edge(vc):
            return c
    raise ValueError("no apex found")


