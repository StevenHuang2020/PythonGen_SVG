

from svg.basic import get_styles, add_style, draw_text, draw_text_only, random_color
from svg.file import SVGFileV2
from common import gImageOutputPath
from common_path import traverse_files


def drawText():
    def GeFile():
        file = r'.\res\hi.txt'
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()

    file = gImageOutputPath + r'\Hi.svg'
    H, W = 200, 1200
    # str='Hello'

    svg = SVGFileV2(file, W, H, border=False)

    styleDict = {}
    styleDict['fill'] = 'black'
    styleDict['font-family'] = 'Consolas'
    styleDict['font-size'] = '10px'
    styleDict['font-style'] = 'normal'
    styleDict['font-variant'] = 'normal'
    # styleDict['xml:space'] = 'preserve' #deprecated
    styleDict['white-space'] = 'pre'

    styleList = get_styles(styleDict)
    svg.draw(add_style('text', styleList))

    if 0:
        y0 = 15
        for i in range(10):
            svg.draw(draw_text(0, y0, '.    Hello     World!        1'))
            y0 += 12
    else:
        strs = GeFile()
        y0 = 15
        h = 12
        for i in strs:
            # i = i.replace('#', '@')
            i = ' '.join(i)  # '.'.join(i)
            print(i)
            # svg.draw(draw_text(0,y0,i, blank_space='preserve'))
            # text = svg.draw(draw_text_only(0,y0,i))

            # attr = "{{{}}}".format(svg.namespace) + 'space' #
            # svg.set_node(text, attr,"preserve") #error without namespace
            y0 += h

    svg.close()


'''
新細明體：PMingLiU
細明體：MingLiU
標楷體：DFKai-SB
黑体：SimHei
宋体：SimSun
新宋体：NSimSun
仿宋：FangSong
楷体：KaiTi
仿宋_GB2312：FangSong_GB2312
楷体_GB2312：KaiTi_GB2312
微軟正黑體：Microsoft JhengHei
微软雅黑体：Microsoft YaHei
隶书：LiSu
幼圆：YouYuan
华文细黑：STXihei
华文楷体：STKaiti
华文宋体：STSong
华文中宋：STZhongsong
华文仿宋：STFangsong
方正舒体：FZShuTi
方正姚体：FZYaoti
华文彩云：STCaiyun
华文琥珀：STHupo
华文隶书：STLiti
华文行楷：STXingkai
华文新魏：STXinwei
'''
'''
王维（701年—761年），字摩诘，号摩诘居士。唐代诗人，画家。
王维《山居秋暝》
空山新雨後，天氣晚來秋。
明月松間照，清泉石上流。
竹喧歸浣女，蓮動下漁舟。
隨意春芳歇，王孫自可留。

王维《九月九日憶山東兄弟》
獨在異鄉為異客，每逢佳節倍思親。
遙知兄弟登高處，遍插茱萸少一人。

王维《相思》
紅豆生南國，春來發幾枝？
願君多採擷，此物最相思。

王维《送元二使安西》
渭城朝雨浥輕塵，客舍青青柳色新。
勸君更盡一杯酒，西出陽關無故人。

王维《竹里館》
獨坐幽篁裡，彈琴復長嘯。
深林人不知，明月來相照。

陸游《村居書喜》
紅橋梅市曉山橫，白塔樊江春水生，
花氣襲人知驟暖，鵲聲穿樹喜新晴。
坊場酒賤貧猶醉，原野泥深老亦耕，
最喜先期官賦足，經年無吏扣柴門。

'''


