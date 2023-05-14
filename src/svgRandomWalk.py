# python3 Steven
import random
import numpy as np
from svg.file import SVGFileV2
from svg.basic import clip_float, draw_path, random_color
from common import gImageOutputPath
from common_path import join_path


def randomContinueNumbers(x0=0, N=100):
    res = [x0]
    for _ in range(N):
        res.append(res[-1] + np.random.rand())
    return res


def random_walk(x, y, n=1, step=1):
    """Return coordinantes after n block random walk"""
    for _ in range(n):
        (dx, dy) = random.choice(
            [(0, 1 * step), (0, -1 * step), (1 * step, 0), (-1 * step, 0)])  # N,S,E,W
        x += dx
        y += dy
    return x, y


def drawRandomNumbersPath(svg):
    H, W = svg.get_size()
    times = 100
    N = 500
    xW = 5

    for _ in range(times):
        path = 'M 0 0 L '
        ptX = np.arange(N) + xW
        ptY = randomContinueNumbers(N=N)

        for x, y in zip(ptX, ptY):
            path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))

        svg.draw(draw_path(path, stroke_width=0.2, color=random_color()))


def drawRandomWalkPath(svg):
    H, W = svg.get_size()
    times = 1000
    cx, cy = W // 2, H // 2

    x = cx
    y = cy
    path = 'M %.1f %.1f L ' % (x, y)
    for _ in range(times):
        x, y = random_walk(x, y, 1, step=2)
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))

    svg.draw(draw_path(path, stroke_width=0.2))


def main():
    file = join_path(gImageOutputPath, r'randomWalk.svg')
    svg = SVGFileV2(file, W=100, H=100)

    drawRandomNumbersPath(svg)
    # drawRandomWalkPath(svg)


if __name__ == '__main__':
    main()
