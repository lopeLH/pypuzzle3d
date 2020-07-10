from itertools import combinations
from pypuzzle3d.utils import figureGen
from pypuzzle3d.visualization import drawMoves
from pypuzzle3d.solvers import explore
import numpy as np


def generate_and_solve_puzzles_from_set_of_pieces(pieces_set, max_solutions=None, n_pieces_in_puzzle=4, verbose=False):

    pieces_poses = np.asarray([figureGen(f) for f in pieces_set])
    combinations_of_picece_indexes = list(combinations(range(len(pieces_poses)), n_pieces_in_puzzle))

    all_solutions = []

    for i, pieces_indexes in enumerate(combinations_of_picece_indexes):
        if verbose:
            print(f"Exploring {pieces_indexes} [{i+1}/{len(combinations_of_picece_indexes)}]", end="\r")
        pieces = pieces_poses[list(pieces_indexes)]

        solutions = explore(pieces, max_solutions=max_solutions, verbose=False)

        if solutions is not None and len(solutions) > 0:
            if verbose:
                print(F"FOUND PUZZLE WITH {len(solutions)} SOLUTIONS. PIECES: {pieces_indexes}")
                drawMoves(solutions[0], size=(8, 5), arrange=230, putPiecesIn=range(1, n_pieces_in_puzzle+1))
            all_solutions.append([pieces_indexes, solutions])
        else:
            if solutions is None:
                all_solutions.append("Too many")
            elif len(solutions) == 0:
                all_solutions.append(None)
    return all_solutions
