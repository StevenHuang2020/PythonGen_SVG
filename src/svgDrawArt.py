# -*- encoding: utf-8 -*-
# Date: 25/Jun/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Draw examples
"""""""""""""""""""""""""""""""""""""""""""""""""""""

import random
import numpy as np
from svg.basic import draw_circle, draw_line, draw_rect, random_color
from svg.file import SVGFileV2
from common import IMAGE_OUTPUT_PATH
from common_path import join_path


def draw_circleRings(x, y, radius, rings=5, color=None, fill_color='white'):
    """Draw circles rings for svg"""
    for _ in range(rings):
        r = random.randint(1, rings) * radius / (rings + 1)
        stroke_w = random.choice([1, 1, 1, 2, 2, 3])
        color = color or random_color()
        yield f'<circle cx="{x}" cy="{y}" r="{r}" stroke-width="{stroke_w}" \
            stroke="{color}" fill="{fill_color}" />'


class DrawArt:
    styles = ['Line', 'DiagLine', 'Rectangle', 'Circle', 'Rings']

    def __init__(self, svg=None):
        self.svg = svg

    def DrawCircleByPt(self, pt1, pt2, pt3, pt4, circle=True):
        pt_center = np.array([(pt1[0] + pt3[0]) / 2, (pt1[1] + pt3[1]) / 2])
        r = abs(pt_center[0] - pt1[0])

        if circle:
            rings = 4
            r = random.choice(range(1, rings)) * r / rings
            self.svg.draw(draw_circle(pt_center[0], pt_center[1], r))
        else:
            for i in draw_circleRings(pt_center[0], pt_center[1], r):
                self.svg.draw(i)

    def DrawLineByPt(self, start_pt, stop_pt):
        if start_pt[0] > stop_pt[0]:  # switch
            start_pt = start_pt + stop_pt
            stop_pt = start_pt - stop_pt
            start_pt = start_pt - stop_pt
        self.svg.draw(draw_line(start_pt[0], start_pt[1], stop_pt[0], stop_pt[1]))

    def DrawRectangleByPt(self, start_pt, stop_pt):
        if start_pt[0] > stop_pt[0]:  # switch
            start_pt = start_pt + stop_pt
            stop_pt = start_pt - stop_pt
            start_pt = start_pt - stop_pt
        self.svg.draw(draw_rect(start_pt[0], start_pt[1], stop_pt[0] - start_pt[0],
                                stop_pt[1] - start_pt[1]))

    def drawDiagLine(self, pt1, pt2, pt3, pt4, pt_center, style, N):
        a = [0, 1]
        if N == 1:
            if random.choice(a):
                self.DrawLineByPt(pt1, pt3)
            else:
                self.DrawLineByPt(pt2, pt4)

        self.plotArt(pt1, pt_center, N - 1, style=style)
        self.plotArt(pt2, pt_center, N - 1, style=style)
        self.plotArt(pt3, pt_center, N - 1, style=style)
        self.plotArt(pt4, pt_center, N - 1, style=style)

    def drawLine(self, pt1, pt2, pt3, pt4, pt_center, style, N):
        a = [0, 1]
        if N == 1:
            if random.choice(a):
                self.DrawLineByPt(pt1, pt2)
            if random.choice(a):
                self.DrawLineByPt(pt2, pt3)
            if random.choice(a):
                self.DrawLineByPt(pt3, pt4)
            if random.choice(a):
                self.DrawLineByPt(pt1, pt4)

        self.plotArt(pt1, pt_center, N - 1, style=style)
        self.plotArt(pt2, pt_center, N - 1, style=style)
        self.plotArt(pt3, pt_center, N - 1, style=style)
        self.plotArt(pt4, pt_center, N - 1, style=style)

    def drawRectangle(self, pt1, pt2, pt3, pt4, pt_center, style, N):
        # a = [0, 1]
        if N == 1:
            # if random.choice(a):
            self.DrawRectangleByPt(pt1, pt3)

        self.plotArt(pt1, pt_center, N - 1, style=style)
        self.plotArt(np.array([pt_center[0], pt2[1]]), np.array([pt2[0], pt_center[1]]),
                     N - 1, style=style)
        self.plotArt(pt3, pt_center, N - 1, style=style)
        self.plotArt(np.array([pt4[0], pt_center[1]]), np.array([pt_center[0], pt4[1]]),
                     N - 1, style=style)

    def drawCircle(self, pt1, pt2, pt3, pt4, pt_center, style, N, circle=True):
        # a = [0, 1]
        if N == 1:
            # if random.choice(a):
            self.DrawCircleByPt(pt1, pt2, pt3, pt4, circle=circle)

        self.plotArt(pt1, pt_center, N - 1, style=style)
        self.plotArt(np.array([pt_center[0], pt2[1]]), np.array([pt2[0], pt_center[1]]),
                     N - 1, style=style)
        self.plotArt(pt3, pt_center, N - 1, style=style)
        self.plotArt(np.array([pt4[0], pt_center[1]]), np.array([pt_center[0], pt4[1]]),
                     N - 1, style=style)

    def plotArt(self, start_pt, stop_pt, N, style):
        if N > 0:
            if start_pt[0] > stop_pt[0]:  # switch
                start_pt = start_pt + stop_pt
                stop_pt = start_pt - stop_pt
                start_pt = start_pt - stop_pt

            pt1 = start_pt
            pt2 = np.array([stop_pt[0], start_pt[1]])
            pt3 = stop_pt
            pt4 = np.array([start_pt[0], stop_pt[1]])
            pt_center = np.array([(start_pt[0] + stop_pt[0]) / 2, (start_pt[1] + stop_pt[1]) / 2])

            if style == self.styles[0]:
                self.drawLine(pt1, pt2, pt3, pt4, pt_center, style, N)
            elif style == self.styles[1]:
                self.drawDiagLine(pt1, pt2, pt3, pt4, pt_center, style, N)
            elif style == self.styles[2]:
                self.drawRectangle(pt1, pt2, pt3, pt4, pt_center, style, N)
            elif style == self.styles[3]:
                self.drawCircle(pt1, pt2, pt3, pt4, pt_center, style, N)
            elif style == self.styles[4]:
                self.drawCircle(pt1, pt2, pt3, pt4, pt_center, style, N, circle=False)
            else:
                print('Not handled!')
        else:
            return


def drawArtSvg():
    styles = DrawArt().styles

    recurse = [4, 5]
    for N in recurse:
        for style in styles:
            file_name = 'art_' + style + '_' + str(N) + '.svg'
            file = join_path(IMAGE_OUTPUT_PATH, file_name)
            H, W = 200, 200
            svg = SVGFileV2(file, W, H)
            draw = DrawArt(svg)
            draw.plotArt(np.array([0, 0]), np.array([W, H]), N=N, style=style)
