# python3 Steven
import random
import numpy as np
from svg.file import SVGFileV2
from svg.basic import clip_float, draw_only_path, add_style_path, draw_path
from svg.basic import draw_circle, draw_any, random_color
from svgFunction import circleFuc, getCirclePoints, heartFuc, getRectanglePoints
from svg.geo_transformation import rotation_pts_xy, rotation_pts_xy_point
from common import gImageOutputPath
from common_path import join_path


def addNoise(x, y, alpha=2):
    x = x + np.random.randn(len(x)) * alpha
    y = y + np.random.randn(len(y)) * alpha
    return x, y


def drawOnePathcSVG(svg, ptX, ptY, width=1, onlyPath=True):
    x = ptX[0]
    y = ptY[0]
    path = 'M %.1f %.1f L ' % (x, y)
    for x, y in zip(ptX, ptY):
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))
    path = path + 'z'

    if onlyPath:
        svg.draw((path))
    else:
        svg.draw(draw_path(path, stroke_width=width, color=random_color()))


def getCirclePtsSVG(svg, r=1, N=10, offsetX=50, offsetY=50, noise=True, onlyPath=True):
    ptX, ptY = getCirclePoints(r=r, N=N, func=circleFuc)
    ptX = ptX + offsetX
    ptY = ptY + offsetY

    if noise:
        ptX, ptY = addNoise(ptX, ptY)
    return ptX, ptY


def drawRandomPath():
    file = join_path(gImageOutputPath, r'randomShapePath.svg')
    H, W = 500, 1000
    svg = SVGFileV2(file, W, H)

    singleColor = False
    if singleColor:
        onlyPath = True
        color = '#33FFC9'
        svg.draw(add_style_path(stroke=color, stroke_width=1, fill='transparent'))
    else:
        onlyPath = False

    times = 200
    r = 1

    offsetX = 50  # W//2 #
    offsetY = H // 2
    for _ in range(times):
        r = r + random.random() * 2
        # r = r + random.normalvariate(mu=0,sigma=1)*8

        offsetX = offsetX + random.random() * 5  # 8
        # offsetX = offsetX + random.normalvariate(mu=0,sigma=1)*1

        # offsetY = offsetY + random.random()*1
        # offsetX = 50 + random.random()*10
        # offsetY = 50 + random.random()*2

        ptX, ptY = getCirclePtsSVG(
            svg, r=r, N=80, offsetX=offsetX, offsetY=offsetY, noise=True, onlyPath=onlyPath)
        drawOnePathcSVG(svg, ptX, ptY, onlyPath=onlyPath)


def draw_heart_curve():
    file = join_path(gImageOutputPath, r'heartPath.svg')
    H, W = 100, 100
    svg = SVGFileV2(file, W, H)

    offsetX = W // 2
    offsetY = H // 2

    svg.draw(add_style_path(stroke='red', stroke_width=0.5, fill='red'))

    N = 100
    r = 30
    path = 'M %.1f %.1f L ' % (
        0 + offsetX, heartFuc(0, r) + offsetY)  # start point
    x = np.linspace(-r, r, N)
    # Up part points of heart curve, set sqrt value positive
    y = heartFuc(x, r=r)
    # Down part points of heart curve, set sqrt value negative
    xr = np.flip(x)
    yr = heartFuc(xr, r=r, up=False)

    x = np.concatenate((x, xr), axis=0)
    # *-1  svg coordinate system different from standard cod system
    y = np.concatenate((y, yr), axis=0) * -1
    # print('x=', x)
    # print('y=', y)
    x = x + offsetX
    y = y + offsetY

    for i, j in zip(x, y):
        path = path + ' ' + str(clip_float(i)) + ' ' + str(clip_float(j))

    svg.draw(draw_only_path(path))
    svg.close()


def drawRandomCirclePath(svg):
    H, W = svg.get_size()

    styles = ['circles', 'circle points', 'circle points random']

    onlyPath = False
    times = 100
    r = 2
    offsetX = W // 2
    offsetY = H // 2
    style = styles[1]

    if style == styles[0]:
        for _ in range(times):
            r = r + random.random() * 8
            ptX, ptY = getCirclePtsSVG(
                svg, r=r, N=200, offsetX=offsetX, offsetY=offsetY, noise=False, onlyPath=onlyPath)
            drawOnePathcSVG(svg, ptX, ptY, onlyPath=onlyPath)

    elif style == styles[1]:
        times = 10
        for _ in range(times):
            r = r + random.random() * 18
            ptX, ptY = getCirclePtsSVG(
                svg, r=r, N=20, offsetX=offsetX, offsetY=offsetY, noise=False, onlyPath=onlyPath)
            ptNumber = int(5 * r)
            # ptX = np.random.choice(ptX, ptNumber)

            ptX = ptX.reshape((len(ptX), 1))
            ptY = ptY.reshape((len(ptY), 1))
            pts = np.concatenate((ptX, ptY), axis=1)
            # print(ptX.shape, pts.shape)

            ptsIndex = np.random.randint(len(pts), size=ptNumber)
            # print('ptsIndex=', ptsIndex, len(pts))
            pts = pts[ptsIndex, :]

            for i in pts:
                # print('i=', i)
                # ra = 0.5
                ra = np.random.random() * (3 - 0.2) + 0.2
                ra = clip_float(ra)
                x = clip_float(i[0])
                y = clip_float(i[1])
                svg.draw(draw_circle(x, y, radius=ra, color=random_color()))


