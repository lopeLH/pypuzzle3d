import pytest
import numpy as np
from pypuzzle3d.solvers import find_solutions
from fixtures import some_pieces


def test_solves_example_non_square_puzzles(example_non_square_puzzles_with_solution_number):
    for pieces, assembled_puzzle_shape, n_solutions in example_non_square_puzzles_with_solution_number:
        solutions = find_solutions(pieces, assembled_puzzle_shape=assembled_puzzle_shape)
        assert len(solutions) == n_solutions, pieces


@pytest.fixture
def example_non_square_puzzles_with_solution_number(some_pieces):
    puzzles = [((some_pieces[0], some_pieces[3]),
                np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],
                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 1, 1]],
                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 1),

               ((some_pieces[3], some_pieces[4], some_pieces[5]),
                np.asarray(
                    [[[1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]],
                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 1, 0]],
                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 2)]
    return puzzles
