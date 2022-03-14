# python3 Steven
import numpy as np
import random
import itertools
from scipy.spatial import Delaunay, Voronoi
from itertools import combinations

from svg.file import SVGFileV2
from svg.basic import clip_float, draw_any, draw_line, random_color, color_fader, random_color_hsv
from svg.basic import draw_circle, rainbow_colors, draw_path, draw_polygon, draw_text, draw_ring
from svg.basic import random_points, uniform_random_points
from svg.geo_transformation import rotation_pts_xy_point, translation_pts, combine_xy, center_cordinates
from svg.geo_math import get_5star, points_on_triangle, get_regular_ngons
from graph.graphPoints import GraphPoints
from graph.interPoints import GetLineSegInterPoint
from common import gImageOutputPath


def drawlinePoints(svg, pts, node=None, stroke_width=0.5, color=None, stroke_widths=None, dash=None):
    for i, pt in enumerate(pts):
        x1, y1, x2, y2 = pt
        x1 = clip_float(x1)
        y1 = clip_float(y1)
        x2 = clip_float(x2)
        y2 = clip_float(y2)
        if stroke_widths:
            stroke_width = stroke_widths[i]
        svg.draw_node(node, draw_line(x1, y1, x2, y2, stroke_width=stroke_width, color=color or random_color(), stroke_dasharray=dash))


def drawlinePointsContinus(svg, pts, stroke_width=0.5, color=None, stroke_widths=None):
    n = len(pts)
    for i in range(n - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]

        x1 = clip_float(x1)
        y1 = clip_float(y1)
        x2 = clip_float(x2)
        y2 = clip_float(y2)
        if stroke_widths:
            stroke_width = stroke_widths[i]
        svg.draw(draw_line(x1, y1, x2, y2, stroke_width=stroke_width, color=color or random_color()))


def drawlinePointsContinusRainbow(svg, pts, stroke_width=0.5, color=None, colors=None, stroke_widths=None):
    # c = rainbow_colors(N=len(pts))
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]

        x1 = clip_float(x1)
        y1 = clip_float(y1)
        x2 = clip_float(x2)
        y2 = clip_float(y2)
        if stroke_widths:
            stroke_width = stroke_widths[i]
        if colors:
            color = colors[i]
        # color = c[i]

        svg.draw(draw_line(x1, y1, x2, y2, stroke_width=stroke_width, color=color))


def drawTrianglePoints(svg, pt1, pt2, pt3, stroke_width=0.1, color=None):
    pts = []
    pts.append((pt1[0], pt1[1], pt2[0], pt2[1]))  # pt1,pt2
    pts.append((pt1[0], pt1[1], pt3[0], pt3[1]))  # pt1,pt3
    pts.append((pt2[0], pt2[1], pt3[0], pt3[1]))  # pt2,pt3

    drawlinePoints(svg, pts, stroke_width=stroke_width, color=color or random_color())


def drawPloygonNode(svg, pts, node=None, color=None):
    # print('pts',pts)
    points = [str(clip_float(i[0])) + ',' + str(clip_float(i[1])) + ' ' for i in pts]
    points = ''.join(points)
    svg.draw_node(node, draw_polygon(points, stroke_width=0.5, color=color or random_color()))


def drawPointsCircle(svg, pts=[], node=None, r=2, color='black'):
    for pt in pts:
        x = clip_float(pt[0])
        y = clip_float(pt[1])
        svg.draw_node(node, draw_circle(x, y, radius=r, color=color))


def drawPointsCircleFadeColor(svg, pts, r=2):
    c = rainbow_colors(N=len(pts))
    # print(c,type(c))

    for i, pt in enumerate(pts):
        x = clip_float(pt[0])
        y = clip_float(pt[1])

        color = c[i]
        svg.draw(draw_circle(x, y, radius=r, color=color))


