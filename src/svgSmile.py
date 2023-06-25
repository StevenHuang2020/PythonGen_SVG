# -*- encoding: utf-8 -*-
# Date: 14/Sep/2021
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: svg smile emoji drawing
"""""""""""""""""""""""""""""""""""""""""""""""""""""
from svg.file import SVGFileV2
from svg.basic import draw_circle, draw_path
from common import IMAGE_OUTPUT_PATH
from common_path import join_path


def drawSmileSVG(svg, radius, offsetX=0, offsetY=0, color=None):
    return drawSmileSVGNode(svg, node=None, radius=radius, offsetX=offsetX,
                            offsetY=offsetY, color=color)


def drawSmileSVGNode(svg, node, radius, offsetX=0, offsetY=0, color=None):
    x = radius + offsetX
    y = radius + offsetY
    color = color or '#FFC10E'
    svg.draw_node(node, draw_circle(x, y, radius, color=color))

    x = radius * 0.67 + offsetX
    y = radius * 0.66 + offsetY
    r = radius * 0.16
    svg.draw_node(node, draw_circle(x, y, r, color='#333333'))  # left eye

    x = 2 * radius - x + 2 * offsetX
    svg.draw_node(node, draw_circle(x, y, r, color='#333333'))  # right eye

    start_pt = [0.40 * radius + offsetX, 1.05 * radius + offsetY]
    stop_pt = [2 * radius - start_pt[0] + 2 * offsetX, start_pt[1]]
    # Bézier Curves control points
    cp1 = [0.6 * radius + offsetX, 1.78 * radius + offsetY]
    # Bézier Curves control points
    cp2 = [2 * radius - cp1[0] + 2 * offsetX, cp1[1]]

    path = f'M {start_pt[0]} {start_pt[1]} C {cp1[0]} {cp1[1]}, {cp2[0]} {cp2[1]}, { stop_pt[0]} {stop_pt[1]}'

    color = 'black'
    line_width = 0.11 * radius
    svg.draw_node(node, draw_path(
        path, stroke_width=line_width, color=color))  # mouth

    svg.draw_node(node, draw_circle(
        start_pt[0], start_pt[1], line_width / 2, color=color))
    svg.draw_node(node, draw_circle(
        stop_pt[0], stop_pt[1], line_width / 2, color=color))


def testSmile():
    file = join_path(IMAGE_OUTPUT_PATH, r'smileC.svg')
    s = SVGFileV2(file, W=300, H=300)
    drawSmileSVG(s, radius=100, offsetX=20, offsetY=45)


def testSmile2():
    file = join_path(IMAGE_OUTPUT_PATH, r'smileC2.svg')
    N = 6
    inter = 5
    offsetX = 0
    offsetY = 0
    r0 = 10

    total_w = N * (N - 1) * r0 + N * inter + offsetX
    total_h = (N - 1) * 2 * r0 + offsetY

    svg = SVGFileV2(file, W=total_w, H=total_h)

    for i in range(1, N):
        r = i * r0
        drawSmileSVG(svg, radius=r, offsetX=offsetX, offsetY=offsetY)
        offsetX += (2 * r + inter)


def testSmile3():
    file = join_path(IMAGE_OUTPUT_PATH, r'smileC3.svg')

    H, W = 6, 6
    inter = 5
    offsetX = 0
    offsetY = 0
    r0 = 20

    total_w = W * 2 * r0 + W * inter + offsetX
    total_h = H * 2 * r0 + H * inter + offsetY

    svg = SVGFileV2(file, W=total_w, H=total_h)

    for i in range(H):
        for j in range(W):
            r = r0
            offsetX = j * (2 * r + inter)
            offsetY = i * (2 * r + inter)

            # drawSmileSVG(svg,radius = r,offsetX=offsetX,offsetY=offsetY,color=random_color())
            drawSmileSVG(svg, radius=r, offsetX=offsetX,
                         offsetY=offsetY, color='#FFC10E')


def main():
    """ main function """
    # testSmile()
    # testSmile2()
    testSmile3()


if __name__ == '__main__':
    main()
