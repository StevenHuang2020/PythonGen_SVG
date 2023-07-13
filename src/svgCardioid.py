# -*- encoding: utf-8 -*-
# Date: 27/May/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Cardioid Curve
"""""""""""""""""""""""""""""""""""""""""""""""""""""
from dataclasses import dataclass, field
import numpy as np
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svg.file import SVGFileV2
from svg.geo_math import get_regular_ngons
from svg.basic import draw_ring
from svg.geo_transformation import translation_pts
from svgPointLine import drawPointsCircle_style, drawlinePoints


@dataclass(slots=True)
class CardioidData:
    """ Cardioid class"""
    radius: float
    center: tuple
    divisions: int
    multiplier: float
    points_on_circle: np.ndarray = field(init=False)
    lines: list[tuple] = field(default_factory=list)

    def __post_init__(self):
        self._calculate()

    def _calculate(self):
        pts = get_regular_ngons(R=self.radius, N=self.divisions)
        pts = translation_pts(pts, np.array(self.center), True)
        self.points_on_circle = pts
        if self.multiplier != 1:
            self.lines = self._lines_index()
        else:
            print('Warning, no meaning when multiplier=1!')

    def _lines_index(self):
        line_map = []
        i = 0
        while True:
            tmp = int(i * self.multiplier) % self.divisions
            index = i % self.divisions
            # print('index, tmp, line_map: ', index, tmp, line_map)
            if tmp != index:
                key = (index, tmp)
                if key in line_map:
                    break

                line_map.append(key)
            i += 1
        print('line nums: ', len(line_map))
        return line_map


def drawCardioid(svg, radius=90, divisions_n=100, multiplier=3):
    """ draw """
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    svg.set_title(f'Cardioid: divisions={divisions_n}, multiplier={multiplier}')

    ###### draw big circle ########
    svg.draw(draw_ring(cx, cy, radius=radius, stroke_width=1))

    ###### draw points on circle ########
    pts = get_regular_ngons(R=radius, N=divisions_n)  # circle
    pts = translation_pts(pts, np.array([cx, cy]), True)
    drawPointsCircle_style(svg, pts, r=0.5, color='red', style_class='points')

    ###### draw lines ########
    if multiplier == 1:
        print('Warning, no meaning when multiplier=1!')
        return

    line_map = []
    i = 0
    while True:
        tmp = int(i * multiplier) % divisions_n
        index = i % divisions_n
        print('index, tmp, line_map: ', index, tmp, line_map)

        if tmp != index:
            key = (index, tmp)
            if key in line_map:
                break

            line_map.append(key)
            # draw line
            points = [(pts[index][0], pts[index][1], pts[tmp][0], pts[tmp][1])]
            drawlinePoints(svg, points, color='green')
        i += 1


def draw_cardioid(svg, data: CardioidData):
    """ step draws """
    ###### draw big circle ########
    svg.draw(draw_ring(data.center[0], data.center[1], radius=data.radius,
                       stroke_color='black', stroke_width=1))

    ###### draw points on circle ########
    pts = data.points_on_circle
    drawPointsCircle_style(svg, pts, r=0.5, color='red', style_class='points')

    ###### draw lines ########
    if data.lines is not None:
        for start, stop in data.lines:
            points = [(pts[start][0], pts[start][1], pts[stop][0], pts[stop][1])]
            drawlinePoints(svg, points, color='green')


def drawCardioid_class(svg):
    """ draw by using class """
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    radius = 90
    divisions_n = 100
    multiplier = 2.2

    title = f'Cardioid Curve, parameters: divisions={divisions_n}, multiplier={multiplier}'
    svg.set_title(title)

    data = CardioidData(radius, (cx, cy), divisions_n, multiplier)
    draw_cardioid(svg, data)


def drawCardioid_class_mul(svg):
    """ draw mul cardioid """
    H, W = svg.get_size()
    svg.set_title('Cardioid Curve showing')
    r = H * 0.95 / 4
    draw_cardioid(svg, CardioidData(r, (W / 4, H / 4), 100, 2))
    draw_cardioid(svg, CardioidData(r, (W * 3 / 4, H / 4), 30, 1.1))
    draw_cardioid(svg, CardioidData(r, (W / 4, H * 3 / 4), 50, 0.2))
    draw_cardioid(svg, CardioidData(r, (W * 3 / 4, H * 3 / 4), 100, 1.8))


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'Cardioid.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # drawCardioid(svg, divisions_n=200, multiplier=2)
    # drawCardioid(svg, divisions_n=100, multiplier=0.2)
    # drawCardioid(svg, divisions_n=100, multiplier=1.2)
    # drawCardioid_class(svg)
    drawCardioid_class_mul(svg)


if __name__ == "__main__":
    main()
