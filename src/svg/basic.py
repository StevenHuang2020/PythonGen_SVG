# -*- encoding: utf-8 -*-
# Date: 09/07/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Basic svg functions and svg node(string) generating functions.
"""

import random
import string
import colorsys
import matplotlib as mpl
from matplotlib.pyplot import cm
import numpy as np


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
    """ get rainbow colors """
    res = []
    hsv_colors = cm.rainbow(np.linspace(0, 1, N))
    for i in hsv_colors:
        float_rgb = colorsys.hsv_to_rgb(i[0], i[1], i[2])  # h s v
        rgb = [int(x * 255) for x in float_rgb]
        c = convert_rgb(rgb)
        res.append(c)
    return res


def convert_rgb(rgb, alpha=0xff):
    """covert from rgb to hex color"""
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}{alpha:02x}'


def clip_float(x, n=1):
    """ clip float number """
    if isinstance(x, float):
        return round(x, n)
    return x


def clip_floats(x, n=1):
    """ numpy clip float numbers """
    return np.round(x, n)


def rand_str(num=6):
    """random string as ID"""
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


def random_points(size=(1, 2), a=0, b=5, decimal=2):
    """get random points, size=(N, 2) to get N points(x, y) """
    pts = np.random.random(size) * (b - a) + a  # [a, b)
    return np.round(pts, decimals=decimal)


def random_point(a=0, b=5):
    """get one random point"""
    return random_points((2,), a, b)


def grid_xy(xMin, xMax, yMin, yMax, N=10):
    """ grid points """
    return random_coordinates(xMin, xMax, yMin, yMax, N)


def random_coordinates(xMin, xMax, yMin, yMax, N=100):
    """generate random points  """
    x = random_points((N, 1), xMin, xMax)
    y = random_points((N, 1), yMin, yMax)
    return np.concatenate((x, y), axis=1)


def mesh_grid_xy(xMin, xMax, yMin, yMax, N=10):
    """ get mesh graid points """
    # x = np.linspace(xMin, xMax, N)
    # y = np.linspace(yMin, yMax, N)
    x = random_points((N, 1), xMin, xMax).flatten()
    y = random_points((N, 1), yMin, yMax).flatten()
    # x = np.sort(x)
    # y = np.sort(y)

    # print('x=', x)
    # print('y=', y)
    xv, yv = np.meshgrid(x, y)
    xv = xv.flatten().reshape((N * N, 1))
    yv = yv.flatten().reshape((N * N, 1))
    # print('xv=', xv)
    # print('yv=', yv)
    return np.hstack((xv, yv))


def get_grid_coordinates(W, H, v_num=2, h_num=2):
    """ get grid coorinates of svg """
    h_inter = W // h_num
    v_inter = H // v_num
    base = []
    for i in range(h_num):
        for j in range(v_num):
            base.append([i * h_inter, j * v_inter])
    return np.array(base)


def uniform_random_points(W, H, v_num=2, h_num=2, x_offset=2, y_offset=2):
    """get uniform position random points"""
    h_inter = W // h_num
    v_inter = H // v_num

    base = get_grid_coordinates(W, H, v_num, h_num)

    x = random_points((h_num * v_num, 1), a=x_offset, b=h_inter - x_offset)
    y = random_points((h_num * v_num, 1), a=y_offset, b=v_inter - y_offset)

    pts = np.concatenate((x, y), axis=1)
    return base + pts


def get_styles(style_dict):
    """get style list form dictionary, for <style /> element in svg"""
    style_list = ''
    for key, value in style_dict.items():
        style_list = style_list + (key + ': ' + str(value) + '; ')
    return style_list


# ------------------------------draw function--------------------------------- #
SVG_ELEMENTS_NAMES = ['a', 'animate', 'animateMotion>', 'circle', 'defs', 'ellipse',
                      'path', 'line', 'rect', 'ellipse', 'polyline', 'polygon', 'text', 'style']


def is_element_name(name):
    """ check elements name """
    return name in SVG_ELEMENTS_NAMES


def draw_line(x1, y1, x2, y2, stroke_width=0.5, color='black', stroke_dasharray='None'):
    """Draw a line with style for svg"""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" \
        stroke-width="{stroke_width}" stroke-dasharray="{stroke_dasharray}" />'


def draw_line_stroke_width(x1, y1, x2, y2, stroke_width=0.5):
    """Draw a line with stroke_width for svg"""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"\
        stroke-width="{stroke_width}"  />'


def draw_only_line(x1, y1, x2, y2):
    """Draw a line for svg"""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'


def draw_rect(x, y, width, height, stroke_width=0.5, color=None, stroke_color=None):
    """Draw a rectangle for svg"""
    color = color or random_color()
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" \
        fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_width}" />'


def draw_circle(x, y, radius, color='black'):
    """ draw circle """
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" />'


def draw_only_circle(x, y, class_name=None):
    """ draw circle """
    if class_name is None or is_element_name(class_name):
        return f'<circle cx="{x}" cy="{y}" />'
    return f'<circle class="{class_name}" cx="{x}" cy="{y}" />'


def draw_ring(x, y, radius, color='transparent', stroke_color='black', stroke_width=0.5):
    """ draw ring """
    return f'<circle cx="{x}" cy="{y}" r="{radius}" stroke-width="{stroke_width}" \
            stroke="{stroke_color}" fill="{color}" />'


def draw_ellipse(cx, cy, rx, ry, color='transparent', stroke_color='black', stroke_width=0.5):
    """ draw ellipse """
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" \
        stroke="{stroke_color}" fill="{color}" stroke-width="{stroke_width}"/>'


def draw_polyline(points, color=None, stroke_color=None, stroke_width=1.0):
    """ draw polyline """
    return f'<polyline points="{points}" stroke="{stroke_color}" \
        stroke-width="{stroke_width}" fill="{color}" />'


def draw_polygon(points, color=None, stroke_color=None, stroke_width=1.0):
    """ draw polygon """
    return f'<polygon points="{points}" stroke="{stroke_color}" \
        stroke-width="{stroke_width}" fill="{color}" />'


def draw_text(x=0, y=0, text='', font='Consolas', fontsize='smaller',
              color='black', blank_space='pre'):
    """ draw text """
    # xml:space deprecated.
    # white-space: normal,pre,nowrap,pre-wrap,break-spaces,pre-line
    dict_text = {}
    dict_text['x'] = str(x)
    dict_text['y'] = str(y)
    dict_text['fill'] = color
    dict_text['white-space'] = blank_space
    dict_text['font-family'] = font
    dict_text['font-size'] = fontsize
    dict_text['font-style'] = 'normal'
    dict_text['font-variant'] = 'normal'
    return draw_any('text', text, **dict_text)


def draw_text_only(x, y, text):
    """ draw text """
    return f'<text x="{x}" y="{y}" >{text}</text>'


def draw_path(path, stroke_width=30, color='black', fill_color='transparent', fill_rule='nonzero'):
    """ draw path """
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
    # M 100 306 C 168 444, 304 444, 352 306
    return f'<path stroke="{color}" stroke-width="{stroke_width}" fill="{fill_color}" \
        fill-rule="{fill_rule}" d="{path}" />'


def add_style(tag, style_list):
    """ add style """
    return f'<style>{style_content(tag, style_list)}</style>'  # % (tag, style_list)


def style_content(tag, style_list):
    """ style format """
    tmp = "{" + style_list + "}"
    return f' {tag}{tmp}'


def add_style_path(stroke='black', stroke_width=1, fill='transparent'):
    """ add path style """
    style = f'stroke: {stroke}; stroke-width: {stroke_width}; fill: {fill};'
    return add_style(tag='path', style_list=style)


def draw_only_path(path):
    """ draw path """
    return draw_any('path', d=f'{path}')


def draw_tag(tag, text=None):
    """ draw path """
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
        return f"<{tag} {attris}>{text}</{tag}>"
    return f"<{tag} {attris} />"


def text_style(color='black', font='Consolas', font_size='12px', style='normal', variant='normal',
               white_space='pre', baseline='middle', anchor='middle'):
    """ text style dict """
    style_dict = {}

    if color is None:
        color = random_color()

    style_dict['fill'] = color
    style_dict['font-family'] = font
    style_dict['font-size'] = font_size
    style_dict['font-style'] = style
    style_dict['font-variant'] = variant
    # style_dict['xml:space'] = 'preserve' #deprecated
    style_dict['white-space'] = white_space
    style_dict['dominant-baseline'] = baseline
    style_dict['text-anchor'] = anchor
    return style_dict


def line_style(color='black', stroke_width=0.5, stroke_dasharray='None'):
    """ line style dict """
    style_dict = {}

    if color is None:
        color = random_color()

    style_dict['stroke'] = color
    style_dict['stroke-width'] = str(stroke_width)
    style_dict['stroke-dasharray'] = stroke_dasharray  # '0 1' '4' '4 1'
    return style_dict


def transfrom_dict(from_x, from_y, to_x, to_y, trans_type='rotate', dur=1):
    """ transform fict """
    trans_dict = {}
    trans_dict['attributeName'] = 'transform'
    trans_dict['attributeType'] = 'xml'
    trans_dict['type'] = trans_type
    trans_dict['from'] = f'0 {from_x} {from_y}'
    trans_dict['to'] = f'360 {to_x} {to_y}'
    trans_dict['dur'] = f'{dur}s'
    trans_dict["repeatCount"] = "indefinite"  # "5"
    return trans_dict


def main():
    """ main function """
    print(random_color_hsv())

    x = '{china}'
    f = f'i am a {x}'
    print('f=', f)
    print('list=', add_style('abc', 'a:1; b:2; ft:10pt;'))
    print('text=', draw_text(text='hi'))


if __name__ == '__main__':
    main()