def draw_poet(svg):
    '''
    poet = []
    poet.append('感遇·其一')
    poet.append('张九龄')
    poet.append('兰叶春葳蕤，桂华秋皎洁。')
    poet.append('欣欣此生意，自尔为佳节。')
    poet.append('谁知林栖者，闻风坐相悦。')
    poet.append('草木有本心，何求美人折？')
    '''
    poet = []
    poet.append('過故人莊 孟浩然')
    # poet.append('')
    poet.append('故人具雞黍，邀我至田家。')
    poet.append('綠樹村邊合，青山郭外斜。')
    poet.append('開軒面場圃，把酒話桑麻。')
    poet.append('待到重陽日，还來就菊花。')

    styleDict = {}
    styleDict['fill'] = 'black'
    styleDict['font-family'] = 'KaiTi'  # 'Microsoft YaHei'
    styleDict['font-size'] = '16px'
    # font-style: normal; font-variant: normal;

    styleList = get_styles(styleDict)

    W, H = svg.get_size()
    svg.draw(add_style('text', styleList))

    offsetx = 25
    offsety = 20
    x0 = W - 2 * offsetx
    y0 = offsety
    yInter = 16
    xInter = 32

    x = x0
    y = y0
    for i in poet:
        for c in i:
            svg.draw(draw_text_only(x, y, text=c))
            y = y + yInter
        y = y0
        x = x - xInter


def draw_poet2(svg):
    poet = []
    poet.append('紅樓夢')
    poet.append('可嘆停機德，')
    poet.append('堪憐詠絮才。')
    poet.append('玉帶林中掛，')
    poet.append('金簪雪裡埋。')

    styleDict = {}
    styleDict['fill'] = 'red'
    styleDict['font-family'] = 'Microsoft YaHei'
    styleDict['font-size'] = '24px'
    # font-style: normal; font-variant: normal;

    styleList = get_styles(styleDict)

    W, H = svg.get_size()
    svg.draw(add_style('text', styleList))

    offsetx = 28
    offsety = 42
    x0 = W - 2 * offsetx
    y0 = offsety
    yInter = 26
    xInter = 30

    x = x0
    y = y0
    for i in poet:
        for c in i:
            svg.draw(draw_text_only(x, y, text=c))
            y = y + yInter
        y = y0
        x = x - xInter


def draw_style_text(svg):
    text = '怡红快绿'
    styleDict = {}
    # styleDict['fill'] = 'black'
    styleDict['font-family'] = 'Microsoft YaHei'
    styleDict['font-size'] = '50px'

    styleList = get_styles(styleDict)

    W, H = svg.get_size()
    svg.draw(add_style('text', styleList))

    xInter = 60
    yInter = 60
    x0 = (W - xInter) / 2
    y0 = (H - yInter) / 2

    theta = 0
    w, h = 2, 2
    for i, c in enumerate(text):
        x = x0 + i % w * xInter
        y = y0 + i // w * yInter
        node = svg.draw(draw_text_only(x, y, text=c))
        svg.set_node(node, 'text-anchor', 'middle')
        svg.set_node(node, 'dominant-baseline', 'central')
        svg.set_node(node, 'fill', random_color())
        str_tmp = 'rotate({},{},{})'.format(theta, x, y)
        svg.set_node(node, 'transform', str_tmp)
        # svg.draw(draw_circle(x, y, 5, color='red'))
        theta += 90


def draw_style_text2(svg):
    text = 'Text rotation!'
    styleDict = {}
    styleDict['fill'] = 'black'
    styleDict['font-family'] = 'Consolas'
    styleDict['font-size'] = '24px'

    styleList = get_styles(styleDict)

    # W,H = svg.get_size()
    svg.draw(add_style('text', styleList))

    x0 = 10
    y0 = 30
    theta = 0
    for _ in range(6):
        node = svg.draw(draw_text_only(x0, y0, text))
        if 1:
            svg.set_node(node, 'rotate', theta)
        else:
            strTmp = 'rotate({},{},{})'.format(theta, x0, y0)
            svg.set_node(node, 'transform', strTmp)
            svg.set_node(node, 'text-anchor', 'middle')
            svg.set_node(node, 'dominant-baseline', 'central')

        y0 += 25
        theta += 30


def getSystemFonts():
    folder = r'C:\Windows\fonts'
    # return print(os.listdir(folder))
    for i in traverse_files(folder, 'ttf TTF ttc', True):
        print(i)


def main():
    # drawText()
    # getSystemFonts()

    file = gImageOutputPath + r'\text.svg'
    svg = SVGFileV2(file, W=200, H=200, border=True)
    # draw_poet(svg)
    draw_poet2(svg)
    # draw_style_text(svg)
    # draw_style_text2(svg)


if __name__ == '__main__':
    main()
