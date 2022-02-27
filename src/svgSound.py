"""
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Sound visualization
# Date: 28/Oct/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License
"""
import numpy as np
# import matplotlib.pyplot as plt
from svg.file import SVGFileV2
from svg.basic import rainbow_colors
from svgPointLine import drawlinePoints  # drawlinePointsContinus
from svgPointLine import drawlinePointsContinusRainbow, drawPathContinuPoints
from common import gImageOutputPath
# from svg.geo_transformation import translation_pts_xy
import math


# signed 16bit pcm, little-endian 1channel, sample rate 8000HZ
def readSound(file=r'./res/test_signed16_SR8000HZ.pcm', N=200):
    data = np.memmap(file, dtype=np.short, mode='r')
    data = data[:N]
    print(type(data), data.shape, data)
    print('min,max=', np.min(data), np.max(data))
    # plt.plot(data)
    # plt.show()
    return data


def drawSoundGrapic(svg, data):
    W, H = svg.get_size()
    cx, cy = W // 2, H // 2

    data = H // 2 - data // 400  # shrink sound value to a range that svg can show
    print('data=', data, np.min(data), np.max(data))
    pts = []

    # print('pts=', pts)
    xScale = 55
    if 0:  # style 1
        for i in range(len(data) - 1):
            pts.append((i / xScale, data[i], (i + 1) / xScale, data[i + 1]))
        drawlinePoints(svg, pts)

    elif 1:  # style 2, rainbow color
        totlal = len(data)
        if 1:
            for i in range(totlal):
                pts.append((i / xScale, data[i]))
        else:
            R = 120
            data = data - H // 2
            maxV = np.max(data)
            for i in range(totlal):
                angle = i * 2 * np.pi / totlal
                r = R * math.fabs(data[i]) / maxV
                x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
                # print("x, y=", x, y)
                # x, y = translation_pts_xy(x, y, (cx,cy))
                pts.append((x, y))

            # print('pts=', pts)

        if 0:  # rainbowcolor and draw line
            colors = []
            c = rainbow_colors(N=W)
            for pt in pts:
                x, y = pt
                colors.append(c[int(x) % W])
            drawlinePointsContinusRainbow(svg, pts, colors=colors)
        else:  # draw path
            drawPathContinuPoints(svg, pts, strokeWidth=0.2)


def main():
    data = readSound(N=-1)
    file = gImageOutputPath + r'\soundGraphic.svg'
    svg = SVGFileV2(file, W=500, H=200, border=True)
    drawSoundGrapic(svg, data)


if __name__ == "__main__":
    main()
