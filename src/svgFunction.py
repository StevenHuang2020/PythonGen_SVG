import numpy as np
import random
from svg.file import SVGFileV2
from svg.basic import clip_float, draw_path, random_color, random_color_hsv
from svg.geo_transformation import translation_pts_xy, reflection_points
from common import gImageOutputPath
# plot function to svg
# from scipy.special import perm,comb
from itertools import combinations


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
    xDown = np.flip(x)  # Down part points of curve, set sqrt value negative
    yDown = func(xDown, r=r, up=False)

    # connect from start
    x = np.concatenate((x, xDown), axis=0)
    y = np.concatenate((y, yDown), axis=0)

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


def getRandomProper3Points(min=0, max=5):
    """get random point from 0,1,2,3 quadrants,
       pt(x,y) = (min ~ max)
    """
    c = list(combinations(range(4), 3))
    # [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    # print(c)
    qds = random.choice(c)
    # print('qds=',qds)
    center = (max - min) / 2.0
    pts = None
    for qd in qds:
        if qd == 0:
            x = np.random.random() * (center - min) + min
            y = np.random.random() * (center - min) + min
        elif qd == 1:
            x = np.random.random() * (max - center) + center
            y = np.random.random() * (center - min) + min
        elif qd == 2:
            x = np.random.random() * (center - min) + min
            y = np.random.random() * (max - center) + center
        elif qd == 3:
            x = np.random.random() * (max - center) + center
            y = np.random.random() * (max - center) + center

        pt = np.array([[x, y]])
        pts = np.concatenate((pts, pt), axis=0) if pts is not None else pt
    return pts


def drawFuncSVG(svg, offsetX=0, offsetY=0, color=None):
    N = 500
    x = np.linspace(-100, 100, N)

    fOffsetX = 50
    fOffsetY = 100
    ptX = x + offsetX + offsetX
    ptY = funcIdentity(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)

    fOffsetX = 50
    fOffsetY = 50
    ptX = x + offsetX + fOffsetX
    ptY = funcQuadratic(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)

    fOffsetX = 50
    fOffsetY = 50
    ptX = x + offsetX + fOffsetX
    ptY = funcSin(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)

    ptX = x + offsetX + fOffsetX
    ptY = funcCos(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)

    ptX = x + offsetX + fOffsetX
    ptY = normalDistribution(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)
    ptX = x + offsetX + fOffsetX
    ptY = softmaxFuc(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)
    ptX = x + offsetX + fOffsetX
    ptY = sigmoid(x) * -1 + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)

    ptX, ptY = getCirclePoints(r=10, N=10, func=circleFuc)
    ptX = ptX + offsetX + fOffsetX
    ptY = ptY + offsetY + fOffsetY
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=color)


def drawOneFuncSVG(svg, ptX, ptY, N=10, color=None):
    x = ptX[0]
    y = ptY[0]
    path = 'M %.1f %.1f L ' % (x, y)
    for x, y in zip(ptX, ptY):
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))

    svg.draw(draw_path(path, stroke_width=0.5, color=color or random_color()))


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
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 100

    ptX, ptY = getCirclePoints(r=45, N=N, func=heartFuc)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcQuadratic(ptX)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy+40))
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcSin(ptX)*20
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = funcCos(ptX)*20
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=random_color_hsv())

    ptX = np.linspace(-50, 50, num=200)
    ptY = sigmoid(ptX)
    ptX, ptY = reflect_xy(ptX, ptY)
    ptX, ptY = translation_pts_xy(ptX, ptY, (cx, cy))
    drawOneFuncSVG(svg, ptX, ptY, N=N, color=random_color_hsv())


def main():
    file = gImageOutputPath + r'\func.svg'
    svg = SVGFileV2(file, 100, 100, border=True)
    # drawFuncSVG(svg, offsetX=10, offsetY=10)
    drawFuncSVG2(svg)


if __name__ == '__main__':
    main()
