# -*- encoding: utf-8 -*-
# Date: 25/Jun/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Draw math functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""

import random
from itertools import combinations
import numpy as np
from svg.file import SVGFileV2
from svg.basic import clip_float, draw_path, random_color
from svg.basic import random_color_hsv, draw_only_path
from svg.geo_transformation import translation_pts_xy, reflection_points
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
# plot function to svg
# from scipy.special import perm,comb


def funcIdentity(x):
    return x  # y=x


def funcQuadratic(x):
    return x**2


def funcSin(x):
    return np.sin(x)


def funcCos(x):
    return np.cos(x)


def normalDistribution(x):
    return 1 / np.sqrt(2 * np.pi) * np.exp(-0.5 * x**2)


def softmaxFuc(x):
    softmax = np.exp(x) / np.sum(np.exp(x))
    # print(softmax)
    # print(np.sum(softmax))
    return softmax


def heartFuc(x, r=1, up=True):  # heart equation: x**2+ (5*y/4 - sqrt(abs(x)))**2 = r**2
    if up:
        a = np.sqrt(r**2 - x**2) * 1 + np.sqrt(abs(x))
    else:
        a = np.sqrt(r**2 - x**2) * (-1) + np.sqrt(abs(x))
    return a * 4 / 5


def circleFuc(x, r=1, up=True):  # circle equation: x**2+ y**2 = r**2
    if up:
        a = np.sqrt(r**2 - x**2) * 1
    else:
        a = np.sqrt(r**2 - x**2) * (-1)
    return a


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def getCirclePoints(r=1, N=10, func=heartFuc):
    x = np.linspace(-r, r, N)
    y = func(x, r=r)  # Up part points of curve, set sqrt value positive
    x_down = np.flip(x)  # Down part points of curve, set sqrt value negative
    y_down = func(x_down, r=r, up=False)

    # connect from start
    x = np.concatenate((x, x_down), axis=0)
    y = np.concatenate((y, y_down), axis=0)

    if 0:  # connect from random
        rand = np.random.randint(1, len(x), size=1)[0]
        x = np.concatenate((x[rand:], x[:rand]), axis=0)
        y = np.concatenate((y[rand:], y[:rand]), axis=0)

    # print('x=',x)
    # print('y=',y)
    return x, y


def getRectanglePoints(x0=0, y0=0, N=10, w=10, h=10):
    x1 = np.linspace(x0, x0 + w, N)
    y1 = np.zeros_like(x1) + y0
    y2 = np.linspace(y0, y0 + h, N)
    x2 = np.zeros_like(y2) + x0 + w
    x3 = np.flip(x1)
    y3 = np.zeros_like(x3) + y0 + h
    y4 = np.flip(y2)
    x4 = np.zeros_like(y4) + x0

    # connect from start
    x = np.concatenate((x1, x2), axis=0)
    x = np.concatenate((x, x3), axis=0)
    x = np.concatenate((x, x4), axis=0)

    y = np.concatenate((y1, y2), axis=0)
    y = np.concatenate((y, y3), axis=0)
    y = np.concatenate((y, y4), axis=0)

    center = ((x0 + w) / 2, (y0 + h) / 2)
    return x, y, center


def getRandomProper3Points(a=0, b=5):
    """get random point from 0,1,2,3 quadrants,
       pt(x,y) = (a ~ b)
    """
    c = list(combinations(range(4), 3))
    # [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    # print(c)
    qds = random.choice(c)
    # print('qds=',qds)
    center = (b - a) / 2.0
    pts = None
    for i in qds:
        if i == 0:
            x = np.random.random() * (center - a) + a
            y = np.random.random() * (center - a) + a
        elif i == 1:
            x = np.random.random() * (b - center) + center
            y = np.random.random() * (center - a) + a
        elif i == 2:
            x = np.random.random() * (center - a) + a
            y = np.random.random() * (b - center) + center
        elif i == 3:
            x = np.random.random() * (b - center) + center
            y = np.random.random() * (b - center) + center

        pt = np.array([[x, y]])
        pts = np.concatenate((pts, pt), axis=0) if pts is not None else pt
    return pts


def drawFuncSVG(svg, offsetX=0, offsetY=0, color=None):
    N = 500
    x = np.linspace(-100, 100, N)

    offset_x = 50
    offset_y = 100
    ptX = x + offsetX + offsetX
    ptY = funcIdentity(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)

    offset_x = 50
    offset_y = 50
    ptX = x + offsetX + offset_x
    ptY = funcQuadratic(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)

    offset_x = 50
    offset_y = 50
    ptX = x + offsetX + offset_x
    ptY = funcSin(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)

    ptX = x + offsetX + offset_x
    ptY = funcCos(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)

    ptX = x + offsetX + offset_x
    ptY = normalDistribution(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)
    ptX = x + offsetX + offset_x
    ptY = softmaxFuc(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)
    ptX = x + offsetX + offset_x
    ptY = sigmoid(x) * -1 + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)

    ptX, ptY = getCirclePoints(r=10, N=10, func=circleFuc)
    ptX = ptX + offsetX + offset_x
    ptY = ptY + offsetY + offset_y
    drawOnePathcSVG(svg, ptX, ptY, color=color)


def drawOnePathcSVG(svg, ptX, ptY, color=None, stroke_width=0.5, only_path=False):
    x = ptX[0]
    y = ptY[0]
    path = f'M {x:.1f} {y:.1f} L'
    for i, (x, y) in enumerate(zip(ptX, ptY)):
        if i == 0:
            continue
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))
    path = path + 'z'

    if only_path:
        svg.draw(draw_only_path(path))
    else:
        svg.draw(draw_path(path, stroke_width=stroke_width, color=color or random_color()))


def reflect_xy(ptX, ptY):
    """Cartesian(math) coordinate to svg coordiantes

    Args:
        ptX (array): (N, )
        ptY (array): (N, )

    Returns:
        tuple: (ptX',  ptY')
    """
    ptX = ptX.reshape((ptX.shape[0], 1))
    ptY = ptY.reshape((ptY.shape[0], 1))
    pts = np.hstack(([ptX, ptY]))
    # print('pts=', pts, pts.shape)
    return reflection_points(pts, False)


def drawFuncSVG2(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 100

    ptX, ptY = getCirclePoints(r=45, N=N, func=heartFuc)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOnePathcSVG(svg, ptX, ptY, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcQuadratic(ptX)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy + 40))
    drawOnePathcSVG(svg, ptX, ptY, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcSin(ptX) * 20
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOnePathcSVG(svg, ptX, ptY, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcCos(ptX) * 20
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOnePathcSVG(svg, ptX, ptY, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = sigmoid(ptX)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOnePathcSVG(svg, ptX, ptY, color=random_color_hsv())


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'func.svg')
    svg = SVGFileV2(file, 100, 100, border=True)
    # drawFuncSVG(svg, offsetX=10, offsetY=10)
    drawFuncSVG2(svg)


if __name__ == '__main__':
    main()
