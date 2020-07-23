import numpy as np
import pytest
from pypuzzle3d.utils import piece_to_block_list, piece_to_unique_rotations_as_block_lists


def test_piece_to_block_list(pieces_with_block_at_origin):
    for piece in pieces_with_block_at_origin:
        block_list = piece_to_block_list(piece)

        reconstructed_occupancy_array = np.zeros_like(piece)
        for (x, y, z) in block_list:
            reconstructed_occupancy_array[x, y, z] = 1

        assert np.array_equal(piece, reconstructed_occupancy_array)


def test_piece_to_unique_rotations_as_block_lists(example_pieces_with_number_of_unique_rotations):

    for piece, rotation_number in example_pieces_with_number_of_unique_rotations:
        unique_rotations_as_block_lists = piece_to_unique_rotations_as_block_lists(piece)
        assert len(unique_rotations_as_block_lists) == rotation_number


@pytest.fixture
def example_pieces_with_number_of_unique_rotations():
    pieces_with_rotation_number = []

    pieces_with_rotation_number.append((np.asarray(
                    [[[0, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]],

                     [[0, 1, 0, 0],
                      [1, 1, 1, 0],
                      [0, 1, 0, 0]],

                     [[0, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]], ]), 1))

    pieces_with_rotation_number.append((np.asarray(
                    [[[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 1, 0],
                      [1, 1, 1],
                      [0, 1, 0]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]], ]), 1))

    pieces_with_rotation_number.append((np.asarray(
                    [[[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 1, 1],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 3))

    pieces_with_rotation_number.append((np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]], ]), 6))

    pieces_with_rotation_number.append((np.asarray(
                    [[[0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [1, 1, 0],
                      [0, 1, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 8))

    pieces_with_rotation_number.append((np.asarray(
                    [[[0, 0, 0],
                      [1, 1, 1],
                      [1, 0, 1]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 12))

    pieces_with_rotation_number.append((np.asarray(
                    [[[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],

                     [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ]), 24))

    pieces_with_rotation_number.append((np.asarray(
                    [[[1, 1, 1, 0],
                      [1, 1, 1, 1],
                      [1, 1, 1, 0]],

                     [[0, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]],

                     [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]], ]), 24))

    return pieces_with_rotation_number


@pytest.fixture
def pieces_with_block_at_origin():
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
                      [0, 0, 1],
                      [0, 1, 1]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 1, 0]],

                     [[0, 0, 0],
                      [0, 1, 0],
                      [0, 1, 0]], ])

    f3 = np.asarray(
                    [[[1, 1, 0],
                      [1, 0, 0],
                      [1, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    f4 = np.asarray(
                    [[[1, 1, 0],
                      [0, 1, 1],
                      [0, 0, 1]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    f5 = np.asarray(
                    [[[1, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 1, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    f6 = np.asarray(
                    [[[1, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]],

                     [[1, 1, 1, 1],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]],

                     [[1, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]], ])

    f7 = np.asarray(
                    [[[1, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 1, 1],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]],

                     [[1, 1, 0],
                      [0, 0, 0],
                      [0, 0, 0]], ])

    return (f1, f2, f3, f4, f5, f6, f7)
