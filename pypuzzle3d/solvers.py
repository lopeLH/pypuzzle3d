# These are the core functions of the algorithm.
import numpy as np
from numba import jit
from numba.typed import List
import numba
import itertools
from pypuzzle3d.utils import rotations24, fingerprint, piece_to_unique_rotations_as_block_lists, \
    infer_margin_size_from_world
from multiprocessing.pool import ThreadPool


def find_solutions(pieces, assembled_puzzle_shape=np.ones((3, 3, 3)), max_solutions=None):
    assert len(assembled_puzzle_shape.shape) == 3
    assert assembled_puzzle_shape.shape[0] == assembled_puzzle_shape.shape[1] == assembled_puzzle_shape.shape[2]

    for piece in pieces:
        if np.max(piece.shape) > assembled_puzzle_shape.shape[0]:
            raise ValueError("The puzzle contains a piece larger than the assembled puzzle. No solutions can be found.")

    pieces_poses = [piece_to_unique_rotations_as_block_lists(piece) for piece in pieces]
    return explore(pieces_poses, assembled_puzzle_shape=assembled_puzzle_shape, max_solutions=max_solutions)


@jit(nopython=True, nogil=True)
def place(piece, world, location):
    # Note that we copy the input world representation so we don't modify it.
    world_copy = world.copy()
    margin = infer_margin_size_from_world(world)
    for i in range(piece.shape[0]):
        world_copy[margin+location[0]+piece[i][0],
                   margin+location[1]+piece[i][1],
                   margin+location[2]+piece[i][2]] += 1

    return world_copy


@jit(nopython=True, nogil=True)
def is_solved(world, assembled_puzzle_shape):
    margin = infer_margin_size_from_world(world)
    word_in_margings = world[margin:-margin, margin:-margin, margin:-margin]
    assert word_in_margings.shape == assembled_puzzle_shape.shape
    world_rotations = rotations24(word_in_margings)
    for i in range(world_rotations.shape[0]):
        if np.array_equal(world_rotations[i], assembled_puzzle_shape):
            return True
    return False


@jit(nopython=True, nogil=True)
def check(world):
    """ Check if a world representation w is valid:
         a) no figures overlap in space
         b) no figures are outside of the 3x3x3 cube
    """
    margin = infer_margin_size_from_world(world)
    return np.sum(world > 1) == 0 and \
        (np.sum(world) - np.sum(world[margin:-margin, margin:-margin, margin:-margin])) == 0


def explore(pieces, assembled_puzzle_shape=np.ones((3, 3, 3)), max_solutions=None, verbose=True):
    """
    Main function for the exploration of solutions. Recursively explores al possible combinations of positions
    and orientations of the pieces, pruning branches when a non-valid configuration is found. This exploits the fact
    that the order in which the figures are placed is irrelevant.
    """
    assert len(pieces) > 1, "Solving a puzzle of 1 piece does not make much sense."

    solutions = List.empty_list(numba.core.types.ListType(numba.core.types.Tuple([numba.types.int32[:, :],
                                                                                  numba.types.int32[:]])))

    if np.sum([piece.shape[1] for piece in pieces]) != np.sum(assembled_puzzle_shape):
        return []

    soFar = List.empty_list(numba.core.types.Tuple([numba.types.int32[:, :], numba.types.int32[:]]))
    # Based on the heuristic that a puzzle of size SxSxS needs a margin of S on each side to make sure we don't
    # try to place pieces outside the world array representation, assuming pieces are at most of size S.
    margin = assembled_puzzle_shape.shape[0]
    world = np.zeros((assembled_puzzle_shape.shape[0] + 2 * margin,) * 3, np.int32)
    n_pieces = len(pieces)

    pieces = List(pieces)

    # Generate all posible locations [(0,0,0), (0,0,1), ...]
    locations = np.asarray(list(itertools.product(range(world.shape[0] - 2 * margin),
                                                  range(world.shape[1] - 2 * margin),
                                                  range(world.shape[2] - 2 * margin))), dtype=np.int32)

    first_level_branches_to_explore = []

    # For each orientation of the first piece in the list of pieces...
    for orient in pieces[0]:

        # For each posible location ...
        for location in locations:

            # We place the piece with the current orientation in the current location
            worldT = place(orient, world, location)

            # Then we evaluate the resulting representation of the world.
            # If no blocks are outside of the 3x3x3 cube and no pieces overlap...
            if check(worldT):
                soFarT = soFar.copy()
                soFarT.append((orient, location))
                first_level_branches_to_explore.append(
                    [pieces[1:], n_pieces, worldT, soFarT, solutions, assembled_puzzle_shape, locations, max_solutions])

    with ThreadPool() as p:
        multiprocessing_results = p.imap_unordered(lambda x: explore_deep(*x), first_level_branches_to_explore)

        for solutions_from_brach in multiprocessing_results:
            if solutions_from_brach is None:
                return None
            for solution in solutions_from_brach:
                solutions.append(solution)

            solutions = findUnique(solutions, world_with_margings_shape=world.shape)
            if verbose and len(solutions) > 0 and len(solutions_from_brach) > 0:
                print(f"Found {len(solution)} unique solutions.")
            if max_solutions is not None and len(solutions) > max_solutions:
                return None

    return solutions


