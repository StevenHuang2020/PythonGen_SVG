# -*- encoding: utf-8 -*-
# Date: 16/May/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Delaunay svg
"""""""""""""""""""""""""""""""""""""""""""""""""""""
# import timeit
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.path as mplPath
from svg.file import SVGFileV2
from svg.basic import random_points, mesh_grid_xy, grid_xy
from svg.geo_transformation import bounding_cordinates, zoom_pts_point, center_of_cordinates
from svg.geo_transformation import translation_pts
from svg.randoms import random2d
from svg.geo_math import get_5star, get_regular_ngons
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svgPointLine import draw_Delaunay_line
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon


def is_in_polygon(point, polygon_array: np.array) -> bool:
    return mplPath.Path(polygon_array).contains_point(point)
    # return Polygon(polygon_array).contains(Point(point))


def test(N=100000):
    polygon_array = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    pts = random_points((N, 2), 0, 1)  # [0.5, 0.5]

    for pt in pts:
        print(is_in_polygon(pt, polygon_array))


def get_random_inner_pts(polygon_array, N=10, decimal=2):
    res = np.empty(shape=[0, 2])
    # print('pts=', pts)
    xMin, xMax, yMin, yMax = bounding_cordinates(polygon_array)

    while res.shape[0] < N:
        pts = grid_xy(xMin, xMax, yMin, yMax, N)  # mesh_grid_xy
        # pt = random_points((1, 2), min=xMin, max=xMax).flatten()
        for pt in pts:
            if is_in_polygon(pt, polygon_array):
                res = np.vstack((res, pt))

    return np.round(res, decimals=decimal)


def polygon_edge_centers(polygon_array):
    """ polygon_array: (N, 2)"""
    num = polygon_array.shape[0]
    res = np.empty(shape=[0, 2])

    if num < 2:
        return res
    elif num == 2:
        x = (polygon_array[0][0] + polygon_array[1][0]) / 2
        y = (polygon_array[0][1] + polygon_array[1][1]) / 2
        res = np.vstack((res, [x, y]))
    else:
        for i in range(num - 1):
            x = (polygon_array[i][0] + polygon_array[i + 1][0]) / 2
            y = (polygon_array[i][1] + polygon_array[i + 1][1]) / 2
            res = np.vstack((res, [x, y]))
            # print('i=', polygon_array[i], '\nres=', res)

        x = (polygon_array[0][0] + polygon_array[num - 1][0]) / 2
        y = (polygon_array[0][1] + polygon_array[num - 1][1]) / 2
        res = np.vstack((res, [x, y]))

    return res


def drawDelaunay(svg, polygon_array, N=10, offset=True, offset_factor=0.8):
    """ draw Delaunay in a polygon

    Args:
        svg (_type_): svg file handle
        polygon_array (array): polylines, pointd of shape(N, 2)
        N (int, optional): N Delaunay points. Defaults to 10.
        offset (bool, optional): offset to the polygone edge. Defaults to True.
        offset_factor (float, optional): offset zoom factor. Defaults to 0.8.
    """
    N = int(N)
    if offset:
        pt = center_of_cordinates(polygon_array)
        polylines = zoom_pts_point(polygon_array, pt, z=offset_factor)
        pts = get_random_inner_pts(polylines, N)
    else:
        pts = get_random_inner_pts(polygon_array, N)

    edge_centers = polygon_edge_centers(polygon_array)

    pts = np.vstack((pts, edge_centers))  # add edge center points to Delaunay
    pts = np.vstack((pts, polygon_array))  # add polygon points to Delaunay

    # print('pts=', pts, pts.shape)
    tri = Delaunay(pts)
    draw_Delaunay_line(svg, tri, pts)


def drawDelaunay_2dRandom(svg, polygon_array, N=10, div=0.6, mesh=False):
    """ draw Delaunay in a polygon

    Args:
        svg (_type_): svg file handle
        polygon_array (array): polylines, pointd of shape(N, 2)
        N (int, optional): N Delaunay points. Defaults to 10.
        div (float, optional): offset zoom factor. Defaults to 0.8.
    """
    N = int(N)

    H, W = svg.get_size()
    if mesh:
        xMin, xMax, yMin, yMax = bounding_cordinates(polygon_array)
        pts = mesh_grid_xy(xMin, xMax, yMin, yMax, N)
    else:
        pt = center_of_cordinates(polygon_array)
        pts = random2d(pt, W / div, H / div, 10, N)  # random normal

    edge_centers = polygon_edge_centers(polygon_array)

    pts = np.vstack((pts, edge_centers))  # add edge center points to Delaunay
    pts = np.vstack((pts, polygon_array))  # add polygon points to Delaunay

    # print('pts=', pts, pts.shape)
    tri = Delaunay(pts)
    draw_Delaunay_line(svg, tri, pts)


def drawDelaunay1(svg, N=30, factor=0.9):
    H, W = svg.get_size()
    polygon_array = np.array([[W // 2, 0], [W, H], [0, H]])  # triangle
    return drawDelaunay(svg, polygon_array, N, offset_factor=factor)


def drawDelaunay2(svg, N=30, factor=0.9):
    H, W = svg.get_size()
    polygon_array = np.array([[0, 0], [W, 0], [W, H], [0, H]])  # rectangle
    return drawDelaunay(svg, polygon_array, N, offset_factor=factor)


def drawDelaunay3(svg, N=100, factor=0.4):
    H, W = svg.get_size()
    pts = get_5star(R=90, r=30)
    pts = translation_pts(pts, np.array([W // 2, H // 2]), True)
    return drawDelaunay(svg, pts, N, offset_factor=factor)


def drawDelaunay4(svg, N=200, factor=0.99):
    H, W = svg.get_size()
    # pts = get_regular_ngons(90, 3, np.pi / 6)  # triangle
    pts = get_regular_ngons(90, 60)  # circle

    pts = translation_pts(pts, np.array([W // 2, H // 2]), True)
    return drawDelaunay(svg, pts, N, offset_factor=factor)


def drawDelaunay5(svg, N=100, factor=0.3):
    H, W = svg.get_size()
    polygon_array = np.array([[0, 0], [W, 0], [W, H], [0, H]])  # rectangle
    return drawDelaunay_2dRandom(svg, polygon_array, N, div=factor)


def main():
    """ main function """
    # print(timeit.timeit(test, number=1))
    file = join_path(IMAGE_OUTPUT_PATH, r'Delaunay.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawDelaunay1(svg, 90, 0.92)
    # drawDelaunay2(svg, 180, 0.98)
    # drawDelaunay3(svg)
    # drawDelaunay4(svg)
    drawDelaunay5(svg)
    # drawDelaunay5(svg, N=10)


if __name__ == "__main__":
    main()
