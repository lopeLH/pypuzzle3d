import numpy as np
import itertools


def rotations24(a):
    n = a.ndim
    axcomb = list(itertools.permutations(range(n), n))  # all axes combinations
    pcomb = list(itertools.product([1, -1], repeat=n))  # all permuted orders
    out = np.zeros((6, 8,) + a.shape, dtype=a.dtype)  # Initialize output array
    for i, ax in enumerate(axcomb):  # loop through all axes for permuting
        for j, (fx, fy, fz) in enumerate(pcomb):  # all flipping combinations
            out[i, j] = np.transpose(a[::fx, ::fy, ::fz], ax)

    idx = np.array([0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30, 32, 35, 37, 38, 41, 42, 44, 47])

    return out.reshape(6 * 8, 3, 3, 3)[idx]


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


def figureGen(template):
    blocksGeneral = []

    for fig in rotations24(template):
        blocks = []
        orig = None
        origFoundFlag = False

        for i in range(fig.shape[0]):
            for j in range(fig.shape[1]):
                for k in range(fig.shape[2]):

                    if origFoundFlag:
                        if fig[i, j, k] != 0:
                            blocks.append([i - orig[0], j - orig[1], k - orig[2]])

                    else:

                        if fig[i, j, k] != 0:
                            orig = [i, j, k]
                            blocks.append([0, 0, 0])
                            origFoundFlag = True

        if not any([np.array_equal(np.asarray(b), np.asarray(blocks)) for b in blocksGeneral]):
            blocksGeneral.append(blocks)

    return np.asarray(blocksGeneral)
