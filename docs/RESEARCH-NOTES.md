# Research notes: project selection and novelty audit

## Candidates considered

We internally surveyed roughly twenty research directions across enumerative
graph theory, discrete geometry, Ducci-type dynamics, chip-firing, combinatorics
on words, coding theory, positional games, and extremal coloring. The two final
contenders:

1. **Ducci-type dynamics on $\mathbb Z_m^n$** — pairwise near-exact analysis of
   the periods already exists (sequences on $\mathbb Z_m^n$, H-closed Ducci
   sequences, $p$-adic Ducci, and period lower bounds by Breuer–Shparlinski).
   Rejected: the natural modest questions are covered.
2. **Triangulation packings/coverings of a convex polygon under a fixed outer
   cycle** — won.  The small-n brute force immediately matched the counting
   bound, an explicit double-fan family suggested a constructive proof, and
   literature searches surfaced no published exact extremal value for this
   fixed-outer-cycle, maximal piece problem.

Every other surveyed direction failed one of: rediscovered known result,
intractable within a clean theorem, or no natural central question.

## Literature searches used in the novelty audit

- OpenAlex: "edge-disjoint triangulations of a convex polygon",
  "triangulation packing", "maximal outerplanar packing",
  "2-tree packing complete graph", "outerthickness complete graph",
  "decomposition into maximal outerplanar".
- arXiv API: "Ducci sequences over Z_m^n", "triangulation packing",
  "decompose into triangulations", "pairs of disjoint triangulations".
- OEIS web search for packings/decompositions of maximal outerplanar graphs.

No published source states exact $\tau(n)=\lfloor n/2\rfloor$ or
$\kappa(n)=\lceil n/2\rceil$ for maximal outerplanar pieces on a prescribed
outer cycle.  The closest classical parameters are

- book thickness of $K_n$ (Bernhart–Kainen 1979): numerically $\lceil n/2\rceil$,
  but with outerplanar pages along a common Hamiltonian *path*, not saturated by
  a prescribed cycle;
- outerthickness of $K_n$ (Guy–Nowakowski 1990): outerplanar pieces using
  *arbitrary* Hamiltonian cycles.

The research contribution is phrased in the paper as a filling of this gap.

## Falsification agenda

Three adversarial searches were run as committed experiment scripts:

- Exact exhaustive packing for the smallest cases ($n\le 9$), comparing results
  to the asserted formula (`experiments/exact_values.py`).
- Seeded random greedy packing searches: no run has ever exceeded $\lfloor n/2\rfloor$
  (`experiments/adversarial_search.py`).
- Independent chord-by-chord validation of the constructions up to $n=30$,
  testing maximality, disjointness and full coverage piece-by-piece
  (`experiments/verify_constructions.py`).

No invariant violation was ever observed; rules are discussed honestly in the
paper as structural lemmas rather than numerical coincidences.
