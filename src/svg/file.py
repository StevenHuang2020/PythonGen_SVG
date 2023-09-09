# -*- encoding: utf-8 -*-
# Date: 09/07/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: SVGFileV2, SVGFile class
"""

import os
from lxml import etree
from svg.basic import draw_tag, style_content, get_styles, add_style

__all__ = ['SVGFileV2', 'SVGFile']


class SVGFileV2:
    """ lxml version svg """

    _url = 'http://www.w3.org/2000/svg'
    _xlink = 'http://www.w3.org/1999/xlink'
    _namespace = 'http://www.w3.org/XML/1998/namespace'
    _version = '1.1'
    _WINDOWS_LINE_ENDING = '\r\n'
    _UNIX_LINE_ENDING = '\n'

    def __init__(self, file, W=100, H=100, title=None, border=False,
                 border_color='black', border_width=1):
        self._file = file
        self._width = W
        self._height = H

        self._root = etree.Element("svg", nsmap={
                                   None: SVGFileV2._url, "xlink": SVGFileV2._xlink},
                                   version=SVGFileV2._version)

        self.set_node(self._root, 'width', f'{self._width}')
        self.set_node(self._root, 'height', f'{self._height}')
        view_box = f'0 0 {self._width} {self._height}'
        self.set_node(self._root, 'viewBox', view_box)

        if border:
            self.add_border(border_color, border_width)
        self.set_title(title)

    def get_xlink(self):
        """ get xlink """
        return self._xlink

    def get_size(self):
        """ get height, width """
        return self._height, self._width

    def add_svg_style(self, tag: str, style_dict: dict):
        """ add svg style """
        style_node = self.get_child(child_tag='style')
        if style_node is not None:
            new_style = style_content(tag, get_styles(style_dict))
            if new_style not in style_node.text:
                style_node.text += new_style
        else:
            self.draw(add_style(tag, get_styles(style_dict)))

    def add_root_style(self, new_style: str):
        """ add root svg node style """
        style = self._root.get('style')
        if style is not None:
            style = style + ';' + new_style
        else:
            style = new_style
        self._root.set('style', style)

    def add_border(self, border_color, border_width):
        """ add svg border """
        style = f'border:{border_width}px solid {border_color}'
        self.add_root_style(style)

    def set_background(self, color):
        """ set svg background """
        self.add_root_style(f'background-color:{color}')

    def add_style_node(self, style: str):
        style_node = self.get_child(child_tag='style')
        if style_node is None:
            style_node = self.draw(draw_tag('style'))

        if style_node.text is None:
            style_node.text = ''
        style_node.text += style

    def set_title(self, title=None):
        """ set svg title """
        if title is not None:
            self.draw(draw_tag('title', title))

    def get_root(self):
        """ get root node """
        return self._root

    def set_node(self, node, attri, value):
        """ set etree Element node attribute """
        if node is not None:
            node.set(attri, str(value))

    def get_node(self, node, attri):
        """ get etree Element node attribute """
        if node is not None:
            node.get(attri)

    def set_node_dict(self, node, attri_dict):
        """ set node attributes """
        for key, value in attri_dict.items():
            self.set_node(node, key, value)

    def _add_child(self, parent, child):
        """ add child node """
        if parent is None:
            parent = self._root
        parent.append(child)

    def _new_node(self, content: str = ''):
        """ create a node """
        return etree.fromstring(content)

    def draw(self, content: str = ''):
        """ link child to svgRoot """
        return self.draw_node(self._root, content)

    def draw_node(self, node_parent=None, content: str = ''):
        """ link child to parent node """
        child_node = self._new_node(content)
        self._add_child(node_parent, child_node)
        return child_node

    def get_child(self, node=None, child_tag=None):
        """ get first child node by tag """
        if node is None:
            node = self._root
        for i in node:
            if i.tag == child_tag:
                # print(etree.tostring(i))
                # print(i.text)
                return i
        return None

    def close(self, win_eof=True):
        """ write lxml tree to file """
        tree = etree.ElementTree(self._root)
        if not win_eof:
            tree.write(self._file, pretty_print=True,
                       xml_declaration=True, encoding=r'UTF-8', standalone=False)
        else:
            content = etree.tostring(tree, pretty_print=True,
                                     xml_declaration=True, encoding=r'UTF-8', standalone=False)
            with open(self._file, 'w', encoding=r'UTF-8', newline=SVGFileV2._WINDOWS_LINE_ENDING) as xml_fh:
                xml_fh.write(content.decode(r'UTF-8'))

    def save(self):
        """ save svg """
        self.close()

    def __del__(self):
        self.close()


class SVGFile:
    """ string IO version, deprecated """

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
        """ append node to svg """
        content = '        ' + content + '\n'
        self._append_svg(content)

    def close(self):
        """ close svg """
        self._svg_tail()
        self._write_svg()

    def __del__(self):
        self.close()
