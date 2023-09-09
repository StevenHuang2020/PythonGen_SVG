# -*- encoding: utf-8 -*-
# Date: 14/Jul/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Tetris
"""""""""""""""""""""""""""""""""""""""""""""""""""""
from enum import Enum
import numpy as np
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svg.basic import draw_tag, draw_any, random_color, rand_str
from svg.file import SVGFileV2


class Tetris_Type(Enum):
    """ Tetris shape type """
    Type_I = 1
    Type_J = 2
    Type_L = 3
    Type_O = 4
    Type_S = 5
    Type_T = 6
    Type_Z = 7


class Tetris:
    """ Tetris class """

    def __init__(self, svg, block_w=24, block_h=24) -> None:
        self.svg = svg
        self.block_w = block_w
        self.block_h = block_h
        self.block_id = rand_str()   # block id
        self._create_block()

    def _get_defs(self):
        defs = self.svg.get_child(child_tag='defs')
        defs = defs if defs else self.svg.draw(draw_tag('defs'))
        return defs

    def _create_block(self):
        """ create basic tetris block """
        self.defs_node = self._get_defs()
        self._block_tetris(self.svg, self.defs_node, self.get_block_id())

    def _block_tetris(self, svg, defs_node, ref_id):
        g = svg.draw_node(defs_node, draw_any('g', id=ref_id))
        # svg.set_node(g, 'opacity', '1.0')
        svg.draw_node(g, draw_any('rect', height=self.block_h, width=self.block_w))

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

    def _create_type_i(self, self_id, fill=None):
        coordinates = np.array([[0, 0], [0, 24], [0, 48], [0, 72]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_j(self, self_id, fill=None):
        coordinates = np.array([[24, 0], [24, 24], [24, 48], [0, 48]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_l(self, self_id, fill=None):
        coordinates = np.array([[0, 0], [0, 24], [0, 48], [24, 48]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_o(self, self_id, fill=None):
        coordinates = np.array([[0, 0], [24, 0], [0, 24], [24, 24]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_s(self, self_id, fill=None):
        coordinates = np.array([[24, 0], [48, 0], [0, 24], [24, 24]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_t(self, self_id, fill=None):
        coordinates = np.array([[0, 0], [24, 0], [48, 0], [24, 24]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_type_z(self, self_id, fill=None):
        coordinates = np.array([[0, 0], [24, 0], [24, 24], [48, 24]])
        self._create_shape(self.defs_node, self_id, self.get_block_id(), fill=fill,
                           coordinates=coordinates)

    def _create_shape(self, defs_node, self_id, ref_id, coordinates, fill=None):
        """ draw a Tetromino of Tetris """
        g = self.svg.draw_node(defs_node, draw_any('g', id=self_id))

        dict_any = {}
        dict_any[f"{{{self.svg.get_xlink()}}}" + 'href'] = f'#{ref_id}'
        dict_any['fill'] = fill if fill is not None else random_color()

        for i in coordinates:
            dict_any['x'] = str(i[0])
            dict_any['y'] = str(i[1])
            self.svg.set_node_dict(self.svg.draw_node(g, draw_any('use')), dict_any)
        return g

    def get_block_id(self):
        return self.block_id

    def draw_tetromino(self, tetris_type: Tetris_Type, x, y, fill=None):
        ref_id = rand_str()
        if tetris_type == Tetris_Type.Type_I:
            self._create_type_i(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_J:
            self._create_type_j(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_L:
            self._create_type_l(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_O:
            self._create_type_o(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_S:
            self._create_type_s(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_T:
            self._create_type_t(ref_id, fill)
        elif tetris_type == Tetris_Type.Type_Z:
            self._create_type_z(ref_id, fill)

        g = self.svg.draw(draw_any('g'))
        dict_any = {}
        dict_any[f"{{{self.svg.get_xlink()}}}" + 'href'] = f'#{ref_id}'
        dict_any['x'] = str(x)
        dict_any['y'] = str(y)
        self.svg.set_node_dict(self.svg.draw_node(g, draw_any('use')), dict_any)
        return g


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
    return defs


def draw_type(svg, self_id, ref_id, fill, coordinates):
    """ draw a Tetromino of Tetris """
    g = svg.draw(draw_any('g', id=self_id))

    dict_any = {}
    dict_any[f"{{{svg.get_xlink()}}}" + 'href'] = f'#{ref_id}'
    dict_any['fill'] = fill if fill is not None else random_color()

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


def draw_tetris(svg):
    """ draw tetris """
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


def draw_tetris_class(svg):
    """ draw tetris by using class """
    tetris = Tetris(svg)
    x, y = 0, 0
    tetris.draw_tetromino(Tetris_Type.Type_I, x, y)
    x += 2 * 24
    tetris.draw_tetromino(Tetris_Type.Type_J, x, y)
    x += 3 * 24
    tetris.draw_tetromino(Tetris_Type.Type_L, x, y)
    x += 3 * 24
    tetris.draw_tetromino(Tetris_Type.Type_O, x, y)
    x += 3 * 24
    tetris.draw_tetromino(Tetris_Type.Type_S, x, y)
    y += 5 * 24
    x = 0
    tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    x += 4 * 24
    tetris.draw_tetromino(Tetris_Type.Type_Z, x, y)
    x += 4 * 24
    tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    x += 4 * 24
    tetris.draw_tetromino(Tetris_Type.Type_S, x, y)

    x = 0
    y += 5 * 24
    g = tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    x += 4 * 24
    g = tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    svg.set_node(g, 'transform', f'rotate({1*90},{x},{y}) translate(-24 -48)')

    x += 4 * 24
    g = tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    svg.set_node(g, 'transform', f'rotate({2*90},{x},{y}) translate(-48 -24)')
    x += 4 * 24
    g = tetris.draw_tetromino(Tetris_Type.Type_T, x, y)
    svg.set_node(g, 'transform', f'rotate({3*90},{x},{y}) translate(-48 -24)')


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'tetris.svg')
    svg = SVGFileV2(file, W=380, H=400, border=True)
    # draw_tetris(svg)
    draw_tetris_class(svg)


if __name__ == "__main__":
    main()
