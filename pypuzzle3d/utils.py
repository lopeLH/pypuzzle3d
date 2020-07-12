import numpy as np
import itertools


def make_occupacy_array_cubic(piece):
    assert piece.ndim == 3, "Input array must be exactly 3-dimensional"
    assert np.sum(piece) != 0, "Empty input occupancy array"
    if piece.shape[0] == piece.shape[1] == piece.shape[2]:
        return piece
    else:
        larger_dimension_size = np.max(piece.shape)
        cubic_piece = np.zeros((larger_dimension_size, larger_dimension_size, larger_dimension_size))
        cubic_piece[:piece.shape[0], :piece.shape[1], :piece.shape[2]] = piece
        return cubic_piece


def rotations24(piece):
    """ Generate all 24 possible orientations of an input piece.
    Args:
        a (np.ndarray): 3D occupancy array describing the shape of a piece.
    Returns:
        np.ndarray: All 24 possible orientations of the input piece, possibly including duplicates for
                    rotation invariant shapes, represented as a 4D array with shapes (24, 3, 3, 3).
    """
    assert piece.ndim == 3, "Input array must be exactly 3-dimensional"
    assert np.sum(piece) != 0, "Empty input occupancy array"

    piece = make_occupacy_array_cubic(piece)

    ndim = piece.ndim
    axcomb = list(itertools.permutations(range(ndim), ndim))  # all axes combinations
    pcomb = list(itertools.product([1, -1], repeat=ndim))  # all permuted orders
    out = np.zeros((6, 8,) + piece.shape, dtype=piece.dtype)  # Initialize output array
    for i, ax in enumerate(axcomb):  # loop through all axes for permuting
        for j, (fx, fy, fz) in enumerate(pcomb):  # all flipping combinations
            out[i, j] = np.transpose(piece[::fx, ::fy, ::fz], ax)

    idx = np.array([0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30, 32, 35, 37, 38, 41, 42, 44, 47])

    return out.reshape(6 * 8, *piece.shape)[idx]


def fingerprint(sol):

    world = np.zeros((7, 7, 7), np.int32)

    keys = range(1, 100)

    index = 0
    for p, l in sol:

        for i in range(p.shape[0]):
            if world[2 + l[0] + p[i][0], 2 + l[1] + p[i][1], 2 + l[2] + p[i][2]] != 0:
                print("ERROR!")
            world[2 + l[0] + p[i][0], 2 + l[1] + p[i][1], 2 + l[2] + p[i][2]] = keys[index]
        index += 1

    return world[2:5, 2:5, 2:5]


def piece_to_unique_rotations_as_block_lists(piece):
    assert piece.ndim == 3, "Input array must be exactly 3-dimensional"
    assert np.sum(piece) != 0, "Empty input occupancy array"
    unique_block_lists = []

    for oriented_piece in rotations24(piece):
        block_list = piece_to_block_list(oriented_piece)
        if not any([np.array_equal(np.asarray(existing_block_list),
                                   np.asarray(block_list)) for existing_block_list in unique_block_lists]):
            unique_block_lists.append(block_list)

    return np.asarray(unique_block_lists)


def piece_to_block_list(piece):
    assert piece.ndim == 3, "Input array must be exactly 3-dimensional"
    assert np.sum(piece) != 0, "Empty input occupancy array"

    block_list = []
    anchor = None
    for i in range(piece.shape[0]):
        for j in range(piece.shape[1]):
            for k in range(piece.shape[2]):
                if piece[i, j, k] != 0:
                    if len(block_list) == 0:
                        anchor = [i, j, k]
                        block_list.append([0, 0, 0])
                    else:
                        block_list.append([i - anchor[0], j - anchor[1], k - anchor[2]])
    return block_list
