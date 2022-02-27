import os
import numpy as np
import random
from svg.basic import draw_circle, draw_line, draw_rect, random_color
from svg.file import SVGFileV2
from common import gImageOutputPath

def draw_circleRings(x, y, radius, rings=5, color=None, fillColor='white'):
    """Draw circles rings for svg"""
    for _ in range(rings):
        r = random.randint(1, rings) * radius / (rings + 1)
        sw = random.choice([1, 1, 1, 2, 2, 3])
        color = color or random_color()
        yield f'<circle cx="{x}" cy="{y}" r="{r}" stroke-width="{sw}" \
            stroke="{color}" fill="{fillColor}" />'


class DrawArt:
    styles = ['Line', 'DiagLine', 'Rectangle', 'Circle', 'Rings']

    def __init__(self, svg=None):
        self.svg = svg

    def DrawCircleByPt(self, pt1, pt2, pt3, pt4, circle=True):
        ptCenter = np.array([(pt1[0] + pt3[0]) / 2, (pt1[1] + pt3[1]) / 2])
        r = abs(ptCenter[0] - pt1[0])

        if circle:
            rings = 4
            r = random.choice(range(1, rings)) * r / rings
            self.svg.draw(draw_circle(ptCenter[0], ptCenter[1], r))
        else:
            for i in draw_circleRings(ptCenter[0], ptCenter[1], r):
                self.svg.draw(i)

    def DrawLineByPt(self, startPt, stopPt):
        if startPt[0] > stopPt[0]:  # switch
            startPt = startPt + stopPt
            stopPt = startPt - stopPt
            startPt = startPt - stopPt
        self.svg.draw(draw_line(startPt[0], startPt[1], stopPt[0], stopPt[1]))

    def DrawRectangleByPt(self, startPt, stopPt):
        if startPt[0] > stopPt[0]:  # switch
            startPt = startPt + stopPt
            stopPt = startPt - stopPt
            startPt = startPt - stopPt
        self.svg.draw(draw_rect(startPt[0], startPt[1], stopPt[0] - startPt[0], stopPt[1] - startPt[1]))

    def drawDiagLine(self, pt1, pt2, pt3, pt4, ptCenter, style, N):
        a = [0, 1]
        if N == 1:
            if random.choice(a):
                self.DrawLineByPt(pt1, pt3)
            else:
                self.DrawLineByPt(pt2, pt4)

        self.plotArt(pt1, ptCenter, N - 1, style=style)
        self.plotArt(pt2, ptCenter, N - 1, style=style)
        self.plotArt(pt3, ptCenter, N - 1, style=style)
        self.plotArt(pt4, ptCenter, N - 1, style=style)

    def drawLine(self, pt1, pt2, pt3, pt4, ptCenter, style, N):
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

        self.plotArt(pt1, ptCenter, N - 1, style=style)
        self.plotArt(pt2, ptCenter, N - 1, style=style)
        self.plotArt(pt3, ptCenter, N - 1, style=style)
        self.plotArt(pt4, ptCenter, N - 1, style=style)

    def drawRectangle(self, pt1, pt2, pt3, pt4, ptCenter, style, N):
        a = [0, 1]
        if N == 1:
            # if random.choice(a):
            self.DrawRectangleByPt(pt1, pt3)

        self.plotArt(pt1, ptCenter, N - 1, style=style)
        self.plotArt(np.array([ptCenter[0], pt2[1]]), np.array([pt2[0], ptCenter[1]]), N - 1, style=style)
        self.plotArt(pt3, ptCenter, N - 1, style=style)
        self.plotArt(np.array([pt4[0], ptCenter[1]]), np.array([ptCenter[0], pt4[1]]), N - 1, style=style)

    def drawCircle(self, pt1, pt2, pt3, pt4, ptCenter, style, N, circle=True):
        a = [0, 1]
        if N == 1:
            # if random.choice(a):
            self.DrawCircleByPt(pt1, pt2, pt3, pt4, circle=circle)

        self.plotArt(pt1, ptCenter, N - 1, style=style)
        self.plotArt(np.array([ptCenter[0], pt2[1]]), np.array([pt2[0], ptCenter[1]]), N - 1, style=style)
        self.plotArt(pt3, ptCenter, N - 1, style=style)
        self.plotArt(np.array([pt4[0], ptCenter[1]]), np.array([ptCenter[0], pt4[1]]), N - 1, style=style)

    def plotArt(self, startPt, stopPt, N, style):
        if N > 0:
            if startPt[0] > stopPt[0]:  # switch
                startPt = startPt + stopPt
                stopPt = startPt - stopPt
                startPt = startPt - stopPt

            pt1 = startPt
            pt2 = np.array([stopPt[0], startPt[1]])
            pt3 = stopPt
            pt4 = np.array([startPt[0], stopPt[1]])
            ptCenter = np.array([(startPt[0] + stopPt[0]) / 2, (startPt[1] + stopPt[1]) / 2])

            if style == self.styles[0]:
                self.drawLine(pt1, pt2, pt3, pt4, ptCenter, style, N)
            elif style == self.styles[1]:
                self.drawDiagLine(pt1, pt2, pt3, pt4, ptCenter, style, N)
            elif style == self.styles[2]:
                self.drawRectangle(pt1, pt2, pt3, pt4, ptCenter, style, N)
            elif style == self.styles[3]:
                self.drawCircle(pt1, pt2, pt3, pt4, ptCenter, style, N)
            elif style == self.styles[4]:
                self.drawCircle(pt1, pt2, pt3, pt4, ptCenter, style, N, circle=False)
            else:
                print('Not handled!')
        else:
            return


def drawArtSvg():
    styles = DrawArt().styles

    recurse = [4, 5]
    for N in recurse:
        for style in styles:
            fileName = 'art_' + style + '_' + str(N) + '.svg'
            file = os.path.join(gImageOutputPath, fileName)
            H, W = 200, 200
            svg = SVGFileV2(file, W, H)
            draw = DrawArt(svg)
            draw.plotArt(np.array([0, 0]), np.array([W, H]), N=N, style=style)
