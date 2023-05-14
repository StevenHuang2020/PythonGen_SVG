# -*- encoding: utf-8 -*-
# Date: 08/Feb/2022
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: SVG path tag
"""

import numpy as np
import random
from svg.file import SVGFileV2
from svg.basic import clip_float, random_color, random_color_hsv
from svg.basic import draw_path, draw_text, add_style, get_styles
from svg.basic import random_points, random_point
from svg.geo_transformation import translation_pts_xy, rotation_pts_xy, rotation_pts_xy_point
from svg.geo_transformation import zoom_pts_xy_point, zoom_pts_xy
from svg.geo_transformation import identity_trans, translation_pts_xy, translation_pts
from svg.geo_transformation import shear_points, reflection_points, split_points, transform_any_points
from svg.geo_math import get_5star

from common import gImageOutputPath
from svgFunction import funcSin
from svgAnimation import addNodeAnitmation
from svgImageMask import loadImg, OtsuMethodThresHold, showimage
from common_path import join_path


def split_string(src_str, delimiter=' ', length=24):
    new_str = ''
    str_list = src_str.split(delimiter)
    parts = [str_list[i:i + length] for i in range(0, len(str_list), length)]
    print('str_list=', str_list)
    print('parts=', parts, len(parts))
    for i in parts:
        new_str += (' '.join(i) + '\n')

    print('new_str=', new_str)
    return new_str


def draw_points_svg(svg, ptX, ptY, close=False, stroke=0.6, color=None, fillColor='transparent'):
    x = ptX[0]
    y = ptY[0]
    path = 'M %.1f %.1f L' % (x, y)
    for x, y in zip(ptX[1:], ptY[1:]):
        path = path + ' ' + str(clip_float(x)) + ' ' + str(clip_float(y))

    if close:
        path += ' Z'

    # color = color or random_color_hsv()
    return svg.draw(draw_path(path, stroke_width=stroke, color=color, fill_color=fillColor))


def draw_path_grid(svg, N=10, color='green', strokeWidth=0.2):
    H, W = svg.get_size()
    for i in range(N + 1):
        path = f'M{i*(W//N)} 0 V{H}'
        svg.draw(draw_path(path, stroke_width=strokeWidth, color=color))
        path = f'M0 {i*(H//N)} H{W}'
        svg.draw(draw_path(path, stroke_width=strokeWidth, color=color))


def draw_path_arrow(svg):
    path = 'M20 10 H50 V0 L 80 20 L 50 40 V30 H20 Z'
    svg.draw(draw_path(path, stroke_width=0.6, color='green', fill_color='green'))

    path = 'M10 40 h30 v-10 l30 20 l-30 20 v-10 h-30 Z'
    svg.draw(draw_path(path, stroke_width=0.6, color='green', fill_color='red'))

    path = 'M20 70 h30 v-10 l30 20 l-30 20 v-10 h-30 Z'
    svg.draw(draw_path(path, stroke_width=0.6, color='green', fill_color='yellow'))


def draw_path_star(svg):
    # path = 'M20 40 h60 l-50 35 l20 -55 l20 55 z'
    # svg.draw(draw_path(path, stroke_width=0.6, color='green', fill_color='none'))

    # path = 'M10 40 h80 l-65 45 l25 -75 l25 75 z'
    # svg.draw(draw_path(path, stroke_width=0.6, color='black', fill_color='none'))

    path = 'M10 40 h30 l10 -30 l10 30 h30 l-24 17 l9 28 l-25 -17 l-25 17 l9 -28 z'
    svg.draw(draw_path(path, stroke_width=0.6, color='red', fill_color='none'))


def draw_path_star2(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    pts = get_5star(R=70, r=30)
    # print('pts=', pts, pts.shape)

    x, y = split_points(pts)
    x, y = translation_pts_xy(x, y, (cx, cy))
    # print('x=', x)
    # print('y=', y)
    draw_points_svg(svg, x, y, color='green', close=True)


def svg_path_basic(svg):
    svg.set_background('#eeeeee')

    draw_path_grid(svg)
    # draw_path_arrow(svg)
    # draw_path_star(svg)
    draw_path_star2(svg)


def svg_path(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 400
    xoffset = 0.5
    x = np.linspace(xoffset, 10 - xoffset, N) * 10

    y = funcSin(x / 3) * 30
    x, y = translation_pts_xy(x, y, (0, cy))
    draw_points_svg(svg, x, y)

    x1, y1 = rotation_pts_xy_point(x, y, (0, cy), -1 * np.pi / 6)
    draw_points_svg(svg, x1, y1)
    x2, y2 = rotation_pts_xy_point(x, y, (0, cy), np.pi / 6)
    draw_points_svg(svg, x2, y2)


def svg_path2(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 400
    xoffset = 0.5
    x = np.linspace(xoffset, 10 - xoffset, N) * 20
    y = funcSin(x / 2) * 20

    for i in range(4):
        offsetY = i * H // 4 + 20 + 5
        ptx, pty = translation_pts_xy(x, y, (0, offsetY))

        stroke = clip_float(random.random() * 2)
        draw_points_svg(svg, ptx, pty, stroke=stroke)


def svg_path3(svg, anim=True):
    def drawStyleText(svg):
        styleDict = {}
        # styleDict['fill'] = 'black'
        styleDict['font-family'] = 'Consolas'
        styleDict['font-size'] = '10px'
        styleList = get_styles(styleDict)

        svg.draw(add_style('text', styleList))

    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 400
    xoffset = 0.2
    x = np.linspace(xoffset, 5 - xoffset, N) * 20
    y = funcSin(x / 0.6) * x / 3

    x, y = translation_pts_xy(x, y, (cx, cy))
    # draw_points_svg(svg, x, y)

    # drawStyleText(svg)
    # svg.draw(draw_text(5, 10, 'y=sin(x)'))

    N = 10
    for i in range(N):
        ptx, pty = rotation_pts_xy_point(x, y, (cx, cy), i * 2 * np.pi / N)
        node = draw_points_svg(svg, ptx, pty)

        if anim:
            animateTransDict = {}
            animateTransDict['attributeName'] = 'transform'
            animateTransDict['attributeType'] = 'xml'
            animateTransDict['type'] = 'rotate'
            animateTransDict['from'] = f'0 {cx} {cy}'
            animateTransDict['to'] = f'360 {cx} {cy}'
            animateTransDict['dur'] = '8s'
            animateTransDict["repeatCount"] = "indefinite"  # "5"

            addNodeAnitmation(svg, node, animateTransDict, elementName='animateTransform')


def svg_path4(svg):
    H, W = svg.get_size()
    # svg.set_background('#eeeeee')

    cx, cy = W // 2, H // 2
    pts = get_5star(R=20, r=10)
    pts = np.hsplit(pts, 2)
    x, y = pts[0].ravel(), pts[1].ravel()

    # draw one 5-pointed star
    # ptx, pty = translation_pts_xy(x, y, (cx, cy))
    # draw_points_svg(svg, ptx, pty, color='green', close=True)

    # draw random 5-pointed stars
    N = 30  # total points
    margin = 10  # margin to border
    pts = random_points((N, 2), min=10, max=W - margin)

    for pt in pts:
        ptx, pty = translation_pts_xy(x, y, (pt[0], pt[1]))
        draw_points_svg(svg, ptx, pty, color=random_color_hsv(), close=True)


def svg_path5(svg):
    H, W = svg.get_size()

    cx, cy = W // 2, H // 2
    pts = get_5star(R=40, r=10)
    pts = np.hsplit(pts, 2)
    x, y = pts[0].ravel(), pts[1].ravel()

    ptx, pty = translation_pts_xy(x, y, (cx, cy))

    times = 18
    for i in range(times):
        theta = i * (2 * np.pi / times)
        x, y = rotation_pts_xy_point(ptx, pty, (cx, cy), theta)
        draw_points_svg(svg, x, y, color='green', close=True)


def svg_path6(svg):
    H, W = svg.get_size()

    cx, cy = W // 2, H // 2
    pts = get_5star(R=12, r=8)
    pts = np.hsplit(pts, 2)
    x, y = pts[0].ravel(), pts[1].ravel()

    ptx, pty = translation_pts_xy(x, y, (cx, cy))

    times = 28
    for i in range(times):
        z = i**2 / 180  # i*0.5
        x, y = zoom_pts_xy_point(ptx, pty, (cx, cy), z)
        draw_points_svg(svg, x, y, color=random_color_hsv(), stroke=0.4, close=True)


def svg_path7(svg):
    H, W = svg.get_size()
    # dictStyle = {'stroke-width': "0.4", 'fill': "transparent"}
    # dictStyle = {'stroke-width': "0.4", 'fill': "transparent", 'stroke': "green"}
    dictStyle = {'stroke-width': "0.4", 'stroke': "green"}
    styleList = get_styles(dictStyle)
    svg.draw(add_style('path', styleList))

    cx, cy = W // 2, H // 2
    pts = get_5star(R=12, r=8)
    pts = np.hsplit(pts, 2)
    x, y = pts[0].ravel(), pts[1].ravel()

    ptx, pty = translation_pts_xy(x, y, (cx, cy))

    times = 68
    pts = random_points((times, 2), 0, W)
    for i in range(times):
        z = i / times

        x, y = zoom_pts_xy_point(ptx, pty, (pts[i][0], pts[i][1]), z)

        color = None  # random_color_hsv()
        draw_points_svg(svg, x, y, stroke=None, color=color, fillColor=random_color_hsv(), close=True)


def test_geo_transformation():
    x = np.array([1, 2, 5])
    y = np.array([3, 4, 6])
    print(x.shape)
    # new_x, new_y = translation_pts_xy(x, y, (1, 2))
    # translation_pts_xy(x,y,(-1.5,-3.5))

    N = 10
    pts = random_points((N, 2), min=1, max=10)
    print(pts, pts.shape)

    x, y = split_points(pts)

    # print('x, x.shape=', x, x.shape)
    # new_x, new_y = identity_trans(x, y)
    # new_x, new_y = translation_pts_xy(x, y, (1, -2))
    # new_x, new_y = translation_pts(pts, (1, -2))
    # new_x, new_y = rotation_pts_xy(x, y, 0)
    # new_x, new_y = zoom_pts_xy(x, y, 1.1)
    # new_x, new_y = shear_points(pts, 1)
    new_x, new_y = reflection_points(pts, 1)
    print('new_x =', new_x)
    print('new_y =', new_y)


def svg_transformation(svg):
    """basic transforms demonstration"""
    H, W = svg.get_size()

    pts = get_5star(R=9, r=6)
    print('pts=', pts, pts.shape)
    fillColor = 'green'  # random_color_hsv()
    stroke_w = 0.3
    stroke_color = None
    line_color = 'green'
    N = 5  # lines
    hinter = H // N
    text_w = 22
    start_w = (W - text_w) // 2
    text_x = 1
    text_y = 10
    fontsize = '3px'
    offet_x, offet_y = 15, 11

    # start to draw
    path = f'M{text_w} 0 V{H}'
    svg.draw(draw_path(path, stroke_width=stroke_w, color=line_color))

    # draw grid lines
    for i in range(N):
        path = f'M0 {i * hinter} h{W}'
        svg.draw(draw_path(path, stroke_width=stroke_w, color=line_color))

    # start translation
    txt = 'Translation:'
    svg.draw(draw_text(x=text_x, y=text_y, text=txt, fontsize=fontsize))

    x, y = split_points(pts)
    cx = text_w + offet_x
    cy = offet_y
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    cx += start_w
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    # start rotation
    text_y += hinter
    txt = 'Rotation:'
    svg.draw(draw_text(x=text_x, y=text_y, text=txt, fontsize=fontsize))

    cx = text_w + offet_x
    cy += hinter
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    cx += start_w
    px, py = rotation_pts_xy(x, y, np.pi / 6)
    px, py = translation_pts_xy(px, py, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    # start zoom
    text_y += hinter
    txt = 'Zoom:'
    svg.draw(draw_text(x=text_x, y=text_y, text=txt, fontsize=fontsize))

    cx = text_w + offet_x
    cy += hinter
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    cx += start_w
    px, py = zoom_pts_xy(x, y, 0.7)
    px, py = translation_pts_xy(px, py, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    # start shear
    text_y += hinter
    txt = 'Shear:'
    svg.draw(draw_text(x=text_x, y=text_y, text=txt, fontsize=fontsize))

    cx = text_w + offet_x
    cy += hinter
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    cx += start_w
    px, py = shear_points(pts, r=0.7)
    px, py = translation_pts_xy(px, py, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    # start reflection
    text_y += hinter
    txt = 'Reflection:'
    svg.draw(draw_text(x=text_x, y=text_y, text=txt, fontsize=fontsize))

    cx = text_w + offet_x
    cy += hinter
    px, py = translation_pts(pts, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)

    cx += start_w
    px, py = reflection_points(pts, reflectx=False)
    px, py = translation_pts_xy(px, py, (cx, cy))
    draw_points_svg(svg, px, py, stroke=None, color=stroke_color, fillColor=fillColor, close=True)


def svg_transformation_cust(svg):
    """custom transform"""
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    pts = get_5star(R=25, r=15)
    # print('pts=', pts, pts.shape)

    px, py = translation_pts(pts, (cx - 15, cy - 15))
    draw_points_svg(svg, px, py, stroke=None, color='green', fillColor='green', close=True)

    matrix = np.array([[0.2, 0.3],
                       [-1.2, 0.1]])

    px, py = transform_any_points(pts, matrix)
    px, py = translation_pts_xy(px, py, (cx + 15, cy + 15))
    draw_points_svg(svg, px, py, stroke=None, color='green', fillColor='green', close=True)


def main():
    file = join_path(gImageOutputPath, 'svgPath.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    svg_path_basic(svg)
    # svg_path(svg)
    # svg_path2(svg)
    # svg_path3(svg)
    # svg_path4(svg)
    # svg_path5(svg)
    # svg_path6(svg)
    # svg_path7(svg)
    # test_geo_transformation()
    # svg_transformation(svg)
    # svg_transformation_cust(svg)


if __name__ == "__main__":
    main()
