# python3 Steven
import random
import numpy as np
# from numpy.core.numeric import NaN
from scipy.linalg import solve
from svg.file import SVGFileV2
from svg.basic import rainbow_colors, random_color, color_fader, random_color_hsv
from svg.basic import draw_line, draw_circle, draw_rect, random_points, random_coordinates
from svg.geo_math import get_line

from svgFunction import getRandomProper3Points
from svg.geo_transformation import zoom_pts_xy_point, rotation_pts_xy_point, center_cordinates, translation_pts_xy
from svgPointLine import drawPloygon  # drawlinePointsContinus
from svgPointLine import drawlinePoints, drawlinePointsContinusRainbow
from svgPointLine import drawPointsCircle, drawPointsCircleFadeColor
from svgPointLine import drawTrianglePoints
from svgAnimation import addNodeAnitmation
from common import gImageOutputPath
from common_path import join_path


def drawLineGrapic(svg):
    H, W = svg.get_size()
    times = 100
    len = 0
    offsetX = W // 2
    offsetY = 0

    pts = []
    for _ in range(times):
        len = len + 0.5
        offsetY = offsetY + 0.5

        x1 = offsetX - len
        y1 = offsetY
        x2 = offsetX + len
        y2 = y1
        pts.append((x1, y1, x2, y2))

    for _ in range(times):
        len = len - 0.5
        offsetY = offsetY + 0.5
        pts.append((offsetX - len, offsetY, offsetX + len, offsetY))

    drawlinePoints(svg, pts)


def drawLineGrapic2(svg):
    H, W = svg.get_size()
    len = 0
    offsetX = W / 4
    offsetY = 0
    yInter = 0.5
    wStep = 0.5

    pts = []
    while (offsetY < H / 2):
        offsetY = offsetY + yInter
        if offsetY < H / 4:
            len = len + wStep
        else:
            len = len - wStep
            if (len < 0):
                break
        pts.append((offsetX - len, offsetY, offsetX + len, offsetY))

    offsetX = W * 3 / 4
    offsetY = 0
    len = 0
    while (offsetY < H / 2):
        offsetY = offsetY + yInter
        if offsetY < H / 4:
            len = len + wStep
        else:
            len = len - wStep
            if (len < 0):
                break
        pts.append((offsetX - len, offsetY, offsetX + len, offsetY))

    offsetX = W / 4
    offsetY = H / 2
    len = 0
    while (offsetY < H):
        offsetY = offsetY + yInter
        if offsetY < H * 3 / 4:
            len = len + wStep
        else:
            len = len - wStep
            if (len < 0):
                break
        pts.append((offsetX - len, offsetY, offsetX + len, offsetY))

    offsetX = W * 3 / 4
    offsetY = H / 2
    len = 0
    while (offsetY < H):
        offsetY = offsetY + yInter
        if offsetY < H * 3 / 4:
            len = len + wStep
        else:
            len = len - wStep
            if (len < 0):
                break
        pts.append((offsetX - len, offsetY, offsetX + len, offsetY))

    drawlinePoints(svg, pts)


def drawTrianglePointsXY(svg, x, y, stroke_width=0.1, color=None):
    """x&y are (3,) vector, three points"""
    pt1 = (x[0], y[0])
    pt2 = (x[1], y[1])
    pt3 = (x[2], y[2])
    drawTrianglePoints(svg, pt1, pt2, pt3,
                       stroke_width=stroke_width, color=color)


