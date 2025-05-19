# sat_solver.py
"""
A minimal DPLL SAT solver.

Representation
--------------
• Literals  : signed ints  ( 3 ≙  x3,   -3 ≙ ¬x3 )
• Clause    : list[int]
• CNF       : list[list[int]]

Public API
----------
solve_sat(clauses, assignment=None)  → dict | None
    clauses     : CNF formula
    assignment  : optional partial assignment {var: bool}

Returns a total satisfying assignment or None if unsatisfiable.
"""

from __future__ import annotations
from typing import List, Dict, Optional

Literal    = int
Clause     = List[Literal]
CNF        = List[Clause]
Assignment = Dict[int, bool]


# ──────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ──────────────────────────────────────────────────────────────────────────────
def _lit_true(lit: Literal, assign: Assignment) -> bool:
    """Is the literal already satisfied by the current assignment?"""
    val = assign.get(abs(lit))
    return (val is True and lit > 0) or (val is False and lit < 0)


def _simplify(clauses: CNF, lit: Literal) -> CNF:
    """
    Return a *new* CNF after setting `lit` to True:
      • drop all clauses containing  lit
      • remove ¬lit from remaining clauses
    """
    new_cnf: CNF = []
    for clause in clauses:
        if lit in clause:                  # satisfied
            continue
        if -lit in clause:
            new_clause = [x for x in clause if x != -lit]
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clause[:])
    return new_cnf


# ──────────────────────────────────────────────────────────────────────────────
# Core DPLL solver
# ──────────────────────────────────────────────────────────────────────────────
def solve_sat(clauses: CNF,
              assignment: Optional[Assignment] = None) -> Optional[Assignment]:
    """
    Deterministic DPLL with unit-propagation.

    Returns a satisfying assignment extending the given partial one,
    or None if the formula is unsatisfiable.
    """
    assignment = {} if assignment is None else dict(assignment)

    # ――――――――――――――――――――― Unit propagation ――――――――――――――――――――― #
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            # Clause already satisfied?
            if any(_lit_true(l, assignment) for l in clause):
                continue

            unassigned = [l for l in clause if abs(l) not in assignment]
            if not unassigned:             # all literals false ⇒ conflict
                return None
            if len(unassigned) == 1:       # unit clause ⇒ force it
                forced = unassigned[0]
                assignment[abs(forced)] = forced > 0
                clauses = _simplify(clauses, forced)
                changed = True
                break                      # restart loop with new CNF

    # ――――――――――――――――――――― All clauses satisfied? ――――――――――――――――― #
    if not clauses:                        # CNF empty ⇒ satisfied
        return assignment

    # ―――――――――――――――― Choose next variable deterministically ――――――――― #
    vars_in_cnf = sorted({abs(l) for c in clauses for l in c})   # **deterministic order**
    var = next(v for v in vars_in_cnf if v not in assignment)

    # ―――――――――――――――――――― Branch: True first, then False ――――――――――――― #
    for value in (True, False):
        new_assign = assignment.copy()
        new_assign[var] = value
        result = solve_sat(_simplify(clauses, var if value else -var), new_assign)
        if result is not None:
            return result

    return None   # both branches failed
