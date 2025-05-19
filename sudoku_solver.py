# sudoku_solver.py
"""
Sudoku → SAT encoder + solver for standard 9×9 puzzles.

The encoding uses the classic “exactly-one” constraints:

Variable numbering
------------------
v(r, c, d)  := 81·(r-1) + 9·(c-1) + d,    with 1 ≤ r,c,d ≤ 9
    r … row, c … column, d … digit

Exactly-one constraints are decomposed into
    (i)  at-least-one  – one long clause  (x1 ∨ … ∨ x9)
    (ii) at-most-one   – pairwise negatives (¬xi ∨ ¬xj)  for i<j
"""

from __future__ import annotations
from typing import List
import sat_solver

# Types
Grid = List[List[int]]
CNF  = List[List[int]]


# --------------------------------------------------------------------------- #
# Helper: variable numbering
# --------------------------------------------------------------------------- #
def _var(r: int, c: int, d: int) -> int:
    """1-based row/col/digit → unique positive integer variable id."""
    return 81 * (r - 1) + 9 * (c - 1) + d


# --------------------------------------------------------------------------- #
# Encoding helpers
# --------------------------------------------------------------------------- #
def _exactly_one(lits: List[int], cnf: CNF) -> None:
    """Add 'exactly one of the literals is true' to CNF."""
    # 1) at least one
    cnf.append(lits)
    # 2) at most one  (pairwise)
    for i in range(len(lits)):
        for j in range(i + 1, len(lits)):
            cnf.append([-lits[i], -lits[j]])


def sudoku_encode(grid: Grid) -> CNF:
    """Return CNF encoding of the given 9×9 Sudoku grid."""
    cnf: CNF = []

    # ------------------------------------------------------------ #
    # (A) Cell constraints – each cell contains exactly one digit
    # ------------------------------------------------------------ #
    for r in range(1, 10):
        for c in range(1, 10):
            lits = [_var(r, c, d) for d in range(1, 10)]
            _exactly_one(lits, cnf)

    # ------------------------------------------------------------ #
    # (B) Row constraints – each digit appears exactly once per row
    # ------------------------------------------------------------ #
    for r in range(1, 10):
        for d in range(1, 10):
            lits = [_var(r, c, d) for c in range(1, 10)]
            _exactly_one(lits, cnf)

    # ------------------------------------------------------------ #
    # (C) Column constraints – each digit appears exactly once/col
    # ------------------------------------------------------------ #
    for c in range(1, 10):
        for d in range(1, 10):
            lits = [_var(r, c, d) for r in range(1, 10)]
            _exactly_one(lits, cnf)

    # ------------------------------------------------------------ #
    # (D) Block constraints – each digit appears exactly once/block
    # ------------------------------------------------------------ #
    for br in range(0, 3):
        for bc in range(0, 3):
            for d in range(1, 10):
                lits = [
                    _var(r, c, d)
                    for r in range(br * 3 + 1, br * 3 + 4)
                    for c in range(bc * 3 + 1, bc * 3 + 4)
                ]
                _exactly_one(lits, cnf)

    # ------------------------------------------------------------ #
    # (E) Pre-filled cells → unit clauses
    # ------------------------------------------------------------ #
    for r in range(1, 10):
        for c in range(1, 10):
            val = grid[r - 1][c - 1]
            if val != 0:
                cnf.append([_var(r, c, val)])

    return cnf


# --------------------------------------------------------------------------- #
# Public solver
# --------------------------------------------------------------------------- #
def solve_sudoku(grid: Grid) -> Grid | None:
    """
    Solve the given 9×9 Sudoku.

    grid –  list[list[int]] with 0 for empty cells
    Returns a fully solved grid or None if unsatisfiable.
    """
    cnf = sudoku_encode(grid)
    model = sat_solver.solve_sat(cnf)

    if model is None:
        return None

    # Build solved grid from model
    solution = [[0] * 9 for _ in range(9)]
    for r in range(1, 10):
        for c in range(1, 10):
            for d in range(1, 10):
                if model.get(_var(r, c, d), False):
                    solution[r - 1][c - 1] = d
                    break

    return solution
