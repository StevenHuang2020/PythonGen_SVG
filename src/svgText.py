# -*- encoding: utf-8 -*-
# Date: 07/May/2023 updated
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: SVG text node exampls
"""""""""""""""""""""""""""""""""""""""""""""""""""""
from svg.basic import get_styles, add_style, draw_text, draw_text_only, random_color,text_style
from svg.file import SVGFileV2
from common import IMAGE_OUTPUT_PATH
from common_path import traverse_files, join_path

# chinese font style font-family names:
# 新細明體: PMingLiU
# 細明體: MingLiU
# 標楷體: DFKai-SB
# 黑体: SimHei
# 宋体: SimSun
# 新宋体: NSimSun
# 仿宋: FangSong
# 楷体: KaiTi
# 仿宋_GB2312: FangSong_GB2312
# 楷体_GB2312: KaiTi_GB2312
# 微軟正黑體: Microsoft JhengHei
# 微软雅黑体: Microsoft YaHei
# 隶书: LiSu
# 幼圆: YouYuan
# 华文细黑: STXihei
# 华文楷体: STKaiti
# 华文宋体: STSong
# 华文中宋: STZhongsong
# 华文仿宋: STFangsong
# 方正舒体: FZShuTi
# 方正姚体: FZYaoti
# 华文彩云: STCaiyun
# 华文琥珀: STHupo
# 华文隶书: STLiti
# 华文行楷: STXingkai
# 华文新魏: STXinwei


def svg_draw_text(svg):
    """ draw text svg """
    style_dict = text_style()
    svg.draw(add_style('text', get_styles(style_dict)))

    y0 = 15
    for i in range(10):
        svg.draw(draw_text(0, y0, f'.  Hello   World!     {i}'))
        # svg.draw(draw_text_only(0, y0, '.  Hello   World!     {}'.format(i)))
        y0 += 12


def draw_text_file():
    """ draw text svg from a file content """
    def GeFile(file = r'.\res\hi.txt'):
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()

    file = join_path(IMAGE_OUTPUT_PATH, r'Hi.svg')
    H, W = 200, 1200

    svg = SVGFileV2(file, W, H, border=False)

    style_dict = text_style(font_size='10px')
    svg.draw(add_style('text', get_styles(style_dict)))

    x0 = 0
    y0 = 15
    h = 12
    for i in GeFile():
        # i = i.replace('#', '@') # use another character instead
        i = ' '.join(i)
        # print(i)
        svg.draw(draw_text_only(x0, y0, i))
        y0 += h


def draw_str_list(svg, str_list, x0, y0, x_inter, y_inter, from_right=True):
    """ draw text lines """
    x = x0
    y = y0

    if from_right:
        x_inter *= -1

    for i in str_list:
        for c in i:
            svg.draw(draw_text_only(x, y, text=c))
            y = y + y_inter
        y = y0
        x = x + x_inter


def draw_poet(svg):
    """ draw a poet """
    # poet = []
    # poet.append('感遇·其一')
    # poet.append('张九龄')
    # poet.append('兰叶春葳蕤，桂华秋皎洁。')
    # poet.append('欣欣此生意，自尔为佳节。')
    # poet.append('谁知林栖者，闻风坐相悦。')
    # poet.append('草木有本心，何求美人折？')

    poet = []
    poet.append('過故人莊 孟浩然')
    poet.append('故人具雞黍，邀我至田家。')
    poet.append('綠樹村邊合，青山郭外斜。')
    poet.append('開軒面場圃，把酒話桑麻。')
    poet.append('待到重陽日，还來就菊花。')

    style_dict = text_style(font='KaiTi', font_size='16px')
    svg.draw(add_style('text', get_styles(style_dict)))

    _, W = svg.get_size()
    offsetX = 25
    offsetY = 20
    x0 = W - 2 * offsetX
    y0 = offsetY
    y_inter = 15
    x_inter = 32

    draw_str_list(svg, poet, x0, y0, x_inter, y_inter)


def draw_poet2(svg):
    """ draw a poet """
    poet = []
    poet.append('紅樓夢')
    poet.append('可嘆停機德，')
    poet.append('堪憐詠絮才。')
    poet.append('玉帶林中掛，')
    poet.append('金簪雪裡埋。')

    style_dict = text_style(color='red', font='LiSu', font_size='22px')
    # H, W = svg.get_size()
    svg.draw(add_style('text', get_styles(style_dict)))

    offsetX = 28
    offsetY = 42
    x0 = offsetX
    y0 = offsetY
    y_inter = 26
    x_inter = 30

    draw_str_list(svg, poet, x0, y0, x_inter, y_inter, False)


def draw_style_text(svg, text = '怡红快绿', x_inter = 60, y_inter = 60):
    """ rotation examples """
    style_dict = text_style(color='red', font='Microsoft YaHei', font_size='50px')
    svg.draw(add_style('text', get_styles(style_dict)))

    H, W = svg.get_size()
    x0 = (W - x_inter) / 2
    y0 = (H - y_inter) / 2
    w, _ = 2, 2
    for i, c in enumerate(text):
        x = x0 + i % w * x_inter
        y = y0 + i // w * y_inter
        node = svg.draw(draw_text_only(x, y, text=c))
        svg.set_node(node, 'text-anchor', 'middle')
        svg.set_node(node, 'dominant-baseline', 'central')
        svg.set_node(node, 'fill', random_color())
        svg.set_node(node, 'transform', f'rotate({(i-1)*90},{x},{y})')
        # svg.draw(draw_circle(x, y, 5, color='red'))


def draw_style_text2(svg, only_rotate=False):
    """ rotation examples """
    text = 'Text rotation!'

    style_dict = text_style(font='Consolas', font_size='24px')
    svg.draw(add_style('text', get_styles(style_dict)))

    x0 = 70
    y0 = 30
    theta = 0
    for _ in range(6):
        node = svg.draw(draw_text_only(x0, y0, text))
        if only_rotate:
            svg.set_node(node, 'rotate', theta)
        else:
            str_tmp = f'rotate({theta},{x0},{y0})'
            svg.set_node(node, 'transform', str_tmp)
            svg.set_node(node, 'text-anchor', 'middle')
            svg.set_node(node, 'dominant-baseline', 'central')

        y0 += 25
        theta += 30


def getSystemFonts(folder = r'C:\Windows\fonts'):
    """ print system fonts """
    for i in traverse_files(folder, 'ttf TTF ttc', True):
        print(i)


def main():
    """ main function """
    # draw_text_file()
    # getSystemFonts()

    file = join_path(IMAGE_OUTPUT_PATH, r'text.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # svg_draw_text(svg)
    # draw_poet(svg)
    # draw_poet2(svg)
    # draw_style_text(svg)
    draw_style_text2(svg)


if __name__ == '__main__':
    main()
