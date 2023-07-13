# -*- encoding: utf-8 -*-
# Date: 11/06/20
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: SVG show pandas data
"""""""""""""""""""""""""""""""""""""""""""""""""""""

from enum import Enum
import numpy as np
import pandas as pd
from svg.basic import add_style, get_styles, draw_any, color_fader, clip_float
from svg.file import SVGFileV2
from common import IMAGE_OUTPUT_PATH
from svgSmile import drawSmileSVGNode
from common_path import join_path


class TableContentStyle(Enum):
    """ style list """
    TEXT = 1  # plain text
    COLOR = 2  # color
    SMILE = 3  # smile


def getDataSet():
    """ generate a dataset """
    # return pd.DataFrame(np.arange(12).reshape(-1, 3),columns=['A', 'B', 'C'])
    return pd.DataFrame(np.random.randint(
        1, 150, size=(5, 3)), columns=['A', 'B', 'C'])

    # data = {'Name':['Tom', 'Jane', 'Steve', 'Ricky'],
    #         'Gender':['Male','Female','Male','Male'], 'Age':[28,34,29,42]}
    # return pd.DataFrame(data)


def plotTable(svg, node, df, style=TableContentStyle.TEXT, offsetX=5, offsetY=5):
    """ plot table """
    H, W = svg.get_size()
    # print('df.shape=', df.shape)
    # print(df)
    row, col = df.shape

    col_width = (W - 2 * offsetX) // (col + 1)  # 45
    row_height = (H - 2 * offsetY) // (row + 1)  # 25

    ################# Draw table lines ###############
    any_dict = {}
    any_dict['stroke'] = 'black'
    any_dict['stroke-width'] = '0.5'
    svg.draw_node(node, add_style('line', get_styles(any_dict)))

    for i in range(row + 2):
        any_dict.clear()
        any_dict['x1'] = offsetX
        any_dict['y1'] = offsetY + i * row_height
        any_dict['x2'] = any_dict['x1'] + (col + 1) * col_width
        any_dict['y2'] = any_dict['y1']
        svg.draw_node(node, draw_any('line', **any_dict))

    for i in range(col + 2):
        any_dict.clear()
        any_dict['x1'] = offsetX + i * col_width
        any_dict['y1'] = offsetY
        any_dict['x2'] = any_dict['x1']
        any_dict['y2'] = any_dict['y1'] + (row + 1) * row_height
        svg.draw_node(node, draw_any('line', **any_dict))

    ################# Draw table cells ###############
    def draw_label(svg, node, df, offsetX,offsetY, col_width, row_height):
        any_dict = {}
        any_dict['font-family'] = 'Consolas'
        # any_dict['font-size'] = '22px'
        any_dict['dominant-baseline'] = "middle"
        any_dict['text-anchor'] = "middle"
        svg.draw_node(node, add_style('text', get_styles(any_dict)))

        any_dict.clear()
        any_dict['font-size'] = '14px'
        any_dict['fill'] = 'red'
        # draw index text
        for i, index in enumerate(df.index):
            # print(index)
            any_dict['x'] = offsetX + col_width / 2
            any_dict['y'] = offsetY + (i + 1) * row_height + row_height / 2
            svg.draw_node(node, draw_any('text', index, **any_dict))

        # draw column text
        for i, column in enumerate(df.columns):
            any_dict['x'] = offsetX + (i + 1) * col_width + col_width / 2
            any_dict['y'] = offsetY + row_height / 2
            svg.draw_node(node, draw_any('text', column, **any_dict))

    draw_label(svg, node, df, offsetX,offsetY, col_width, row_height)

    # draw content cell text
    def draw_cells(svg, node, style, row, col, col_width, row_height, df):
        for i in range(row):
            for j in range(col):
                x = offsetX + (j + 1) * col_width
                y = offsetY + (i + 1) * row_height

                g = svg.draw_node(node, draw_any(
                    'g', opacity=1.0, id=str(i) + '_' + str(j)))

                if style == TableContentStyle.TEXT:
                    any_dict['x'] = x + col_width / 2
                    any_dict['y'] = y + row_height / 2
                    any_dict['font-size'] = '12px'
                    any_dict['fill'] = 'black'
                    svg.draw_node(g, draw_any('text', df.iloc[i, j], **any_dict))
                elif style == TableContentStyle.COLOR:
                    any_dict['x'] = x
                    any_dict['y'] = y
                    any_dict['width'] = col_width
                    any_dict['height'] = row_height

                    max_v = np.max(df.values)
                    min_v = np.min(df.values)
                    scalar = (df.iloc[i, j] - min_v) / (max_v - min_v)
                    any_dict['fill'] = color_fader(
                        '#C0392B', '#3498DB', scalar)  # 'b'
                    svg.draw_node(g, draw_any('rect', df.iloc[i, j], **any_dict))
                elif style == TableContentStyle.SMILE:
                    r = row_height // 2 - 1
                    x = x + col_width / 2 - r
                    y = y + row_height / 2 - r

                    r = clip_float(r)
                    x = clip_float(x)
                    y = clip_float(y)
                    drawSmileSVGNode(svg, g, radius=r, offsetX=x, offsetY=y)
                    # svg.draw_node(node, draw_any('rect', df.iloc[i,j], **any_dict))
                    # svg.draw_node(node, draw_any('circle', cx=x,cy=y,r=2,fill='red'))
                else:
                    print('Warnning, not implement yet.')

    draw_cells(svg, node, style, row, col, col_width, row_height, df)


def drawDataFrame(svg, style=TableContentStyle.TEXT):
    """ draw pandas data """
    svg.set_title('Draw Dataframe data')

    g = svg.draw(draw_any('g', opacity=1.0))
    df = getDataSet()
    plotTable(svg, g, df, style)


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'dataFrame.svg')
    svg = SVGFileV2(file, W=200, H=120, border=True)
    # drawDataFrame(svg, TableContentStyle.TEXT)
    # drawDataFrame(svg, TableContentStyle.COLOR)
    drawDataFrame(svg, TableContentStyle.SMILE)


if __name__ == '__main__':
    main()
