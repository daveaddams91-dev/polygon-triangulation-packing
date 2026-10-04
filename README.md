# Polygon Triangulation Packings and Coverings

An exact extremal theory for packing and covering the diagonals of a convex
polygon by its own triangulations.

## TL;DR

For the convex *n*-gon, let:

- **τ(n)** = maximum number of pairwise **diagonal-disjoint** triangulations; a *packing* number.
- **κ(n)** = minimum number of triangulations whose diagonal-sets **cover** every diagonal; a *covering* number.

Both quantities are determined exactly by a simple counting bound:

```
τ(n) = ⌊n/2⌋,     κ(n) = ⌈n/2⌉    (n ≥ 4).
```

The even case is witnessed by an explicit symmetric "double-fan" decomposition.
The odd case displays a strict packing/covering gap (τ(2m+1) = m < m+1 = κ(2m+1)),
so after removing the maximal packing there is a small **crossing wedge** of
leftover diagonals that cannot be absorbed by any single additional triangulation.

Every piece of every optimal packing/covering is a valid triangulation of the
same prescribed outer cycle, i.e., a **maximal outerplanar supergraph of a fixed
Hamiltonian cycle**. Equivalently, the results describe exact decompositions of
the "diagonal graph" K_n − C_n into maximal outerplanar graphs on the same vertex
cyclic order.

## Research question

> What fraction of the edges of the complete geometric graph on *n* convexly
> positioned points can be accounted for by maximally many pairwise edge-disjoint
> triangulations drawn on the *same* outer cycle, and what is the matching
> covering number?

## Main theorem

**Theorem.** For every n ≥ 4, τ(n) = ⌊n/2⌋ and κ(n) = ⌈n/2⌉.

- Even n = 2m: the double-fan decomposition partitions all diagonals into m triangulations.
- Odd n = 2m+1: an insertion lemma over the even construction yields m disjoint triangulations, while every diagonal set of size 2m−2 bounds the packings; m+1 triangulations cover all diagonals (even pieces extended by one chord + fan at the new vertex).

## Computational verification

- The count-bound lower bound is matched exactly by the explicit constructions:
  validated to the edge + crossing level for 4 ≤ n ≤ 30 (`experiments/verify_constructions.py`).
- Exact packing numbers match τ(n) = ⌊n/2⌋ by independent exhaustive backtracking for all n ≤ 9.
- Adversarial random greedy searches never produce a better lower bound than ⌊n/2⌋ (`experiments/adversarial_search.py`).
- Randomized search for a packing that beats the proved bound is impossible by the counting bound itself; the enumeration and the table of Catalan growth (`experiments/exact_values.py`) document why the exhaustive era ends around n ≈ 9 (C₈ = 1430 triangulations, C₉ = 4862, C₁₀ = 16796).

## Repository layout

```
src/polygon_packings/      core math + verified constructions + exhaustive search
tests/                     pytest suite (crossing checks, disjointness, cover completeness)
experiments/               verification, adversarial, exact-value, scaling, figures
experiments/results/       committed CSV outputs of all experiments
figures/                   PNG figures (even partition, odd packing wedge, span profiles)
paper/                     LaTeX manuscript (tectonic-compilable)
```

## Reproducing

```bash
pip install -e . 
python -m pytest tests -q
python experiments/verify_constructions.py    # E1
python experiments/adversarial_search.py      # E2
python experiments/exact_values.py            # E3
python experiments/scaling.py                 # E4
python experiments/make_figures.py            # figures
# paper:
tectonic paper/main.tex
```

(Note: on Windows, tectonic may print a harmless Fontconfig warning; the PDF is
still written correctly.)

## Limitations

- The exactness used that maximal pieces are full triangulations; dropping
  maximality changes the problem (book thickness territory).
- Related "pages" parameters of K_n (Bernhart–Kainen 1979) have been re-purposed
  here for triangulations with a prescribed outer cycle.  The numerical results
  coincide at odd-even ceiling levels but the catalogues of extremal systems differ.
- Exhaustive enumeration is feasible only for tiny n; the theoretical construction
  covers everything.

## License

MIT (see LICENSE).
