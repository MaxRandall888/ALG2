import pytest
from sat_solver import solve_sat
from sudoku_solver import solve_sudoku


# ──────────────────────────────────────────────────────────────────────────────
# Part 1: SAT solver tests
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("clauses, assignment, expected", [
    # 1) unsatisfiable
    ([[1, 2], [-1], [-2], [-1, -2]], {}, None),

    # 2) simple two-var example
    ([[1, 2], [-1], [2]], {}, {1: False, 2: True}),

    # 3) all unit clauses
    ([[1], [2], [3], [-4], [-5], [-6]], {},
     {1: True, 2: True, 3: True, 4: False, 5: False, 6: False}),

    # 4) another unsatisfiable example
    ([[1, -2], [-1, 2], [3], [-3, 4], [-4]], {}, None),
])
def test_sat_solver(clauses, assignment, expected):
    result = solve_sat(clauses, assignment)
    assert result == expected


# ──────────────────────────────────────────────────────────────────────────────
# Part 2: Sudoku solver tests
# ──────────────────────────────────────────────────────────────────────────────
# 1) The “easy” sample
easy = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
solution_easy = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

# 2) Single‐row clue
puzzle2 = [
    [0, 0, 0, 0, 0, 1, 2, 0, 3],
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
]
solution2 = [
    [4, 5, 6, 7, 8, 1, 2, 9, 3],
    [1, 2, 3, 4, 5, 9, 6, 7, 8],
    [7, 8, 9, 2, 3, 6, 1, 4, 5],
    [2, 1, 4, 3, 6, 5, 7, 8, 9],
    [3, 6, 5, 8, 9, 7, 4, 1, 2],
    [8, 9, 7, 1, 2, 4, 3, 5, 6],
    [5, 3, 1, 6, 4, 8, 9, 2, 7],
    [6, 4, 8, 9, 7, 2, 5, 3, 1],
    [9, 7, 2, 5, 1, 3, 8, 6, 4],
]

# 3) Duplicate “1” in first row → unsolvable
puzzle3 = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
    [0]*9,
]

# 4) Diagonal ones → unsolvable
puzzle4 = [[1 if i == j else 0 for j in range(9)] for i in range(9)]

# 5) A nearly‐complete but invalid puzzle
puzzle5 = [
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 0, 5, 0],
    [2, 5, 3, 1, 8, 6, 0, 7, 4],
    [6, 8, 4, 2, 0, 7, 5, 0, 0],
    [7, 9, 1, 0, 5, 0, 6, 0, 8],
]

@pytest.mark.parametrize("grid, expected", [
    (easy,    solution_easy),
    (puzzle2, solution2),
    (puzzle3, None),
    (puzzle4, None),
    (puzzle5, None),
])
def test_sudoku_solver(grid, expected):
    result = solve_sudoku(grid)
    assert result == expected
