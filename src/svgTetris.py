# -*- encoding: utf-8 -*-
# Date: 14/Jul/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Tetris
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svg.basic import draw_tag, draw_any, random_color, rand_str
from svg.file import SVGFileV2


def block_tetris(svg, ref_id):
    """ defintion of one basic block """
    defs = svg.draw(draw_tag('defs'))
    g = svg.draw_node(defs, draw_any('g', id=ref_id))
    # svg.set_node(g, 'opacity', '1.0')
    svg.draw_node(g, draw_any('rect', height='24', width='24'))

    dict_any = {}
    dict_any['fill'] = '#fff'
    dict_any['fill-opacity'] = '.7'
    dict_any['d'] = "m0,0 3,3 18,0 3,-3"
    svg.set_node_dict(svg.draw_node(g, draw_any('path')), dict_any)

    dict_any['fill'] = '#000'
    dict_any['fill-opacity'] = '.1'
    dict_any['d'] = "m0,0 3,3 0,18 -3,3 m24,-24 -3,3 0,18 3,3"
    svg.set_node_dict(svg.draw_node(g, draw_any('path')), dict_any)

    dict_any['fill'] = '#000'
    dict_any['fill-opacity'] = '.5'
    dict_any['d'] = "m0,24 3,-3 18,0 3,3"
    svg.set_node_dict(svg.draw_node(g, draw_any('path')), dict_any)


def draw_type(svg, self_id, ref_id, fill, coordinates):
    """ draw a Tetromino of Tetris """
    g = svg.draw(draw_any('g', id=self_id))

    dict_any = {}
    dict_any[f"{{{svg.get_xlink()}}}" + 'href'] = f'#{ref_id}'
    if fill is None:
        fill = random_color()
    dict_any['fill'] = fill

    for i in coordinates:
        dict_any['x'] = str(i[0])
        dict_any['y'] = str(i[1])
        svg.set_node_dict(svg.draw_node(g, draw_any('use')), dict_any)
    return g


def draw_type1(svg, self_id, ref_id, fill='#00f0f0'):
    """ create type 1 """
    coordinates = np.array([[0, 0], [0, 24], [0, 48], [0, 72]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type2(svg, self_id, ref_id, fill='#0000f0'):
    """ create type 2 """
    coordinates = np.array([[72, 0], [72, 24], [72, 48], [48, 48]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type3(svg, self_id, ref_id, fill='#f0a000'):
    """ create type 3 """
    coordinates = np.array([[144, 0], [144, 24], [144, 48], [168, 48]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type4(svg, self_id, ref_id, fill='#f0f000'):
    """ create type 4 """
    coordinates = np.array([[216, 0], [240, 0], [216, 24], [240, 24]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type5(svg, self_id, ref_id, fill='#00f000'):
    """ create type 5 """
    coordinates = np.array([[24, 120], [48, 120], [0, 144], [24, 144]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type6(svg, self_id, ref_id, fill='#a000f0'):
    """ create type 6 """
    coordinates = np.array([[96, 120], [120, 120], [144, 120], [120, 144]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type7(svg, self_id, ref_id, fill='#f00000'):
    """ create type 7 """
    coordinates = np.array([[192, 120], [216, 120], [216, 144], [240, 144]])
    return draw_type(svg, self_id, ref_id, fill, coordinates)


def draw_type_any(svg, ref_id, fill=None):
    """ create type """
    x = 0
    y = 192
    sz = 24  # block size
    coords = [[x, y]]
    for i in range(2):
        x += sz
        y += sz
        coords.append([x, y])

    # print('coords=', coords)
    draw_type(svg, self_id=rand_str(), ref_id=ref_id, fill=fill, coordinates=coords)

    x += 2 * sz
    y = 192

    coords = [[x + sz, y]]
    coords.append([x, y + sz])
    coords.append([x + sz, y + sz])
    coords.append([x + sz + sz, y + sz])
    coords.append([x + sz, y + sz + sz])
    draw_type(svg, self_id=rand_str(), ref_id=ref_id, fill=fill, coordinates=coords)

    x += 4 * sz
    y = 192
    coords = [[x, y]]
    coords.append([x, y + sz])
    coords.append([x + sz, y + sz])
    coords.append([x + sz + sz, y + sz])
    coords.append([x + sz + sz, y + sz + sz])
    draw_type(svg, self_id=rand_str(), ref_id=ref_id, fill=fill, coordinates=coords)


def tetris(svg):
    H, W = svg.get_size()
    svg.set_title('Tetris')

    blcok_id = 'x'
    block_tetris(svg, blcok_id)
    draw_type1(svg, ref_id=blcok_id, self_id='i', fill=None)
    draw_type2(svg, ref_id=blcok_id, self_id='j', fill=None)
    draw_type3(svg, ref_id=blcok_id, self_id='l', fill=None)
    draw_type4(svg, ref_id=blcok_id, self_id='o', fill=None)
    draw_type5(svg, ref_id=blcok_id, self_id='s', fill=None)
    draw_type6(svg, ref_id=blcok_id, self_id='t', fill=None)
    draw_type7(svg, ref_id=blcok_id, self_id='z', fill=None)
    draw_type_any(svg, ref_id=blcok_id)


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'tetris.svg')
    svg = SVGFileV2(file, W=350, H=400, border=True)
    tetris(svg)


if __name__ == "__main__":
    main()
