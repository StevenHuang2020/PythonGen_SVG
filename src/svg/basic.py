# -*- encoding: utf-8 -*-
# Date: 09/07/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Basic svg functions and svg node(string) generating functions.
"""

import random
import matplotlib as mpl
from matplotlib.pyplot import cm
import numpy as np
import string
import colorsys


def color_fader(c1='#000000', c2='#ffffff', mix=0):
    """fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)"""
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1 - mix) * c1 + mix * c2)


def random_color():
    """random a web hex color format"""
    return '#' + ''.join(random.sample('0123456789ABCDEF', 6))


def reverse_hex(color):
    """reverse web hex color, #FFFF00 -> #0000FF"""
    def is_hex_str(s):
        return set(s).issubset(string.hexdigits)

    if color.startswith('#'):
        color = color[1:]  # remove first '#'
        if is_hex_str(color) and len(color) <= 6:
            return '#' + hex(0xffffff - int(color, 16))[2:]
    return color


def random_color_hsv():
    """random a hex color, only random h value to get a brighter color"""
    h, s, v = random.random(), 1, 1
    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    return convert_rgb([int(x * 255) for x in float_rgb])


def rainbow_colors(N=255):
    res = []
    hsv_colors = cm.rainbow(np.linspace(0, 1, N))
    for i in hsv_colors:
        float_rgb = colorsys.hsv_to_rgb(i[0], i[1], i[2])  # h s v
        rgb = [int(x * 255) for x in float_rgb]
        c = convert_rgb(rgb)
        res.append(c)
    return res


def convert_rgb(rgb):
    """covert from rgb to hex color"""
    return "#{0:02x}{1:02x}{2:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def clip_float(x, n=1):
    if isinstance(x, float):
        return round(x, n)
    return x


def rand_str(num=6):
    """random string as ID"""
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


def random_points(size=(1, 2), min=0, max=5):
    """get random points, size=(N, 2) to get N points(x,y) """
    return np.random.random(size) * (max - min) + min  # [0,5)


def random_point(min=0, max=5):
    """get one random point"""
    return random_points((2,), min=min, max=max)


def get_grid_coordinates(W, H, vNum=2, hNum=2):
    hInter = W // hNum
    vInter = H // vNum
    base = []
    for i in range(hNum):
        for j in range(vNum):
            base.append([i*hInter, j*vInter])
    return np.array(base)


def uniform_random_points(W, H, vNum=2, hNum=2, x_offset=2, y_offset=2):
    """get uniform position random points"""
    hInter = W // hNum
    vInter = H // vNum

    base = get_grid_coordinates(W, H, vNum, hNum)

    x = random_points((hNum*vNum, 1), min=x_offset, max=hInter-x_offset)
    y = random_points((hNum*vNum, 1), min=y_offset, max=vInter-y_offset)

    pts = np.concatenate((x, y), axis=1)
    return base + pts


def get_styles(style_dict):
    """get style list form dictionary, for <style /> element in svg"""
    style_list = ''
    for key, value in style_dict.items():
        style_list = style_list + (key + ': ' + str(value) + '; ')
    return style_list


# ------------------------------draw function--------------------------------- #
def draw_line(x, y, x2, y2, stroke_width=0.5, color='black', stroke_dasharray='None'):
    """Draw a line for svg"""
    return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" \
        stroke-width="{stroke_width}" stroke-dasharray="{stroke_dasharray}" />'


def draw_rect(x, y, width, height, stroke_width=0.5, color=None, stroke_color=None):
    """Draw a rectangle for svg"""
    color = color or random_color()
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" \
        fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_width}" />'


def draw_circle(x, y, radius, color='black'):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" />'


def draw_ring(x, y, radius, color='transparent', stroke_color='black', stroke_width=0.5):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" stroke-width="{stroke_width}" \
            stroke="{stroke_color}" fill="{color}" />'


def draw_ellipse(cx, cy, rx, ry, color='transparent', stroke_color='black', stroke_width=0.5):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" \
        stroke="{stroke_color}" fill="{color}" stroke-width="{stroke_width}"/>'


def draw_polyline(points, color=None, stroke_color=None, stroke_width=1.0):
    return f'<polyline points="{points}" stroke="{stroke_color}" \
        stroke-width="{stroke_width}" fill="{color}" />'


def draw_polygon(points, color=None, stroke_color=None, stroke_width=1.0):
    return f'<polygon points="{points}" stroke="{stroke_color}" \
        stroke-width="{stroke_width}" fill="{color}" />'


def draw_text(x, y, text, font='Consolas', fontsize='smaller',
              color='black', blank_space='pre'):
    # xml:space deprecated.
    # white-space: normal,pre,nowrap,pre-wrap,break-spaces,pre-line
    return f'<text x="{x}" y="{y}" fill="{color}" white-space="{blank_space}" \
        font-family="{font}" font-size="{fontsize}" font-style="normal" \
            font-variant="normal">{text}</text>'


def draw_text_only(x, y, text):
    return f'<text x="{x}" y="{y}" >{text}</text>'


def draw_path(path, stroke_width=30, color='black', fill_color='transparent', fill_rule='nonzero'):
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
    # M 100 306 C 168 444, 304 444, 352 306
    return f'<path stroke="{color}" stroke-width="{stroke_width}" fill="{fill_color}" \
        fill-rule="{fill_rule}" d="{path}" />'


def add_style(tag, style_list):
    return '<style> %s { %s } </style>' % (tag, style_list)


def add_style_path(stroke='black', stroke_width=1, fill='transparent'):
    style = f'stroke: {stroke}; stroke-width: {stroke_width}; fill: {fill};'
    return add_style(tag='path', style_list=style)


def draw_only_path(path):
    return draw_any('path', d=f'{path}')


def draw_tag(tag, text=None):
    return draw_any(tag, text)


def draw_any(tag, text=None, **kwargs):
    """Draw any tag
    Usage examples:
    draw_any(tagName, text, attr1=anything, attr2=anything, ...) or
    draw_any(tagName, text, **attrDict)
    """

    attri_list = [(str(key) + '=' + '"' + str(value) + '"')
                  for key, value in kwargs.items()]
    attris = ' '.join(attri_list)
    # print('attris=', attris)
    if text is not None:
        return "<{} {}>{}</{}>".format(tag, attris, text, tag)
    return "<{} {} />".format(tag, attris)