def drawPathContinuPoints(svg, pts, strokeWidth=0.5, color=None):
    path = 'M '
    for i in range(len(pts)):
        x, y = pts[i]
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))

    svg.draw(draw_path(path, stroke_width=strokeWidth, color=color or random_color()))


def drawPointsLineGraphic(svg):
    W, H = svg.get_size()
    # cx,cy = W//2,H//2
    N = 50

    color = 'black'
    pts = random_points((N, 2), min=2, max=W - 2)
    drawPointsCircle(svg, pts, r=1, color='red')

    graph = GraphPoints(pts)
    # graph.show()

    # conMatrix = graph.getConnectionMatrix(K=3,KNearst=4)  # style1
    conMatrix = graph.getConnectionMatrix2(KNearst=6)  # style2
    # print('conMatrix=',conMatrix)
    linePoints = []
    for i in conMatrix:
        s, t = i[0], i[1]  # start stop point index
        if t == -1:
            continue

        conect = (pts[s][0], pts[s][1], pts[t][0], pts[t][1])
        linePoints.append(conect)

    drawlinePoints(svg, linePoints, color=color)
    # drawInterPointLines(svg, linePoints, r=1, color=color)  # draw intersection points


def drawPointsLineGraphic2(svg):
    W, H = svg.get_size()
    # cx,cy = W//2,H//2
    N = 200

    color1 = 'green'
    color2 = '#C70039'

    # svg.draw(draw_rect(0,0,W,H,color='#808B96')) #background
    pts = random_points((N, 2), min=2, max=W - 2)

    pts1 = pts[:N // 2]
    pts2 = pts[N // 2:]
    drawPointsCircle(svg, pts1, color=color1)
    drawPointsCircle(svg, pts2, color=color2)

    linePoints = [(0, 0, i[0], i[1]) for i in pts1]
    drawlinePoints(svg, linePoints, color=color1, stroke_width=0.2)

    linePoints = [(i[0], i[1], W, H) for i in pts2]
    drawlinePoints(svg, linePoints, color=color2, stroke_width=0.2)


def drawPointsLineGraphic3(svg):
    W, H = svg.get_size()
    # cx,cy = W//2,H//2
    N = 100
    color1 = 'green'
    # color2 = 'yellow'

    pts = random_points((N, 2), min=2, max=W - 2)

    pts1 = pts[: N // 2]
    pts2 = pts[N // 2:]
    drawPointsCircle(svg, pts1, r=1, color=color1)
    drawPointsCircle(svg, pts2, r=1, color=color1)

    linePoints = [(pt1[0], pt1[1], pt2[0], pt2[1]) for pt1, pt2 in zip(pts1, pts2)]

    drawlinePoints(svg, linePoints, color=color1, stroke_width=0.2)
    drawInterPointLines(svg, linePoints, r=1, color=color1)


def drawPointsLineGraphic4(svg):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 300
    r0 = 80
    color = '#48C9B0'  # 'green'

    offsetX = cx
    offsetY = cy
    linePoints = []
    theta = 0
    strokeWidths = []
    for _ in range(N):
        r = r0 + random.normalvariate(mu=0, sigma=1) * 4
        theta = theta + 2 * np.pi / (N - 1) + random.normalvariate(mu=0, sigma=1) * .01
        x = r * np.cos(theta) + offsetX
        y = r * np.sin(theta) + offsetY
        linePoints.append((offsetX, offsetY, x, y))
        strokeWidths.append(random.choice([0.2, 0.3, 0.8, 1.0, 1.5]))

    drawlinePoints(svg, linePoints, color=color, stroke_widths=strokeWidths)


def drawInterPointLines(svg, linePoints, r=1, color=None):
    for line in linePoints:
        for i in linePoints:
            if line == i:
                continue

            # print('line=', line)
            # print('i=', i)

            line1 = np.array(list(line)).reshape((2, 2))
            line2 = np.array(list(i)).reshape((2, 2))
            # print('line1=',line1)
            # print('line2=',line2)
            ptInter = GetLineSegInterPoint(line1, line2).get_inter()
            if ptInter:
                # print('ptInter=',ptInter)
                drawPointsCircle(svg, [ptInter], r=1, color=color)  # r=3, color='red'


def drawPointsLineGraphic5(svg):
    W, H = svg.get_size()
    # cx,cy = W//2,H//2
    N = 10

    color = 'black'
    pts = random_points((N, 2), min=2, max=W - 2)
    drawPointsCircle(svg, pts, r=1)

    graph = GraphPoints(pts)
    # graph.show()

    conMatrix = graph.getConnectionMatrix2(KNearst=3)
    print('conMatrix=', conMatrix)
    # for i,pt in enumerate(pts):
    #     #print(i,pt, conMatrix[i])
    #     ptsTriangle=[]
    #     ptsTriangle.append(pts[i])
    #     ptsTriangle.append(pts[conMatrix[i][0]])
    #     ptsTriangle.append(pts[conMatrix[i][1]])

    #     color = None
    #     drawPloygon(svg,ptsTriangle,color=color)

    linePoints = []
    for i in conMatrix:
        s, t = i[0], i[1]  # start stop point index
        if t == -1:
            continue
        linePoints.append((pts[s][0], pts[s][1], pts[t][0], pts[t][1]))

    drawlinePoints(svg, linePoints, color=color)


def drawPloygon(svg, pts, color=None, stroke_color=None):
    # print('pts',pts)
    points = []
    for i in pts:
        points.append(str(clip_float(i[0])) + ',' + str(clip_float(i[1])) + ' ')
    points = ''.join(points)
    svg.draw(draw_polygon(points, stroke_width=0.5,
                          color=color or random_color(),
                          stroke_color=stroke_color))


def drawPointsLineGraphic6(svg):
    W, H = svg.get_size()
    # cx,cy = W//2,H//2
    N = 50

    color = 'black'
    pts = random_points((N, 2), min=2, max=W - 2)
    drawPointsCircle(svg, pts, r=1)

    graph = GraphPoints(pts)
    # graph.show()

    # conMatrix = graph.getAllConnectionMatrix()
    conMatrix = graph.getConnectionMatrix2(KNearst=4)
    print('conMatrix=', conMatrix)
    linePoints = []
    for i in conMatrix:
        s, t = i[0], i[1]  # start stop point index
        if t == -1:
            continue

        conect = (pts[s][0], pts[s][1], pts[t][0], pts[t][1])
        if not IsIntersectionWithAlreayLines(conect, linePoints):
            linePoints.append(conect)

    drawlinePoints(svg, linePoints, color=color)


def IsIntersectionWithAlreayLines(conect, linePoints):
    def getLineFrom2Pts(connect):
        return np.array(list(connect)).reshape((2, 2))

    line1 = getLineFrom2Pts(conect)
    for i in linePoints:
        line2 = getLineFrom2Pts(i)
        if GetLineSegInterPoint(line1, line2).get_inter():
            return True
    return False


def drawPointsLineGraphic7(svg):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2

    r = 50
    x0 = [cx, cx + 2 * r, cx + r]
    y0 = [cy, cy, cy - r * np.tan(np.pi / 6)]

    times = 8
    theta = 0
    for i in range(times):
        theta = i * (2 * np.pi / times)
        x, y = rotation_pts_xy_point(x0, y0, (cx, cy), theta)
        drawPloygon(svg, [(x[0], y[0]), (x[1], y[1]), (x[2], y[2])], color='black')


def drawPointsLineGraphic8(svg):  # Neuron network
    def getNumberYs(H, N=3):
        offsetY = 190 / N
        # hInter = (H - 2 * offsetY) / (N - 1)
        if N == 1:
            return [H / 2]
        return np.linspace(offsetY, H - offsetY, N)

    W, H = svg.get_size()
    # cx, cy = W // 2, H // 2

    layerNumbers = [8, 6, 6, 4]
    ptsLayers = []

    inter = 52
    x0 = 15
    for i, N in enumerate(layerNumbers):
        # x = x0 + i*inter
        xs = np.zeros((N,)) + x0 + i * inter
        ys = getNumberYs(H, N)
        # print('xs=', len(xs), xs)
        # print('ys=', len(ys), ys)

        ptLayer = np.stack(([xs, ys])).T
        # print('ptLayer=',ptLayer)
        ptsLayers.append(ptLayer)

    # print('ptsLayers=',ptsLayers)
    for i, layPts in enumerate(ptsLayers):
        x = layPts[0][0] - 15
        y = layPts[0][1] - 8
        # print(x,y)
        svg.draw(draw_text(x, y, 'layer' + str(i)))
        drawPointsCircle(svg, layPts, r=3, color=random_color())

    for i in range(len(ptsLayers) - 1):
        layerPtsPre = ptsLayers[i]
        layerPts = ptsLayers[i + 1]
        # print('layerPtsPre=',layerPtsPre)
        # print('layerPts=',layerPts)

        linePoints = []
        for pre in layerPtsPre:
            for cur in layerPts:
                # print('pre,cur=', pre, cur)
                conect = (pre[0], pre[1], cur[0], cur[1])
                linePoints.append(conect)

        drawlinePoints(svg, linePoints, color='black')


def drawPointsLineGraphic9(svg):
    W, H = svg.get_size()
    # cx, cy = W // 2, H // 2
    N = 50

    pts = random_points((N, 2), min=2, max=W - 2)
    drawPointsCircle(svg, pts, r=2, color='black')
    drawPointsCircle(svg, pts, r=1.5, color='red')

    # print(pts, len(pts), type(pts))
    ptsNum = list(itertools.combinations(range(len(pts)), 2))
    # print(ptsNum)
    linePts = np.array([]).reshape(0, 2)
    for i, j in ptsNum:
        # print(i,j, pts[i], pts[j])
        # linePts.append([pts[i], pts[j]])
        linePts = np.vstack((linePts, pts[i]))
        linePts = np.vstack((linePts, pts[j]))

    # print('linePts=', linePts)
    drawlinePointsContinus(svg, linePts, stroke_width=0.2, color='black')


def draw_Delaunay_triangle(svg, tri, pts):
    # print('tri.simplices=', tri.simplices, len(tri.simplices))
    con_ponts = pts[tri.simplices]
    # print('con_ponts=', con_ponts, len(con_ponts))
    num = len(con_ponts)
    ci = np.random.randint(num, size=num)
    for i, pts in enumerate(con_ponts):
        # color = color_fader('#000000', '#ffffff', ci[i % num] / num)
        # color = color_fader('#F2F5F3', '#4A406C', ci[i % num] / num)  # purple
        # color = color_fader('#8FBC8F', '#4B8063', ci[i % num] / num)  # green
        color = random_color_hsv()
        drawPloygonNode(svg, pts=pts, color=color)


def draw_Delaunay_line(svg, tri, pts, color='green'):
    linePoints = []
    com = list(combinations(range(3), 2))
    # print(com)
    for pt in tri.simplices:
        for i in com:
            linePoints.append((pt[i[0]], pt[i[1]]))

    # print('linePoints=', linePoints, len(linePoints))
    # linePoints = list(set(linePoints))
    linePoints = list(set(map(tuple, map(sorted, linePoints))))
    # print('linePoints=', linePoints, len(linePoints))

    con_ponts = [pts[[i[0], i[1]]] for i in linePoints]  # pts[[4,2]]
    # print('con_ponts=', con_ponts)
    con_ponts = [i.flatten() for i in con_ponts]
    # print('con_ponts=', con_ponts)
    drawlinePoints(svg, con_ponts, color=color)  # draw lines

    drawPointsCircle(svg, pts, r=0.8, color='black')  # draw node circle


def drawPointsLineGraphic10(svg):
    """ https://en.wikipedia.org/wiki/Delaunay_triangulation """
    def get_edge_points(W, H, vNum, hNum):
        hInter = W // hNum
        vInter = H // vNum
        res = []
        for i in range(hNum+1):
            res.append([i*hInter, 0])
            res.append([i*hInter, H])

        for i in range(1, vNum):
            res.append([0, i*vInter])
            res.append([W, i*vInter])
        res = np.asarray(res)
        # print('res=', res, res.shape)
        return res

    W, H = svg.get_size()
    cx, cy = W / 2, H // 2
    N = 20

    # pts = random_points((100, 2), min=2, max=W - 2)
    pts = uniform_random_points(W, H, N, N, x_offset=W//N/6, y_offset=H//N/6)

    # print('pts.shape=', pts.shape)
    # s_pt = np.array([[0, 0], [W, 0], [0, H], [W, H]])  # 4 corners
    s_pt = get_edge_points(W, H, N, N)
    pts = np.vstack((pts, s_pt))
    # print('pts, pts.shape=', pts, pts.shape)

    tri = Delaunay(pts)

    draw_Delaunay_line(svg, tri, pts)
    # draw_Delaunay_triangle(svg, tri, pts)

    # svg.draw(draw_text(x=30, y=cy, text='Delaunay triangulation', color='red', fontsize='12px'))


def draw_plogon_subtriangle(svg, pts, center_pt, N=500):
    x, y = translation_pts(pts, center_pt)

    # pts_ploygon = [(i, j) for i, j in zip(x, y)]
    # drawPloygon(svg, pts=pts_ploygon, stroke_color='black', color='None')

    x = x.reshape((x.shape[0], 1))
    y = y.reshape((y.shape[0], 1))
    new_pts = np.concatenate((x, y), axis=1)
    # print('new_pts=', new_pts, new_pts.shape)
    tri = Delaunay(new_pts)
    draw_Delaunay_line(svg, tri, new_pts, color='green')

    con_ponts = new_pts[tri.simplices]
    # print('con_ponts=', con_ponts, len(con_ponts))
    num = len(con_ponts)
    colors = [random_color_hsv() for _ in range(num)]
    for i, pts in enumerate(con_ponts):
        # print(i, pts)
        inner_pts = points_on_triangle(pts, N)
        # print(i, inner_pts)
        drawPointsCircle(svg, inner_pts, r=0.8, color=colors[i])


def drawPointsLineGraphic11(svg):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2

    path = f'M{W/2} 0 V{H}'
    svg.draw(draw_path(path, stroke_width=0.5, color='green'))
    path = f'M0 {H/2} H{W}'
    svg.draw(draw_path(path, stroke_width=0.5, color='green'))

    pts = get_regular_ngons(R=48, N=4)
    draw_plogon_subtriangle(svg, pts, (W/4, H/4))

    pts = get_regular_ngons(R=48, N=5)
    draw_plogon_subtriangle(svg, pts, (W*3/4, H/4))

    pts = get_regular_ngons(R=48, N=6)
    pts2 = get_regular_ngons(R=22, N=6, offset_angle=np.pi/6)
    pts = np.vstack((pts, pts2))
    # print('pts=', pts, pts.shape)
    draw_plogon_subtriangle(svg, pts, (W/4, H*3/4), N=100)

    pts = get_regular_ngons(R=48, N=7)
    pts2 = get_regular_ngons(R=32, N=7, offset_angle=np.pi/7)
    pts = np.vstack((pts, pts2))
    draw_plogon_subtriangle(svg, pts, (W*3/4, H*3/4), N=100)


def get_voronoi_lines(vor):
    center = vor.points.mean(axis=0)
    ptp_bound = vor.points.ptp(axis=0)

    finite_segments = []
    infinite_segments = []
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            finite_segments.append(vor.vertices[simplex])
        else:
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            if (vor.furthest_site):
                direction = -direction
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            infinite_segments.append([vor.vertices[i], far_point])
    return np.asarray(finite_segments), np.asarray(infinite_segments)


def get_vor_region_polygons(vor, radius=None):
    """get all finite and non-finite polygons"""
    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # print('all_ridges=', all_ridges)
    # finit_polygons = []

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = np.asarray(vor.regions[region])
        if np.all(vertices >= 0):
            new_regions.append(vertices)
            # polygon = [vor.vertices[i].tolist() for i in vertices]
            # finit_polygons.append(polygon)
        else:
            # reconstruct a non-finite region
            new_region = [v for v in vertices if v >= 0]
            for p2, v1, v2 in all_ridges[p1]:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge
                t = vor.points[p2] - vor.points[p1]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

    new_vertices = np.asarray(new_vertices)
    # print('new_regions=', new_regions)
    # print('new_vertices=', new_vertices)
    return new_regions, new_vertices


def draw_voronoi_regions(svg, node, vor, radius=None):
    regions, vertices = get_vor_region_polygons(vor, radius)

    num = len(regions)
    ci = np.random.randint(num, size=num)
    for i, region in enumerate(regions):
        polygon = vertices[region]
        # color = color_fader('#000000', '#ffffff', ci[i % num] / num)
        color = color_fader('#F2F5F3', '#4A406C', ci[i % num] / num)  # purple
        # color = color_fader('#8FBC8F', '#4B8063', ci[i % num] / num)  # green
        # color = random_color_hsv()
        drawPloygonNode(svg, pts=polygon, node=node, color=color)

    '''
    # color regions
    polygons = []
    for r in vor.point_region:
        region = vor.regions[r]
        if region is not None:
            if not -1 in region:
                polygon = [vor.vertices[i].tolist() for i in region]
                # print('polygon=', polygon)
                polygons.append(polygon)
            else:
                region = [x for x in region if x >= 0]  # finite end Voronoi vertex
                print('region=', region)
                # polygon = [vor.vertices[i].tolist() for i in region]
                # polygons.append(polygon)

    for i in polygons:
        drawPloygonNode(svg, i, node=node, color=random_color_hsv())
    '''


def drawPointsLineGraphic12(svg):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 10

    defs = svg.draw(draw_any('defs'))  # for cliping the outside drawing
    clip = svg.draw_node(defs, draw_any('clipPath', id='clip'))
    svg.draw_node(clip, draw_any('rect', x="0", y="0", width=f"{W}", height=f"{H}"))

    group = svg.draw(draw_any('g'))
    svg.set_node(group, 'clip-path', 'url(#clip)')

    offset = 6
    # pts = random_points((50, 2), min=offset, max=W-offset)
    pts = uniform_random_points(W, H, N, N, x_offset=W//N/8, y_offset=H//N/8)
    # pts = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])*40

    # x, y = translation_pts(pts, (cx, cy))
    # pts = combine_xy(x, y)
    # pts = center_cordinates(pts, (cx, cy))
    # print('pts.shape=', pts, pts.shape)

    vor = Voronoi(pts)
    # print('vor.vertices=', vor.vertices, vor.vertices.shape)
    # print('vor.ridge_points=', vor.ridge_points, vor.ridge_points.shape)
    # print('vor.regions=', vor.regions, len(vor.regions))
    # print('vor.ridge_vertices=', vor.ridge_vertices, len(vor.ridge_vertices))
    # print('vor.point_region=', vor.point_region, len(vor.point_region))

    f_segments, i_segments = get_voronoi_lines(vor)
    f_segments = [i.flatten() for i in f_segments]
    i_segments = [i.flatten() for i in i_segments]
    # print('f_segments=', f_segments)
    # print('i_segments=', i_segments)

    # draw Voronoi ridges--lines
    for i in f_segments:
        drawlinePoints(svg, [i], node=group, color='green')
    for i in i_segments:
        drawlinePoints(svg, [i], node=group, color='green', dash='None')

    draw_voronoi_regions(svg, group, vor)  # color regions

    drawPointsCircle(svg, pts, node=group, r=1, color='black')
    drawPointsCircle(svg, vor.vertices, node=group, r=0.8, color='green')


def area_regular_polygon(r=1, N=6):
    # len = 2 * np.sin(np.pi / N) * r / 2
    len = np.sin(np.pi / N) * r
    s = len * r * N
    return s


def chord_length(r=1, pre_chord_len=1, N=6):
    """regular polygon chord length

    Args:
        r (float): radius of circle
        pre_chord_len (float): chord length of N(6, 12, 24, 48, ...) regular polygon
    """
    # https://en.wikipedia.org/wiki/Liu_Hui's_%CF%80_algorithm
    chord_len = np.sqrt(pre_chord_len**2/4 + (r - np.sqrt(r**2-pre_chord_len**2/4))**2)
    s = pre_chord_len*r*N/2
    return s, chord_len


def drawPointsLineGraphic13(svg):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2
    r = 55
    cy -= 20

    g = svg.draw(draw_any('g'))
    svg.draw_node(g, draw_ring(cx, cy, radius=r))

    pts_12 = get_regular_ngons(r, 12)
    pts_12 = translation_pts(pts_12, (cx, cy), True)
    # print('pts_12, pts_12.shape', pts_12, pts_12.shape)
    drawPointsCircle(svg, pts_12, node=g, r=1, color='green')
    drawPloygonNode(svg, pts_12, g, color='blue')

    pts_6 = get_regular_ngons(r, 6)
    pts_6 = translation_pts(pts_6, (cx, cy), True)
    # print('pts_6, pts_6.shape', pts_6, pts_6.shape)
    drawPointsCircle(svg, pts_6, node=g, r=1, color='red')
    drawPloygonNode(svg, pts_6, g, color='green')

    # draw lines
    linePts = np.array([]).reshape(0, 2)
    for pt in pts_6:
        linePts = np.vstack((linePts, pt))
        linePts = np.vstack((linePts, [cx, cy]))

    linePts = np.vstack((linePts, [cx, cy]))
    linePts = np.vstack((linePts, pts_12[3]))
    # print('linePts=', linePts)
    drawlinePointsContinus(svg, linePts, stroke_width=0.5, color='black')

    svg.draw_node(g, draw_text(52, 15, "Pi Day of 2022", fontsize='12px'))
    svg.draw_node(g, draw_text(25, 150, "Liu Hui's π algorithm", fontsize='12px'))

    strs = []
    y0 = 160
    x0 = 2

    r = 1
    chord_len = r  # chord length of hexagon equal to r
    for i in range(1, 11):
        N = np.power(2, i - 1) * 6
        # s = area_regular_polygon(N=N)
        s, chord_len = chord_length(r=1, pre_chord_len=chord_len, N=N)
        # print('N, s, chord_len=', N, s, chord_len)
        x = f'S_{2*N}={s}'
        print(x)
        strs.append(x)

        if i % 2 == 0:
            svg.draw_node(g, draw_text(x0, y0, ','.join(strs), fontsize='7px'))
            y0 += 8
            strs = []


def drawPointLine():
    file = gImageOutputPath + r'\pointsLine.svg'
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawPointsLineGraphic(svg)
    # drawPointsLineGraphic2(svg)
    # drawPointsLineGraphic3(svg)
    # drawPointsLineGraphic4(svg)
    # drawPointsLineGraphic5(svg)
    # drawPointsLineGraphic6(svg)
    # drawPointsLineGraphic7(svg)
    # drawPointsLineGraphic8(svg)
    # drawPointsLineGraphic9(svg)
    # drawPointsLineGraphic10(svg)
    # drawPointsLineGraphic11(svg)
    # drawPointsLineGraphic12(svg)
    drawPointsLineGraphic13(svg)


def main():
    drawPointLine()


if __name__ == '__main__':
    main()
