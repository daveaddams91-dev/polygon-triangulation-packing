"""polygon_packings: exact extremal values for packing/covering triangulations
of a convex polygon, with verified constructive proofs."""

from .core import (
    all_diagonals,
    cross,
    is_diagonal,
    is_triangulation,
    triangulations,
    apex_on_boundary_edge,
)
from .constructions import (
    double_fan_decomposition,
    fan_at_vertex,
    fan_triangulation,
    odd_covering,
    odd_packing,
)
from .exhaustive import (
    max_pack_exact,
    min_cover_exact,
    random_greedy_pack,
)

__all__ = [
    "all_diagonals",
    "cross",
    "is_diagonal",
    "is_triangulation",
    "triangulations",
    "apex_on_boundary_edge",
    "double_fan_decomposition",
    "fan_at_vertex",
    "fan_triangulation",
    "odd_covering",
    "odd_packing",
    "max_pack_exact",
    "min_cover_exact",
    "random_greedy_pack",
]

__version__ = "1.0.0"
