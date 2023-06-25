"""
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Sound visualization
# Date: 28/Oct/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License
"""
import math
import numpy as np
from svg.file import SVGFileV2
from svg.basic import rainbow_colors
from svgPointLine import drawlinePoints
from svgPointLine import drawPathContinuPoints, drawlinePointsContinusRainbow
from common import IMAGE_OUTPUT_PATH
from common_path import join_path

# signed 16bit pcm, little-endian 1channel, sample rate 8000HZ


def readSoundData(file, N=-1):
    """ read sound pcm file """
    data = np.memmap(file, dtype=np.short, mode='r')
    data = data[:N]
    print(type(data), data.shape, data)
    print('min,max=', np.min(data), np.max(data))
    # plt.plot(data)
    # plt.show()
    return data


def drawSoundGrapic(svg, data):
    """ draw sound wave data """
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    data = H // 2 - data // 400  # shrink sound value into a range that svg can show
    print('data, min, max=', data, np.min(data), np.max(data))
    pts = []

    x_scale = 55
    if 0:
        for i in range(len(data) - 1):
            pts.append((i / x_scale, data[i], (i + 1) / x_scale, data[i + 1]))
        # drawlinePoints(svg, pts)  # style 1
        drawlinePoints(svg, pts, styles_opt=False)

    elif 1:
        totlal = len(data)
        if 1:
            for i in range(totlal):
                pts.append((i / x_scale, data[i]))
        else:
            R = 120
            data = data - H // 2
            max_v = np.max(data)
            for i in range(totlal):
                angle = i * 2 * np.pi / totlal
                r = R * math.fabs(data[i]) / max_v
                x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
                pts.append((x, y))

        drawPathContinuPoints(svg, pts, stroke_width=0.2)  # style 2


def main():
    """ main function """
    data = readSoundData(file=r'./res/test_signed16_SR8000HZ.pcm')
    file = join_path(IMAGE_OUTPUT_PATH, r'soundGraphic.svg')
    svg = SVGFileV2(file, W=500, H=200, border=True)
    drawSoundGrapic(svg, data)


if __name__ == "__main__":
    main()