@jit(nopython=True, nogil=True)
def explore_deep(pieces, n_pieces, world, soFar, solutions, assembled_puzzle_shape, locations, max_solutions=None):

    for orient in pieces[0]:
        for location in locations:

            worldT = place(orient, world, location)
            if check(worldT):
                if len(soFar) == (n_pieces-1) and is_solved(worldT, assembled_puzzle_shape):

                    soFarT = soFar.copy()
                    soFarT.append((orient, location))
                    solutions.append(soFarT)
                    solutions = findUnique(solutions, world_with_margings_shape=world.shape)
                    n_solutions = len(solutions)

                    if max_solutions is not None and n_solutions > max_solutions:
                        return None

                elif len(soFar) < (n_pieces-1):
                    soFarT = soFar.copy()
                    soFarT.append((orient, location))

                    solutions = explore_deep(pieces[1:], n_pieces=n_pieces, world=worldT, soFar=soFarT,
                                             solutions=solutions, assembled_puzzle_shape=assembled_puzzle_shape,
                                             locations=locations, max_solutions=max_solutions)
                    if solutions is None:
                        return None

    return solutions


@jit(nopython=True, nogil=True)
def findUnique(solutions, world_with_margings_shape, verbose=False):
    """
    Takes a set of non-unique solutions to a 3x3x3 puzzle and returns a list of unique solutions. That is, given
    a solution, do not consider the 26 rotated versions of that cube as different solutions.

    The idea is simple: initialize a list with the first solution found. Then, for each non-unique solution, test if a
    rotated version of it is in the that list. If not, add it to the list.

    IMPORTANT NOTE: If the puzzle contains two identical pieces, this function will identify two solutions where the
    identical pieces are swaped as different. This can be modified altering the variable keys in function fingerprint()

    Parameters
    ----------

    solutions:  list of non-unique solutions as returned by explore()

    """

    if len(solutions) < 2:
        return solutions
    # initialize list of unique solutions
    unique_success = solutions.copy()[:1]

    # initialize a list with the fingerprints of unique solutions
    # in this context a fingerprint is a 3x3x3 matrix where each entry is an integer representing
    # the figure that occupies that region of space. Each figure/piece has a different integer identifier
    unique_finger = [fingerprint(solutions[0], world_with_margings_shape=world_with_margings_shape)]

    if verbose:
        print("Unique found... ")
        print(len(unique_success))

    i = 0
    # for each solution in the list of non-unique solutions...
    for suc in solutions[1:]:

        # generate the 24 rotated versions of one fingerprint of the solution
        rots = rotations24(fingerprint(suc, world_with_margings_shape=world_with_margings_shape))

        # by default, assume this solution is one we have not seen before
        unique_flag = True

        # if any of the rotated fingerprints of the solution is in our list of fingerprints,
        # the solution is not a new one. Mark the flag as false.
        for rot in rots:
            for uni in unique_finger:
                if np.all(rot == uni):
                    unique_flag = False

        # If none of the rotated versions of the solution is in our list of fingerprints, the solution
        # is indeed new. We add it to the list of unique solutions, and its fingerprint to the list of
        # fingerprints.
        if unique_flag:
            unique_finger.append(fingerprint(suc, world_with_margings_shape=world_with_margings_shape))
            unique_success.append(suc)
            if verbose:
                print("Unique found... ")
                print(len(unique_success))
        i += 1
    return unique_success
