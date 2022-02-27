# -*- encoding: utf-8 -*-
# Date: 09/07/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: SVGFileV2, SVGFile class
"""

import os
from lxml import etree
from svg.basic import draw_rect, draw_tag

__all__ = ['SVGFileV2', 'SVGFile']


class SVGFileV2:
    """lxml version svg"""

    def __init__(self, file, W=100, H=100, title=None, border=False,
                 border_color='black', border_width=1):
        self._file = file
        self._width = W
        self._height = H
        self._url = "http://www.w3.org/2000/svg"
        self._xlink = "http://www.w3.org/1999/xlink"
        # self.namespace = "http://www.w3.org/XML/1998/namespace"
        self._version = "1.1"
        self._root = etree.Element("svg", nsmap={None: self._url, "xlink": self._xlink},
                                   version=self._version)

        self.set_node(self._root, 'width', f'{self._width}')
        self.set_node(self._root, 'height', f'{self._height}')
        view_box = '0 0 {} {}'.format(self._width, self._height)
        self.set_node(self._root, 'viewBox', view_box)

        self._bk_rect = None  # background rect
        if border:
            self.add_border(border_color, border_width)
        self.set_title(title)

    def get_size(self):
        return self._width, self._height

    def add_root_style(self, new_style):
        style = self._root.get('style')
        if style is not None:
            style = style + ';' + new_style
        else:
            style = new_style
        self._root.set('style', style)

    def add_border(self, border_color, border_width):
        def setborder_1():
            """ Method 1: add to svg root node """
            style = f'border:{int(border_width)}px solid {border_color}'
            self.add_root_style(style)

        def setborder_2():
            """ Method 2: add a background rect """
            self._bk_rect = self.draw(draw_rect(0, 0, self._width, self._height, stroke_width=1,
                                      color='None', stroke_color='black'))
            self._bk_rect.set("id", "border")
            self._bk_rect.set("opacity", "0.8")

        setborder_1()
        # setborder_2()

    def set_background(self, color):
        def bg_method1(color):
            # Method 1: set _root mode 'style'
            style = f'background-color:{color}'
            self.add_root_style(style)

        def bg_method2(color):
            # Method 2: set 'fill' attr of _bk_rect node
            if self._bk_rect is not None:
                self._bk_rect.set("fill", f"{color}")

        bg_method1(color)

    def set_title(self, title=None):
        if title is not None:
            self.draw(draw_tag('title', title))

    def get_root(self):
        return self._root

    def set_node(self, node, attri, value):
        """set etree Element node attribute"""
        if node is not None:
            node.set(attri, str(value))

    def get_node(self, node, attri):
        """get etree Element node attribute"""
        if node is not None:
            node.get(attri)

    def set_node_dict(self, node, attri_dict):
        for key, value in attri_dict.items():
            self.set_node(node, key, value)

    def add_child(self, node_parent, child):
        if node_parent is None:
            self._root.append(child)
        else:
            node_parent.append(child)

    def draw(self, content: str):
        """link child to svgRoot element"""
        return self.draw_node(self._root, content)

    def new_node(self, content=''):
        # print('content=',content)
        return etree.fromstring(content)

    def draw_node(self, node=None, content=''):
        """link child to node element"""
        child_node = self.new_node(content)
        self.add_child(node, child_node)
        return child_node

    def close(self):
        """write lxml tree to file"""
        tree = etree.ElementTree(self._root)
        tree.write(self._file, pretty_print=True,
                   xml_declaration=True, encoding='UTF-8', standalone=False)

    def save(self):
        self.close()

    def __del__(self):
        self.close()


class SVGFile:
    """string IO version, deprecated"""

    def __init__(self, file_name, width=100, height=100):
        self._init_file(file_name)
        self._file_name = file_name
        self.width = width
        self.height = height
        self._svg_content = ''
        self._svg_header()

    def _init_file(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    def _append_svg(self, content):
        self._svg_content += content

    def _write_svg(self):
        with open(self._file_name, 'a', newline='\n', encoding="utf-8") as f:
            f.write(self._svg_content)

    def _svg_header(self):
        header = ''
        s = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        header += s
        s = f'<svg width="{self.width}" height="{self.height}" version="1.1" \
            xmlns="http://www.w3.org/2000/svg">\n'
        header += s
        s = '    <g opacity="1.0">\n'
        header += s
        self._append_svg(header)

    def _svg_tail(self):
        tail = '    </g> \n</svg>'
        self._append_svg(tail)

    def draw(self, content):
        content = '        ' + content + '\n'
        self._append_svg(content)

    def close(self):
        self._svg_tail()
        self._write_svg()

    def __del__(self):
        self.close()
