import pytest
from pypuzzle3d.solvers import find_solutions
from pypuzzle3d.puzzle_design_helpers import generate_and_solve_puzzles_from_set_of_pieces
from fixtures import some_pieces
import numpy as np


def test_core_function_can_be_imported():
    from pypuzzle3d.solvers import explore  # noqa: F401


def test_generate_and_solve_puzzles_from_set_of_pieces(some_pieces):
    all_solutions = generate_and_solve_puzzles_from_set_of_pieces(some_pieces)
    assert all_solutions is not None


def test_raises_if_some_piece_is_larger_than_the_assembled_puzzle():
    with pytest.raises(ValueError):
        find_solutions([np.ones((3,3,3)), np.ones((4,3,3))])


def test_solves_example_puzzles(example_puzzles_with_solution_number):
    for pieces, n_solutions in example_puzzles_with_solution_number:
        solutions = find_solutions(pieces)
        assert len(solutions) == n_solutions, pieces


def test_solves_example_puzzles_with_max_solutions(example_puzzles_with_solution_number):
    MAX_SOLUTIONS = 2
    for pieces, n_solutions in example_puzzles_with_solution_number:
        solutions = find_solutions(pieces, max_solutions=MAX_SOLUTIONS)
        if n_solutions > MAX_SOLUTIONS:
            assert solutions is None
        else:
            assert len(solutions) == n_solutions


@pytest.fixture
def example_puzzles_with_solution_number(some_pieces):
    puzzles = [((some_pieces[0], some_pieces[1]), 1),
               ((some_pieces[0], some_pieces[2]), 0),
               ((some_pieces[3], some_pieces[4], some_pieces[5], some_pieces[6]), 4)]
    return puzzles