def getRectanglePtsSVG(w, h, N=10, noise=True):
    ptX, ptY, center = getRectanglePoints(w=w, h=h, N=N)
    if noise:
        ptX, ptY = addNoise(ptX, ptY, alpha=0.8)
    return ptX, ptY, center


def drawRandomRectanglePath(svg):
    H, W = svg.get_size()
    styles = ['rectangle', 'rectangle roation', 'rotataion Center']

    onlyPath = False
    times = 80
    w = 2
    h = w
    offsetX = 5
    offsetY = 5
    style = styles[2]

    if style == styles[0]:
        for _ in range(times):
            w = w + random.random() * 4
            h = w
            ptX, ptY, _ = getRectanglePtsSVG(w, h, N=20, noise=True)
            ptX = ptX + offsetX
            ptY = ptY + offsetY
            drawOnePathcSVG(svg, ptX, ptY, onlyPath=onlyPath)

    elif style == styles[1]:
        times = 150
        offsetX = W // 2
        offsetY = H // 2
        theta = 0
        for _ in range(times):
            w = w + random.random() * 1
            h = w
            ptX, ptY, center = getRectanglePtsSVG(w, h, N=20, noise=False)

            ptX, ptY = rotation_pts_xy(ptX, ptY, theta)
            theta = theta + 2 * np.pi / (times - 1)

            ptX = ptX + offsetX
            ptY = ptY + offsetY
            drawOnePathcSVG(svg, ptX, ptY, width=0.5, onlyPath=onlyPath)
    elif style == styles[2]:
        times = 120
        offsetX = 20  # W//2
        offsetY = 20  # H//2
        theta = 0
        for _ in range(times):
            offsetX = offsetX + random.random() * 1  # 8
            w = w + random.random() * 1
            h = w
            ptX, ptY, center = getRectanglePtsSVG(w, h, N=30, noise=True)

            ptX, ptY = rotation_pts_xy_point(ptX, ptY, center, theta)
            theta = theta + 2 * np.pi / (times - 1)

            ptX = ptX + offsetX
            ptY = ptY + offsetY
            drawOnePathcSVG(svg, ptX, ptY, width=0.5, onlyPath=onlyPath)

    print(w, H)


def drawAllTypePath(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    svg.set_title('draw path')
    g = svg.draw(draw_any('g', opacity=1.0))

    anyDict = {}
    anyDict['stroke'] = 'black'
    anyDict['fill'] = 'transparent'

    anyDict['d'] = 'M 10 10 C 20 20, 40 20, 50 10'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 70 10 C 70 20, 110 20, 110 10'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 130 10 C 120 20, 180 20, 170 10'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 10 30 C 20 50, 40 50, 50 30'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 70 30 C 70 50, 110 50, 110 30'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'MM 130 30 C 120 50, 180 50, 170 30'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 10 50 C 20 80, 40 80, 50 50'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 70 50 C 70 80, 110 80, 110 50'
    svg.draw_node(g, draw_any('path', **anyDict))
    anyDict['d'] = 'M 130 50 C 120 80, 180 80, 170 50'
    svg.draw_node(g, draw_any('path', **anyDict))

    # anyDict['d'] = 'M 10 10 10 60 60 30'
    # svg.draw_node(g, draw_any('path', **anyDict))

    anyDict['d'] = 'M 10 315    \
           L 110 215    \
           A 30 50 0 0 1 162.55 162.45  \
           L 172.55 152.45  \
           A 30 50 -45 0 1 215.1 109.9  \
           L 315 10'

    anyDict['fill'] = 'green'
    anyDict['stroke-width'] = '2'
    svg.draw_node(g, draw_any('path', **anyDict))


def main():
    # drawRandomPath()
    # draw_heart_curve()

    file = join_path(gImageOutputPath, r'randomShapePath.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawRandomCirclePath(svg)
    drawRandomRectanglePath(svg)
    # drawAllTypePath(svg)


if __name__ == '__main__':
    main()
