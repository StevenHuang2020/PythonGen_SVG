#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Profile svg
# Date: 2021/09/14
# Author: Steven Huang, Auckland, NZ
from svg.basic import draw_any, add_style, get_styles, draw_rect, draw_path
from svg.file import SVGFileV2
from common import gImageOutputPath
from common_path import join_path, abs_path
from svgImageMask import get_binary_image, get_potrace_path, path_potrace_jagged_trans


class ProfileStyleSimple:
    """Profile svg class"""

    def __init__(self, svg, dataDict=None):
        self.svg = svg
        self.dataDict = dataDict
        self._draw_()

    def _prepare_svg(self):  # style css define
        self.svg.draw(draw_any('title ', text=self.dataDict['name']))
        styleNode = self.svg.draw(draw_any('style ', type="text/css"))

        dictStyle = {'fill': "black", 'font-family': "sans-serif", 'font-size': '28px'}
        self.svg.add_child(styleNode, self.svg.new_node(add_style('.big', get_styles(dictStyle))))
        dictStyle = {'fill': "black", 'font-family': "sans-serif", 'font-size': '20px'}
        self.svg.add_child(styleNode, self.svg.new_node(add_style('.small', get_styles(dictStyle))))
        dictStyle = {'fill': "black", 'font-family': "cursive", 'font-size': '20px'}  # cursive  fantasy monospace
        self.svg.add_child(styleNode, self.svg.new_node(add_style('.bodyText', get_styles(dictStyle))))

    def _draw_(self):
        self._prepare_svg()
        H, W = self.svg.get_size()
        # ----------------header------------------- #
        dictLink = {}
        dictLink["{{{}}}".format(self.svg._xlink) + 'href'] = self.dataDict['wiki']
        aLink = self.svg.draw(draw_any(tag='a'))
        self.svg.set_node_dict(aLink, dictLink)

        itemW = 110
        itemH = 150
        styleImg = {}
        styleImg['width'] = str(itemW)
        styleImg['height'] = str(itemH)
        styleImg['x'] = str(0)
        styleImg['y'] = str(0)
        styleImg['href'] = self.dataDict['photo']

        if 0:
            # self.svg.draw(draw_any('image', **styleImg))
            self.svg.add_child(aLink, self.svg.new_node(draw_any('image', **styleImg)))
        else:
            self.draw_portrait(aLink, styleImg['href'], itemW, itemH, (0, 0))

        y0 = 30
        x0 = itemW + 5
        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0, text=self.dataDict['name']))
        self.svg.set_node(node, 'class', 'big')

        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 30, text=self.dataDict['name_cn']))
        self.svg.set_node(node, 'class', 'big')

        date = '(' + self.dataDict['date_birth'] + ' - ' + self.dataDict['date_death'] + ')'
        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 60, text=date))
        self.svg.set_node(node, 'class', 'small')

        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 90, text=self.dataDict['profile']))
        self.svg.set_node(node, 'class', 'small')

        # ----------------split line--------------- #
        self.svg.draw(draw_rect(x=0, y=itemH, width=W, height=0.01 * H, stroke_width=0.2, color='#FCC64A'))

        # ----------------body--------------------- #
        y0 = itemH + 10
        nodeTextBody = self.svg.draw(draw_any(tag='text'))
        self.svg.set_node(nodeTextBody, 'class', 'bodyText')

        dictStyle = {'dy': "0.2em", 'x': "10"}
        for i, txts in enumerate(self.dataDict['quotes'], start=1):
            # dictStyle['y'] = str(y0)
            for k, lineText in enumerate(txts, start=1):
                if k == 1:
                    s = str(i) + '. ' + lineText
                else:
                    s = lineText

                y0 += 30
                dictStyle['y'] = str(y0)
                line = self.svg.new_node(draw_any(tag='tspan', text=s, **dictStyle))
                self.svg.add_child(nodeTextBody, line)
            y0 += 20

    def draw_portrait(self, node, file, width, height, to_point=(0, 0)):
        image = get_binary_image(file, binary=True)
        W = image.shape[1]
        H = image.shape[0]
        paths = get_potrace_path(image)

        path = path_potrace_jagged_trans(paths, zoom_x=width / W, zoom_y=height / H, to_point=to_point)
        # print('len(path)=', len(path))
        self.svg.draw_node(node, draw_path(path, color='none', fill_color='black', fill_rule='evenodd'))


