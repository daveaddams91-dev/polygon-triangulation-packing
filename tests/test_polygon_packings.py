import random
import pytest

from src.polygon_packings import core, constructions
from src.polygon_packings.exhaustive import max_pack_exact, random_greedy_pack


class TestCore:
    def test_diag_count(self):
        for n in (3, 4, 5, 8, 12):
            assert len(core.all_diagonals(n)) == n * (n - 3) // 2

    def test_triangle_not_triangulation_too_few(self):
        assert not core.is_triangulation(set(), 4)

    def test_fan_is_triangulation(self):
        for n in (3, 4, 6, 9):
            assert core.is_triangulation(set(constructions.fan_at_vertex(n, 0)), n)

    def test_crossing_predicate(self):
        assert core.cross((0, 4), (1, 3)) is False  # nested, not crossing
        assert core.cross((0, 3), (1, 4)) is True
        assert core.cross((0, 2), (1, 3)) is True
        assert core.cross((0, 3), (3, 5)) is False

    def test_triangulations_count(self):
        counts = {3: 1, 4: 2, 5: 5, 6: 14, 7: 42, 8: 132}
        for n, c in counts.items():
            assert len(core.triangulations(n)) == c

    def test_triangulations_valid(self):
        for n in (4, 6, 8):
            for T in core.triangulations(n):
                assert core.is_triangulation(set(T), n)


class TestEvenDecomposition:
    @pytest.mark.parametrize("m", [2, 3, 4, 6, 9, 12])
    def test_exact_partition(self, m):
        n = 2 * m
        pieces = constructions.double_fan_decomposition(list(range(n)))
        assert len(pieces) == m
        D = set(core.all_diagonals(n))
        covered = set()
        for T in pieces:
            assert core.is_triangulation(set(T), n)
            assert T.isdisjoint(covered)
            covered |= T
        assert covered == D

    @pytest.mark.parametrize("m", [2, 3, 5, 8])
    def test_apex_distinctness(self, m):
        """The triangle apex on the wrap-around edge is different for every piece --
        this is what licenses the insertion lemma in the odd packing."""
        cycle = list(range(1, 2 * m + 1))
        pieces = constructions.double_fan_decomposition(cycle)
        edge = (2 * m, 1)
        apexes = {}
        for T in pieces:
            c = constructions._apex_on_even_edge(T, edge, cycle)
            assert c not in apexes
            apexes[c] = True


class TestOddConstructions:
    @pytest.mark.parametrize("m", [2, 3, 4, 6, 10, 15])
    def test_odd_packing_valid(self, m):
        n = 2 * m + 1
        pack = constructions.odd_packing(m)
        assert len(pack) == m
        used = set()
        for T in pack:
            assert core.is_triangulation(set(T), n)
            assert T.isdisjoint(used)
            used |= T

    @pytest.mark.parametrize("m", [2, 3, 4, 6, 10, 15])
    def test_odd_covering_covers_everything(self, m):
        n = 2 * m + 1
        cov = constructions.odd_covering(m)
        assert len(cov) == m + 1
        covered = set()
        for T in cov:
            assert core.is_triangulation(set(T), n)
            covered |= T
        assert covered == set(core.all_diagonals(n))


class TestExhaustive:
    @pytest.mark.parametrize("n,expect", [(4, 2), (5, 2), (6, 3), (7, 3), (8, 4)])
    def test_max_pack_small_n(self, n, expect):
        best, _ = max_pack_exact(n)
        assert best == expect

    def test_random_greedy_never_beats_bound(self):
        rng = random.Random(2026)
        for n in (6, 8, 10):
            assert random_greedy_pack(n, rng, reps=3) <= n // 2
