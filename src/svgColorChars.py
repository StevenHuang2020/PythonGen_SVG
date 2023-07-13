# -*- encoding: utf-8 -*-
# Date: 09/Jul/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Color characters
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
from svg.basic import get_colors, draw_text, list_colormaps, draw_text_only
from svg.basic import text_style, add_style, get_styles, draw_any
from svg.file import SVGFileV2
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
# from svgPointLine import calculate_pi


def Convert(s):
    """ get char list of a string"""
    # list1 = []
    # list1[:0] = s
    # return list1
    return [i for i in s]


def get_text_colors(text):
    """ get color maps """
    s = list(set(Convert(text)))
    s.sort()

    list_colormaps()
    colors = get_colors(len(s), color_map='rainbow')
    colors_dict = {}
    for i, c in enumerate(s):
        colors_dict[c] = colors[i]
    return colors_dict


def draw_char(svg, char, x0, y0, color):
    """ draw text lines """
    # svg.draw(draw_text(x=x0, y=y0, text=char, color=color))
    # svg.draw(draw_text_only(x=x0, y=y0, text=char))
    svg.draw(draw_any("text", text=char, x=x0, y=y0, fill=color))


def chunk_string(string, length):
    """ chunk string into smaller ones """
    return [string[0 + i:length + i] for i in range(0, len(string), length)]


def draw_color_chars(svg, x0=10, y0=12, x_inter=6, y_inter=16, line_w=30):
    H, W = svg.get_size()
    svg.set_title('Draw color text')

    style_dict = text_style(font_size='12px')
    style_dict.pop('fill', None)
    svg.draw(add_style('text', get_styles(style_dict)))

    text = str(calculate_pi()).lower()
    # print('text=', text)
    colors = get_text_colors(text)
    colors['.'] = 'black'

    x = x0
    y = y0
    for line in chunk_string(text, line_w):
        for c in line:
            draw_char(svg, c, x, y, colors[c])
            x += x_inter
        x = x0
        y += y_inter


def calculate_pi(N=1545):
    def make_pi(N=N):
        q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
        for j in range(N):
            if 4 * q + r - t < m * t:
                yield m
                q, r, t, k, m, x = 10 * q, 10 * (r - m * t), t, k, (10 * (3 * q + r)) // t - 10 * m, x
            else:
                q, r, t, k, m, x = q * k, (2 * q + r) * x, t * x, k + 1, (q * (7 * k + 2) + r * x) // (t * x), x + 2

    my_array = [str(i) for i in make_pi()]
    my_array = my_array[:1] + ['.'] + my_array[1:]
    return "".join(my_array)


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'colors.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    draw_color_chars(svg)


if __name__ == "__main__":
    main()