def Nietzsche():
    file = join_path(gImageOutputPath, r'Nietzsche.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    dataDict = {}
    dataDict['name'] = 'Friedrich Wilhelm Nietzsche'
    dataDict['name_cn'] = '弗里德里希·威廉·尼采'
    dataDict['wiki'] = 'https://en.wikipedia.org/wiki/Friedrich_Nietzsche'
    dataDict['date_birth'] = '15 October 1844'
    dataDict['date_death'] = '25 August 1900'
    dataDict['photo'] = abs_path(r'.\res\download\nicai.jpg')
    dataDict['profile'] = 'German philosopher, cultural critic, composer, poet, writer.'
    dataDict['quotes'] = []

    dataDict['quotes'].append('Without music, life would be a mistake.'.splitlines())
    dataDict['quotes'].append('That which does not kill us makes us stronger.'.splitlines())
    dataDict['quotes'].append('To live is to suffer, to survive is to find some \rmeaning in the suffering.'.splitlines())
    dataDict['quotes'].append('We should consider every day lost on which we have not \rdanced at least once.'.splitlines())
    dataDict['quotes'].append('A person who knows why he lives, can endure any kind of life.'.splitlines())
    dataDict['quotes'].append('An unfortunate marriage is not a lack of love, but \ra lack of friendship.'.splitlines())
    dataDict['quotes'].append('God is dead.'.splitlines())
    dataDict['quotes'].append('My time has not come, and some people are born after death.'.splitlines())
    dataDict['quotes'].append('You might as well take a bold risk in life because \ryou have to lose it.'.splitlines())
    dataDict['quotes'].append('The man of knowledge must be able not only to \rlove his enemies but also to hate his friends.'.splitlines())

    ProfileStyleSimple(svg, dataDict)


def KarlPopper():
    file = join_path(gImageOutputPath, r'KarlPopper.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    dataDict = {}
    dataDict['name'] = 'Karl Raimund Popper'
    dataDict['name_cn'] = '卡尔·雷蒙德·波普尔'
    dataDict['wiki'] = 'https://en.wikipedia.org/wiki/Karl_Popper'
    dataDict['date_birth'] = '28 July 1902'
    dataDict['date_death'] = '17 September 1994'
    dataDict['photo'] = abs_path(r'.\res\download\Karl_Popper.jpg')
    dataDict['profile'] = ' Austrian-British philosopher, \rand social commentator'
    dataDict['quotes'] = []

    dataDict['quotes'].append('Science must begin with myths, and with the criticism of myths.'.splitlines())
    dataDict['quotes'].append('Unlimited tolerance must lead to the disappearance of tolerance.'.splitlines())
    dataDict['quotes'].append('Our knowledge can only be finite, while our ignorance must \rnecessarily be infinite.'.splitlines())
    dataDict['quotes'].append('True ignorance is not the absence of knowledge, \rbut the refusal to acquire it.'.splitlines())
    dataDict['quotes'].append('Those who promise us paradise on earth never \rproduced anything but a hell.'.splitlines())
    dataDict['quotes'].append('A theory that explains everything, explains nothing.'.splitlines())
    dataDict['quotes'].append('All life is problem solving.'.splitlines())
    dataDict['quotes'].append('While differing widely in the various little bits we know, \rin our infinite ignorance we are all equal.'.splitlines())
    dataDict['quotes'].append('Science may be described as the art of systematic \roversimplification.'.splitlines())
    ProfileStyleSimple(svg, dataDict)


def Socrates():
    file = join_path(gImageOutputPath, r'Socrates.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    dataDict = {}
    dataDict['name'] = 'Socrates'
    dataDict['name_cn'] = '苏格拉底'
    dataDict['wiki'] = 'https://en.wikipedia.org/wiki/Socrates'
    dataDict['date_birth'] = '470 BC'
    dataDict['date_death'] = '399 BC'
    dataDict['photo'] = abs_path(r'.\res\download\Socrates.jpg')
    dataDict['profile'] = 'Ancient Greek philosopher'
    dataDict['quotes'] = []

    dataDict['quotes'].append('An unexamined life is not worth living.'.splitlines())
    dataDict['quotes'].append('One thing only I know, and that is that I know nothing.'.splitlines())
    dataDict['quotes'].append('True knowledge exists in knowing that you know nothing.'.splitlines())
    dataDict['quotes'].append('I know that I am intelligent, because I know that I know nothing.'.splitlines())
    dataDict['quotes'].append('I cannot teach anybody anything, I can only make them think.'.splitlines())
    dataDict['quotes'].append('To find yourself, think for yourself.'.splitlines())
    dataDict['quotes'].append('Education is the kindling of a flame, not the filling of a vessel.'.splitlines())
    dataDict['quotes'].append('An honest man is always a child.'.splitlines())
    dataDict['quotes'].append('The only true wisdom is in knowing you know nothing.'.splitlines())
    dataDict['quotes'].append('There is only one good, knowledge, and one evil, ignorance.'.splitlines())
    dataDict['quotes'].append('Wonder is the beginning of wisdom.'.splitlines())
    dataDict['quotes'].append('He who is not contented with what he has, would not \rbe contented with what he would like to have.'.splitlines())

    ProfileStyleSimple(svg, dataDict)


def main():
    # Socrates()
    # Nietzsche()
    KarlPopper()


if __name__ == "__main__":
    main()
