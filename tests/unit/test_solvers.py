import numpy as np
import pytest
from pypuzzle3d.solvers import find_solutions


def test_core_function_can_be_imported():
    from pypuzzle3d.solvers import explore  # noqa: F401


def test_solves_example_puzzles(example_puzzles_with_solution_number):
    for pieces, n_solutions in example_puzzles_with_solution_number:
        solutions = find_solutions(pieces)
        assert len(solutions) == n_solutions, pieces


@pytest.fixture
def example_puzzles_with_solution_number():
    f1 = np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    f2 = np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],

                     [[1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    f3 = np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],

                     [[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    puzzles = [((f1, f2), 1),
               ((f1, f3), 0)]
    return puzzles
