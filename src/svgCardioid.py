# -*- encoding: utf-8 -*-
# Date: 27/May/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Cardioid Curve
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
from svg.file import SVGFileV2
from svg.geo_math import get_regular_ngons
from common import gImageOutputPath
from common_path import join_path
from svg.basic import draw_circle, draw_ring
from svgPointLine import drawPointsCircle_style, drawlinePoints
from svg.geo_transformation import translation_pts


class CardioidData:
    def __init__(self, radius=90, center=(0, 0), divisions=100, multiplier=2):
        self._radius = radius
        self._center = center
        self._divisions = divisions
        self._multiplier = multiplier
        self._points_on_circle = None
        self._lines = None
        self._calculate()

    def _calculate(self):
        pts = get_regular_ngons(R=self._radius, N=self._divisions)
        pts = translation_pts(pts, np.array(self._center), True)
        self._points_on_circle = pts
        if self._multiplier != 1:
            self._lines = self._lines_index()
        else:
            print('Warning, no meaning when multiplier=1!')

    def _lines_index(self):
        line_map = []
        i = 0
        while True:
            tmp = int(i * self._multiplier) % self._divisions
            index = i % self._divisions
            # print('index, tmp, line_map: ', index, tmp, line_map)
            if tmp != index:
                key = (index, tmp)
                if key in line_map:
                    break
                else:
                    line_map.append(key)
            i += 1
        print('line nums: ', len(line_map))
        return line_map


def drawCardioid(svg, radius=90, divisions_N=100, multiplier=3):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    title = f'Cardioid Curve, parameters: divisions={divisions_N}, multiplier={multiplier}'
    svg.set_title(title)

    ###### draw big circle ########
    svg.draw(draw_ring(cx, cy, radius=radius, stroke_width=1))

    ###### draw points on circle ########
    pts = get_regular_ngons(R=radius, N=divisions_N)  # circle
    pts = translation_pts(pts, np.array([cx, cy]), True)
    drawPointsCircle_style(svg, pts, r=0.5, color='red', style_class='points')

    ###### draw lines ########
    if multiplier == 1:
        print('Warning, no meaning when multiplier=1!')
        return

    line_map = []
    i = 0
    while True:
        tmp = int(i * multiplier) % divisions_N
        index = i % divisions_N
        print('index, tmp, line_map: ', index, tmp, line_map)

        if tmp != index:
            key = (index, tmp)
            if key in line_map:
                break
            else:
                line_map.append(key)
                # draw line
                points = [(pts[index][0], pts[index][1], pts[tmp][0], pts[tmp][1])]
                drawlinePoints(svg, points, color='green')
        i += 1


def draw_cardioid(svg, data: CardioidData):
    ###### draw big circle ########
    svg.draw(draw_ring(data._center[0], data._center[1], radius=data._radius, stroke_color='black', stroke_width=1))

    ###### draw points on circle ########
    pts = data._points_on_circle
    drawPointsCircle_style(svg, pts, r=0.5, color='red', style_class='points')

    ###### draw lines ########
    if data._lines is not None:
        for start, stop in data._lines:
            points = [(pts[start][0], pts[start][1], pts[stop][0], pts[stop][1])]
            drawlinePoints(svg, points, color='green')


def drawCardioid_class(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    radius = 90
    divisions_N = 100
    multiplier = 2.2

    title = f'Cardioid Curve, parameters: divisions={divisions_N}, multiplier={multiplier}'
    svg.set_title(title)

    data = CardioidData(radius, (cx, cy), divisions_N, multiplier)
    draw_cardioid(svg, data)


def drawCardioid_class_mul(svg):
    H, W = svg.get_size()
    svg.set_title('Cardioid Curve showing')
    r = H * 0.95 / 4
    draw_cardioid(svg, CardioidData(r, (W / 4, H / 4), 100, 2))
    draw_cardioid(svg, CardioidData(r, (W * 3 / 4, H / 4), 30, 1.1))
    draw_cardioid(svg, CardioidData(r, (W / 4, H * 3 / 4), 50, 0.2))
    draw_cardioid(svg, CardioidData(r, (W * 3 / 4, H * 3 / 4), 100, 1.8))


def main():
    file = join_path(gImageOutputPath, r'Cardioid.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawCardioid(svg, divisions_N=200, multiplier=2)
    # drawCardioid(svg, divisions_N=100, multiplier=0.2)
    # drawCardioid(svg, divisions_N=100, multiplier=1.2)
    # drawCardioid_class(svg)
    drawCardioid_class_mul(svg)


if __name__ == "__main__":
    main()