def drawLsoscelesTrianglePoints(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    times = 40
    width = 0
    rotation = True
    for _ in range(times):
        # width = width + 4
        width = 160

        x = []
        y = []

        # pt1 = (cx - width/2, cy + (width/2)*np.tan(np.pi/6))
        # pt2 = (cx + width/2, cy + (width/2)*np.tan(np.pi/6))
        # pt3 = (cx, cy - (width/2)*(np.tan(np.pi/3) - np.tan(np.pi/6)))
        x.append(cx - width / 2)
        x.append(cx + width / 2)
        x.append(cx)
        x = np.array(x)

        y.append(cy + (width / 2) * np.tan(np.pi / 6))
        y.append(cy + (width / 2) * np.tan(np.pi / 6))
        y.append(cy - (width / 2) * (np.tan(np.pi / 3) - np.tan(np.pi / 6)))
        y = np.array(y)

        if rotation:
            # theta = i*2*np.pi/(times+1)
            theta = random.random() * 2 * np.pi
            x, y = rotation_pts_xy_point(x, y, (cx, cy), theta)

        drawTrianglePointsXY(svg, x, y)


def getCenterPoint(p1, p2, p3):
    """get center point of three points"""
    # return get_outer_circle(p1,p2,p3)
    return get_inner_circle(p1, p2, p3)


def get_inner_circle(A, B, C):
    xa, ya = A[0], A[1]
    xb, yb = B[0], B[1]
    xc, yc = C[0], C[1]

    ka = (yb - ya) / (xb - xa) if xb != xa else None
    kb = (yc - yb) / (xc - xb) if xc != xb else None

    alpha = np.arctan(ka) if ka is not None else np.pi / 2
    beta = np.arctan(kb) if kb is not None else np.pi / 2

    a = np.sqrt((xb - xc)**2 + (yb - yc)**2)
    b = np.sqrt((xa - xc)**2 + (ya - yc)**2)
    c = np.sqrt((xa - xb)**2 + (ya - yb)**2)

    ang_a = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
    ang_b = np.arccos((a**2 + c**2 - b**2) / (2 * a * c))

    # slop
    k1 = np.tan(alpha + ang_a / 2)
    k2 = np.tan(beta + ang_b / 2)
    kv = np.tan(alpha + np.pi / 2)

    # circle center calculate
    y, x = solve([[1.0, -k1], [1.0, -k2]], [ya - k1 * xa, yb - k2 * xb])
    ym, xm = solve([[1.0, -ka], [1.0, -kv]], [ya - ka * xa, y - kv * x])
    r1 = np.sqrt((x - xm)**2 + (y - ym)**2)

    return (x, y, r1)


def get_outer_circle(px1, px2, px3):
    x1 = px1[0]
    y1 = px1[1]
    x2 = px2[0]
    y2 = px2[1]
    x3 = px3[0]
    y3 = px3[1]
    e = 2 * (x2 - x1)
    f = 2 * (y2 - y1)
    g = x2 * x2 - x1 * x1 + y2 * y2 - y1 * y1
    a = 2 * (x3 - x2)
    b = 2 * (y3 - y2)
    c = x3 * x3 - x2 * x2 + y3 * y3 - y2 * y2
    X = (g * b - c * f) / (e * b - a * f)
    Y = (a * g - c * e) / (a * f - b * e)
    R = np.sqrt((X - x1) * (X - x1) + (Y - y1) * (Y - y1))
    return X, Y, R


def drawRandomTrianglePoints(svg):
    """draw a random triangle and zoom this to seris"""
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    r = 10
    if 1:
        pts = getRandomProper3Points(min=r, max=W - r)
    else:
        pts = random_points((3, 2), min=cx - r, max=cx + r)
        print(pts)

    # drawTrianglePoints(svg,pts[0],pts[1],pts[2])

    cx, cy, _ = getCenterPoint(pts[0], pts[1], pts[2])
    x = pts.T[0]
    y = pts.T[1]
    print('cx,cy=', cx, cy)

    # zoomPoint = (0,0)
    zoomPoint = (cx, cy)
    times = 30
    for z in np.linspace(0.1, 1.0, times):
        zx, zy = zoom_pts_xy_point(x, y, zoomPoint, z)
        drawTrianglePointsXY(svg, zx, zy)


def getCenterPointOf2Pts(pt1, pt2, ratio=1 / 2):
    x = (pt1[0] + pt2[0]) * ratio
    y = (pt1[1] + pt2[1]) * ratio
    return np.array([[x, y]])


def getTrianglesCenterPoints(points):
    # print('points,shape=',points,points.shape)
    pt1 = getCenterPointOf2Pts(points[0], points[1])
    pt2 = getCenterPointOf2Pts(points[1], points[2])
    pt3 = getCenterPointOf2Pts(points[2], points[0])

    pts = np.concatenate((pt1, pt2), axis=0)
    pts = np.concatenate((pts, pt3), axis=0)
    return pts


def drawRandomTriangles(svg):
    """draw a random triangle and inter center triangles"""
    H, W = svg.get_size()
    # cx, cy = W // 2, H // 2
    # r = 10
    color = None  # 'black'
    pts = getRandomProper3Points(min=10, max=W - 10)
    # print(pts)
    drawTrianglePoints(svg, pts[0], pts[1], pts[2], color=color)

    for _ in range(5):
        pts = getTrianglesCenterPoints(pts)
        drawTrianglePoints(svg, pts[0], pts[1], pts[2], color=color)


def getLinePointFromSlope(slope=1, p0=(20, 0)):
    b = slope * p0[0] - p0[1]
    ptYaxis = [0, 0]
    y = -slope * ptYaxis[0] + b
    ptYaxis[1] = y
    return ptYaxis


def drawAbstractLine(svg):
    H, W = svg.get_size()
    # cx, cy = W // 2, H // 2
    N = 10

    # svg.draw(draw_rect(0,0,W,H,color='#808B96'))  # background

    slope = 1.7
    # ptYaxis = getLinePointFromSlope(slope,(20,0))
    # print('ptYaxis=',ptYaxis)
    pts1 = random_points((N,), min=0, max=W).reshape((N, 1))
    pts1 = np.append(pts1, np.zeros_like(pts1), axis=1)

    pts2 = None
    for i in pts1:
        pt = getLinePointFromSlope(slope, (i[0], i[1]))
        pt = np.array(pt).reshape(1, 2)
        # print('pt=',pt)
        # pts2 = np.append(pts2, pt, axis=1)
        pts2 = np.concatenate((pts2, pt), axis=0) if pts2 is not None else pt

    # print('pts1=',pts1)
    # print('pts2=',pts2)

    linePoints = []
    widths = []
    for pt1, pt2 in zip(pts1, pts2):
        linePoints.append((pt1[0], pt1[1], pt2[0], pt2[1]))
        widths.append(random.choice([2, 2, 4, 6, 8, 10]))
    # print(widths)
    drawlinePoints(svg, linePoints, color=None, stroke_widths=widths)


def drawArrowCircleLine(svg):
    def getPointCircle(r, theta):
        # return np.array([[r*np.cos(theta), r*np.sin(theta)]])
        return (r * np.cos(theta), r * np.sin(theta))

    def getTwinPoints(r, theta, sTheta=2 * np.pi / 80):
        pt1 = getPointCircle(r, theta - sTheta / 2)
        pt2 = getPointCircle(r, theta + sTheta / 2)
        return pt1, pt2

    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 40
    R0 = 80
    rMin = 8
    rMax = 30
    theta = 0
    for i in range(1, N):
        theta = theta + 2 * np.pi / (N - 1)
        R = R0 + random.normalvariate(mu=0, sigma=1) * 3
        r = random.choice(np.linspace(rMin, rMax, 10))

        ptInner = getPointCircle(r, theta)
        sTheta = 2 * np.pi / random.choice(range(80, 200, 2))
        ptOuter1, ptOuter2 = getTwinPoints(R, theta, sTheta=sTheta)

        x = [ptInner[0], ptOuter1[0], ptOuter2[0]]
        y = [ptInner[1], ptOuter1[1], ptOuter2[1]]

        x, y = translation_pts_xy(x, y, (cx, cy))
        # drawTrianglePoints(svg,(x[0],y[0]), (x[1],y[1]), (x[2],y[2]))
        drawPloygon(svg, [(x[0], y[0]), (x[1], y[1]),
                    (x[2], y[2])], color='black')


def drawLineGrapic3(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    length = 160

    pt1 = (-1 * length / 2, -1 * length / 2 * np.tan(np.pi / 6))
    pt2 = (length / 2, -1 * length / 2 * np.tan(np.pi / 6))
    pt3 = (0, (length / 2) / np.cos(np.pi / 6))
    x = [pt1[0], pt2[0], pt3[0]]
    y = [pt1[1], pt2[1], pt3[1]]
    x, y = translation_pts_xy(x, y, (cx, cy))
    pt1 = (x[0], y[0])
    pt2 = (x[1], y[1])
    pt3 = (x[2], y[2])

    N = 20
    pts = []

    s, b = get_line(pt2, pt3)
    for i in range(N + 1):
        xn = pt3[0] + np.abs(pt2[0] - pt3[0]) * i / N
        yn = s * xn + b
        pts.append((pt1[0], pt1[1], xn, yn))

    s, b = get_line(pt1, pt3)
    for i in range(N + 1):
        xn = pt1[0] + np.abs(pt1[0] - pt3[0]) * i / N
        yn = s * xn + b
        pts.append((pt2[0], pt2[1], xn, yn))

    s, b = get_line(pt1, pt2)
    for i in range(N + 1):
        xn = pt1[0] + np.abs(pt1[0] - pt2[0]) * i / N
        yn = s * xn + b
        pts.append((pt3[0], pt3[1], xn, yn))

    drawlinePoints(svg, pts, color='black')


def drawLineGrapic4(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    length = 160

    pt1 = (0, -1 * (length / 2) / np.cos(np.pi / 6))
    pt2 = (-1 * length / 2, length / 2 * np.tan(np.pi / 6))
    pt3 = (length / 2, length / 2 * np.tan(np.pi / 6))
    x = [pt1[0], pt2[0], pt3[0]]
    y = [pt1[1], pt2[1], pt3[1]]
    x, y = translation_pts_xy(x, y, (cx, cy))
    pt1 = (x[0], y[0])
    pt2 = (x[1], y[1])
    pt3 = (x[2], y[2])

    N = 20
    for i in range(N + 1):
        newX, newY = rotation_pts_xy_point(
            x, y, (cx, cy), theta=i * np.pi / 6 / N)
        newX, newY = zoom_pts_xy_point(newX, newY, (cx, cy), z=1 - 0.8 * i / N)
        drawTrianglePointsXY(svg, newX, newY, stroke_width=0.5, color='black')


def drawLineGrapic5(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    N = 40
    layer = 14
    r0 = 5
    for k in range(layer + 1):
        xs, ys = [], []

        r = r0 + 6 * k
        th0 = 2 * k * np.pi / layer
        for i in range(N + 1):
            theta = i * 2 * np.pi / N + th0
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            xs.append(x)
            ys.append(y)

        xs, ys = translation_pts_xy(xs, ys, (cx, cy))
        pts = np.vstack((xs, ys)).T
        drawPointsCircle(svg, pts, r=0.2 + k / 5)


def drawLineGrapic6(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    N = 18
    xs, ys = [], []
    r1 = 50
    r2 = 80
    for i in range(N + 1):
        theta = i * 2 * np.pi / N
        x = r1 * np.cos(theta)
        y = r1 * np.sin(theta)
        xs.append(x)
        ys.append(y)

    xs, ys = translation_pts_xy(xs, ys, (cx, cy))
    pts = np.vstack((xs, ys)).T
    linePts = []
    for i in pts:
        linePts.append((cx, cy, i[0], i[1]))
    drawlinePoints(svg, linePts, color='black')
    drawPointsCircle(svg, pts, r=5, color='#000000')

    xs, ys = [], []
    for i in range(N + 1):
        theta = i * 2 * np.pi / N + np.pi / N
        x = r2 * np.cos(theta)
        y = r2 * np.sin(theta)
        xs.append(x)
        ys.append(y)

    xs, ys = translation_pts_xy(xs, ys, (cx, cy))
    pts = np.vstack((xs, ys)).T
    linePts = []
    for i in pts:
        linePts.append((cx, cy, i[0], i[1]))
    drawlinePoints(svg, linePts, color='black')
    # drawPointsCircle(svg, pts, r=5, color='#808B96')
    drawPointsCircleFadeColor(svg, pts, r=5)


def random_start_coordinates(startPt, W, H, margin=10, N=100, u=0.006):
    '''generate random continue points from a start point
    startPt: (x,y)
    W: svg width
    H: svg hight
    margin: Margin to the edge
    '''
    def noise(N=1, a=-15, b=15, base=0):  # [a,b]
        # return np.random.rand(1)
        return np.random.random((N, )) * (b - a) + a + base
        # return np.random.normal(loc=0, scale=0.5, size=(N,))  # scale=0.0005

    pts = []
    pts.append(startPt)
    xl, xr = margin, W - margin
    yl, yr = margin, H - margin
    for i in range(N - 1):
        while (True):
            x = pts[-1][0] + noise(N=1, base=0).flatten()[0]
            y = pts[-1][1] + noise(N=1, base=0).flatten()[0]
            x = int(x)  # round(x, 2)
            y = int(y)  # round(y, 2)
            if (x > xl and x < xr) and (y > yl and y < yr):
                break

        pts.append((x, y))
    return pts


def drawLineGrapic7(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    pts = random_start_coordinates((cx, cy), W=W, H=H, N=5000)
    # print(pts)

    # drawlinePointsContinus(svg, pts)
    # drawlinePointsContinusRainbow(svg, pts, color='black')

    colors = []
    if 1:  # style1: circle
        c = rainbow_colors(N=int(np.sqrt(W ** 2 + H ** 2)) // 2)  # N=W//2
        for pt in pts:
            x, y = pt
            # color = c[int(x)]
            id = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            color = c[int(id)]
            colors.append(color)
        drawlinePointsContinusRainbow(svg, pts, colors=colors)
    else:  # 1/4 circle
        c = rainbow_colors(N=int(np.sqrt(W ** 2 + H ** 2)))
        for pt in pts:
            x, y = pt
            # color = c[int(x)]
            id = np.sqrt((x - W) ** 2 + (y - 0) ** 2)
            color = c[int(id)]
            colors.append(color)
        drawlinePointsContinusRainbow(svg, pts, colors=colors)


def drawLineGrapic8(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    N = 10
    margin = 6
    pts = random_coordinates(margin, W - margin, margin, H - margin, N=N)
    pts = center_cordinates(pts, np.array([cx, cy]))

    length = len(pts)
    c1 = random_color_hsv()
    c2 = random_color_hsv()
    stroke = 0.5
    for i, pt in enumerate(pts):
        # print(pt)
        p1 = pt
        if i == length - 1:
            p2 = pts[0]
        else:
            p2 = pts[i + 1]

        stroke += 1.5
        color = color_fader(c1, c2, i / length)

        # style1: lines
        node = svg.draw(
            draw_line(p1[0], p1[1], p2[0], p2[1], stroke_width=stroke, color=color))
        # svg.set_node(node, 'stroke-linejoin', 'round')  #miter round bevel miter-clip arcs
        # svg.set_node(node, 'stroke-linecap', 'round')  #butt round square

        # style2: circles
        # svg.draw(draw_circle(p1[0], p1[1], radius=stroke, color=color))


def get_anim_values(min, max):
    s = [str(i) for i in range(min, max + 1)]

    rs = s.copy()
    rs.pop()  # remove the last item
    rs.reverse()
    s = s + rs
    return ';'.join(s)


def remove_covered(pts, w, h):
    """remove some intersection rects of start point in pts
    """
    # print('pts=', pts)
    res = []

    def fun(pt):
        # print('res=', res)
        for i in res:
            if (i[0] <= pt[0] <= i[0] + w) or (i[0] <= pt[0] + w <= i[0] + w):
                if (i[1] <= pt[1] <= i[1] + h) or (i[1] <= pt[1] + h <= i[1] + h):
                    return True
        return False

    for pt in pts:
        if not fun(pt):
            res.append(pt)
    # print('len(pts),len(res)=', len(pts), len(res))
    return res


def drawLineGrapic9(svg, anim=True):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 5000

    # svg.set_background(random_color())
    svg.set_background('black')

    rt_w = 10
    rt_h = 10
    pts = random_coordinates(0, W - rt_w, 0, H - rt_h, N=N)
    # remove some points may be lead intersected rect
    pts = remove_covered(pts, rt_w, rt_h)
    for i, pt in enumerate(pts):
        rect = svg.draw(
            draw_rect(pt[0], pt[1], width=rt_w, height=rt_h, color=random_color_hsv()))

        if anim:
            if 0:  # style1 : move rect
                animateDict = {}
                animateDict['attributeName'] = 'x'
                # animateDict['from'] = f'{pt[0] - 1}'
                # animateDict['to'] = f'{pt[0] + 1}'
                animateDict["values"] = get_anim_values(pt[0] - 1, pt[0] + 1)
                animateDict['dur'] = str(random.randint(1, 3)) + 's'
                # animateDict['fill'] = 'freeze'
                animateDict["repeatCount"] = "indefinite"
                animateDict["begin"] = str(random.randint(0, 10)) + 's'
                # animateDict["additive"] = "replace"
                addNodeAnitmation(svg, rect, animateDict)

                animateDict['attributeName'] = 'y'
                # animateDict['from'] = f'{pt[1] - 1}'
                # animateDict['to'] = f'{pt[1] + 1}'
                animateDict["values"] = get_anim_values(pt[1] - 1, pt[1] + 1)
                addNodeAnitmation(svg, rect, animateDict)

            else:  # style2: rotation
                rect_cx = int(pt[0] + rt_w / 2)
                rect_cy = int(pt[1] + rt_h / 2)
                animateDict = {}
                animateDict['attributeName'] = 'transform'
                animateDict['attributeType'] = 'xml'
                animateDict['type'] = 'rotate'
                animateDict['from'] = f'0 {rect_cx} {rect_cy}'
                animateDict['to'] = f'360 {rect_cx} {rect_cy}'
                # animateDict["begin"] = str(random.randint(0, 10)) + 's'
                animateDict['dur'] = str(random.randint(4, 6)) + 's'  # '8s'
                animateDict["repeatCount"] = "indefinite"  # "5"
                addNodeAnitmation(svg, rect, animateDict,
                                  elementName='animateTransform')


def main():
    file = join_path(gImageOutputPath, r'lineGraphic.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawLineGrapic(svg)
    # drawLineGrapic2(svg)
    # drawLsoscelesTrianglePoints(svg)
    # drawRandomTrianglePoints(svg)
    # drawRandomTriangles(svg)
    # drawAbstractLine(svg)
    # drawArrowCircleLine(svg)
    # drawLineGrapic3(svg)
    # drawLineGrapic4(svg)
    # drawLineGrapic5(svg)
    # drawLineGrapic6(svg)
    # drawLineGrapic7(svg)
    drawLineGrapic8(svg)
    # drawLineGrapic9(svg)


if __name__ == '__main__':
    main()
