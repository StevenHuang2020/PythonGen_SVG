# python3 Steven 11/06/20 Auckland,NZ

import numpy as np
import pandas as pd
from enum import Enum
from svg.basic import add_style, get_styles, draw_any, color_fader, clip_float
from svg.file import SVGFileV2
from common import gImageOutputPath
from svgSmile import drawSmileSVGNode


class TableContentStyle(Enum):
    TEXT = 1  # plain text
    COLOR = 2  # color
    SMILE = 3  # smile


def getDataSet():
    # return pd.DataFrame(np.arange(12).reshape(-1, 3),columns=['A', 'B', 'C'])
    return pd.DataFrame(np.random.randint(
        1, 150, size=(5, 3)), columns=['A', 'B', 'C'])

    # data = {'Name':['Tom', 'Jane', 'Steve', 'Ricky'],
    #         'Gender':['Male','Female','Male','Male'], 'Age':[28,34,29,42]}
    # return pd.DataFrame(data)


def plotTable(svg, node, df, style=TableContentStyle.TEXT):
    W, H = svg.get_size()
    print('df.shape=', df.shape)
    indexs = df.index
    columns = df.columns
    print('indexs=', indexs)
    print('columns=', columns)
    print(df)
    row, col = df.shape

    offsetX = 5
    offsetY = 5
    colWidth = (W - 2 * offsetX) / (col + 1)  # 45
    rowHeight = (H - 2 * offsetY) / (row + 1)  # 25

    styleDict = {}
    styleDict['stroke'] = 'black'
    styleDict['stroke-width'] = '0.5'
    svg.draw_node(node, add_style('line', get_styles(styleDict)))

    anyDict = {}
    # anyDict['stroke'] = 'black'
    # anyDict['stroke-width'] = 0.5
    for i in range(row + 2):
        x1 = offsetX
        y1 = offsetY + i * rowHeight
        x2 = x1 + (col + 1) * colWidth
        y2 = y1

        anyDict['x1'] = x1
        anyDict['y1'] = y1
        anyDict['x2'] = x2
        anyDict['y2'] = y2
        svg.draw_node(node, draw_any('line', **anyDict))

    for i in range(col + 2):
        x1 = offsetX + i * colWidth
        y1 = offsetY
        x2 = x1
        y2 = y1 + (row + 1) * rowHeight

        anyDict['x1'] = x1
        anyDict['y1'] = y1
        anyDict['x2'] = x2
        anyDict['y2'] = y2
        svg.draw_node(node, draw_any('line', **anyDict))

    styleDict = {}
    # styleDict['fill'] = 'black'
    styleDict['font-family'] = 'Consolas'
    # styleDict['font-size'] = '22px'
    styleDict['dominant-baseline'] = "middle"
    styleDict['text-anchor'] = "middle"

    svg.draw_node(node, add_style('text', get_styles(styleDict)))

    anyDict = {}
    anyDict['font-size'] = '14px'
    anyDict['fill'] = 'red'
    """draw index text"""
    for i, index in enumerate(indexs):
        # print(index)
        x1 = offsetX
        y1 = offsetY + (i + 1) * rowHeight
        x = x1 + colWidth / 2
        y = y1 + rowHeight / 2

        anyDict['x'] = x
        anyDict['y'] = y
        svg.draw_node(node, draw_any('text', index, **anyDict))

    """draw column text"""
    for i, column in enumerate(columns):
        # print(column)
        x1 = offsetX + (i + 1) * colWidth
        y1 = offsetY
        x = x1 + colWidth / 2
        y = y1 + rowHeight / 2

        anyDict['x'] = x
        anyDict['y'] = y
        svg.draw_node(node, draw_any('text', column, **anyDict))

    """draw content text"""
    for i in range(row):
        for j in range(col):
            x = offsetX + (j + 1) * colWidth
            y = offsetY + (i + 1) * rowHeight

            g = svg.draw_node(node, draw_any('g', opacity=1.0, id=str(i) + '_' + str(j)))

            if style == TableContentStyle.TEXT:
                anyDict['x'] = x + colWidth / 2
                anyDict['y'] = y + rowHeight / 2
                anyDict['font-size'] = '12px'
                anyDict['fill'] = 'black'
                svg.draw_node(g, draw_any('text', df.iloc[i, j], **anyDict))
            elif style == TableContentStyle.COLOR:
                anyDict['x'] = x
                anyDict['y'] = y
                anyDict['width'] = colWidth
                anyDict['height'] = rowHeight

                maxV = np.max(df.values)
                minV = np.min(df.values)
                scalar = (df.iloc[i, j] - minV) / (maxV - minV)
                anyDict['fill'] = color_fader('#C0392B', '#3498DB', scalar)  # 'b'
                svg.draw_node(g, draw_any('rect', df.iloc[i, j], **anyDict))
            elif style == TableContentStyle.SMILE:
                r = rowHeight // 2 - 1
                x = x + colWidth / 2 - r
                y = y + rowHeight / 2 - r

                r = clip_float(r)
                x = clip_float(x)
                y = clip_float(y)
                drawSmileSVGNode(svg, g, radius=r, offsetX=x, offsetY=y)
                # svg.draw_node(node, draw_any('rect', df.iloc[i,j], **anyDict))
                # svg.draw_node(node, draw_any('circle', cx=x,cy=y,r=2,fill='red'))
            else:
                print('Not implement yet.')


def drawDataFrame(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    svg.set_title('draw Dataframe data')

    g = svg.draw(draw_any('g', opacity=1.0))
    # anyNode = svg.draw_node(g, draw_any('test','222', a=10, b="4",c='red',xml='www.ss'))
    # svg.draw_node(g, draw_any('test','hello'))
    df = getDataSet()
    plotTable(svg, g, df, TableContentStyle.TEXT)


def main():
    file = gImageOutputPath + r'\dataFrame.svg'
    svg = SVGFileV2(file, W=200, H=120, border=True)
    drawDataFrame(svg)


if __name__ == '__main__':
    main()
