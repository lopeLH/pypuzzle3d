
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def drawWin(win):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim3d(-2, 3)
    ax.set_ylim3d(-2, 3)
    ax.set_zlim3d(-2, 2)

    drawBox(ax, 0.)

    points = []

    for piece, loc in win:

        pointsSet = []

        for block in piece:

            pointsSet.append(np.asarray(block) + np.asarray(loc))

        points.append(np.asarray(pointsSet))

    for pointsSet in points:
        ax.scatter(pointsSet[:, 0], pointsSet[:, 1], pointsSet[:, 2], marker="o", s=400)

    plt.show()


def drawWorld(wo):

    w = wo.copy()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim3d(-2, 3)
    ax.set_ylim3d(-2, 3)
    ax.set_zlim3d(-2, 2)

    drawBox(ax, 0.0)

    points = []

    for i in range(w.shape[0]):
        for j in range(w.shape[1]):
            for k in range(w.shape[2]):
                while w[i, j, k] > 0:
                    w[i, j, k] -= 1
                    points.append([i, j, k])

    points = np.asarray(points) - 2

    ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker="o", s=400)
    plt.show()


def drawBox(ax, margin=0.5, color="black"):
    ax.plot([0 - margin, 2 + margin], [0 - margin, 0 - margin],
            [0 - margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 2 + margin], [2 + margin, 0 - margin],
            [0 - margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([0 - margin, 0 - margin], [2 + margin, 0 - margin],
            [0 - margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 0 - margin], [2 + margin, 2 + margin],
            [0 - margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([0 - margin, 2 + margin], [0 - margin, 0 - margin],
            [2 + margin, 2 + margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 2 + margin], [2 + margin, 0 - margin],
            [2 + margin, 2 + margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([0 - margin, 0 - margin], [2 + margin, 0 - margin],
            [2 + margin, 2 + margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 0 - margin], [2 + margin, 2 + margin],
            [2 + margin, 2 + margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([0 - margin, 0 - margin], [0 - margin, 0 - margin],
            [2 + margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 2 + margin], [2 + margin, 2 + margin],
            [2 + margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([2 + margin, 2 + margin], [0 - margin, 0 - margin],
            [2 + margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)
    ax.plot([0 - margin, 0 - margin], [2 + margin, 2 + margin],
            [2 + margin, 0 - margin], c=color, dashes=[2, 2], zorder=1000.)


def drawMoves(win, size=(8, 5), putPiecesIn=[1, 2, 3, 4, 5, 6], title="", arrange=230):

    points = []

    for piece, loc in win:

        pointsSet = []

        for block in piece:

            pointsSet.append(np.asarray(block) + np.asarray(loc))

        points.append(np.asarray(pointsSet))

    fig = plt.figure(figsize=size)
    colors = sns.color_palette("hls", len(win))

    for i, j in zip(range(len(points)), putPiecesIn):

        ax = fig.add_subplot(arrange + j, projection='3d')

        ax.set_xlim3d(0, 2)
        ax.set_ylim3d(0, 2)
        ax.set_zlim3d(0, 2)
        ax.axis('off')
        drawBox(ax, 0.)

        j = 0
        for pointsSet in points[0:i]:

            for pta in pointsSet:
                for ptb in pointsSet:
                    dis = np.sum(np.abs(pta - ptb))
                    if dis == 1:
                        z = (pta[0] + ptb[0]) / 2. - (pta[1] + ptb[1]) / 2.
                        ax.plot3D([pta[0], ptb[0]], [pta[1], ptb[1]], [pta[2], ptb[2]], c=colors[j],
                                  linewidth=8, solid_capstyle='round', zorder=z)

            j += 1

        for pta in points[i]:
            for ptb in points[i]:
                dis = np.sum(np.abs(pta - ptb))
                if dis == 1:
                    z = (pta[0] + ptb[0]) / 2. - (pta[1] + ptb[1]) / 2.
                    ax.plot3D([pta[0], ptb[0]], [pta[1], ptb[1]], [pta[2], ptb[2]], c=colors[j],
                              linewidth=10, solid_capstyle='round', zorder=z)

    ax.annotate(title + ".", [.92, 0.1], xycoords="figure fraction")
    plt.show()


def drawMovesSave(win, name, size=(8, 5), putPiecesIn=[1, 2, 3, 4, 5, 6], title="", arrange=230):

    points = []

    for piece, loc in win:

        pointsSet = []

        for block in piece:

            pointsSet.append(np.asarray(block) + np.asarray(loc))

        points.append(np.asarray(pointsSet))

    fig = plt.figure(figsize=size)
    colors = sns.color_palette("hls", len(win))

    for i, j in zip(range(len(points)), putPiecesIn):

        ax = fig.add_subplot(arrange + j, projection='3d')

        ax.set_xlim3d(0, 2)
        ax.set_ylim3d(0, 2)
        ax.set_zlim3d(0, 2)
        ax.axis('off')
        drawBox(ax, 0.)

        j = 0
        for pointsSet in points[0:i]:

            for pta in pointsSet:
                for ptb in pointsSet:
                    dis = np.sum(np.abs(pta - ptb))
                    if dis == 1:
                        z = (pta[0] + ptb[0]) / 2. - (pta[1] + ptb[1]) / 2.
                        ax.plot3D([pta[0], ptb[0]], [pta[1], ptb[1]], [pta[2], ptb[2]], c=colors[j],
                                  linewidth=8, solid_capstyle='round', zorder=z)

            # ax.scatter(pointsSet[:,0],pointsSet[:,1],pointsSet[:,2],c=colors[j],marker="o",
            #           s=400, edgecolor='black')

            j += 1

        # ax.scatter(points[i][:,0],points[i][:,1],points[i][:,2],marker="o",
        #           c=colors[j],linewidth=2,  s=400, edgecolor='black')

        for pta in points[i]:
            for ptb in points[i]:
                dis = np.sum(np.abs(pta - ptb))
                if dis == 1:
                    z = (pta[0] + ptb[0]) / 2. - (pta[1] + ptb[1]) / 2.
                    ax.plot3D([pta[0], ptb[0]], [pta[1], ptb[1]], [pta[2], ptb[2]], c=colors[j],
                              linewidth=10, solid_capstyle='round', zorder=z)

    ax.annotate(title + ".", [.92, 0.1], xycoords="figure fraction")
    plt.savefig(name)
