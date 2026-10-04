# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-04

### Added
- Formal problem definition for triangulation packings/coverings of the diagonals
  of a convex $n$-gon on a fixed boundary cycle, with invariants $\tau(n)$ and $\kappa(n)$.
- Theorem: $ \tau(n)=\lfloor n/2 \rfloor$ and $\kappa(n)=\lceil n/2 \rceil$, with
  explicit constructions: double-fan family for even $n$, insertion lemma for odd
  packings and an extended-plus-fan covering for odd $n$.
- Verified brute-force confirmation of $\tau(n)$ for all $n \le 9$.
- Automated adversarial searches, scaling checks of the constructive theory, and
  originated validation tensors up to $n=30$.
- LaTeX paper (5 pages) and reproduction-ready scripts `experiments/E1`--`E4`.

