# -*- encoding: utf-8 -*-
# Date: 14/Sep/2021
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: SVG profile drawing
"""""""""""""""""""""""""""""""""""""""""""""""""""""
from svg.basic import draw_any, add_style, get_styles, draw_rect, draw_path
from svg.file import SVGFileV2
from common import IMAGE_OUTPUT_PATH
from common_path import join_path, abs_path
from svgImageMask import get_binary_image, get_potrace_path, path_potrace_jagged_trans


class ProfileStyleSimple:
    """Profile svg class"""

    def __init__(self, svg, data_dict=None):
        self.svg = svg
        self.data_dict = data_dict
        self._draw_()

    def _prepare_svg(self):  # style css define
        self.svg.draw(draw_any('title ', text=self.data_dict['name']))
        style_node = self.svg.draw(draw_any('style ', type="text/css"))

        dict_style = {'fill': "black", 'font-family': "sans-serif", 'font-size': '28px'}
        self.svg.add_child(style_node, self.svg.new_node(add_style('.big', get_styles(dict_style))))
        dict_style = {'fill': "black", 'font-family': "sans-serif", 'font-size': '20px'}
        self.svg.add_child(style_node, self.svg.new_node(add_style('.small', get_styles(dict_style))))
        # cursive  fantasy monospace
        dict_style = {'fill': "black", 'font-family': "cursive", 'font-size': '20px'}
        self.svg.add_child(style_node, self.svg.new_node(add_style('.bodyText', get_styles(dict_style))))

    def _draw_(self):
        self._prepare_svg()
        H, W = self.svg.get_size()
        # ----------------header------------------- #
        dict_link = {}
        dict_link[f"{{{self.svg._xlink}}}" + 'href'] = self.data_dict['wiki']
        a_link = self.svg.draw(draw_any(tag='a'))
        self.svg.set_node_dict(a_link, dict_link)

        item_w = 110
        item_h = 150
        style_img = {}
        style_img['width'] = str(item_w)
        style_img['height'] = str(item_h)
        style_img['x'] = str(0)
        style_img['y'] = str(0)
        style_img['href'] = self.data_dict['photo']

        if 0:
            # self.svg.draw(draw_any('image', **style_img))
            self.svg.add_child(a_link, self.svg.new_node(draw_any('image', **style_img)))
        else:
            self.draw_portrait(a_link, style_img['href'], item_w, item_h, (0, 0))

        y0 = 30
        x0 = item_w + 5
        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0, text=self.data_dict['name']))
        self.svg.set_node(node, 'class', 'big')

        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 30, text=self.data_dict['name_cn']))
        self.svg.set_node(node, 'class', 'big')

        date = '(' + self.data_dict['date_birth'] + ' - ' + self.data_dict['date_death'] + ')'
        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 60, text=date))
        self.svg.set_node(node, 'class', 'small')

        node = self.svg.draw(draw_any(tag='text', x=x0, y=y0 + 90, text=self.data_dict['profile']))
        self.svg.set_node(node, 'class', 'small')

        # ----------------split line--------------- #
        self.svg.draw(draw_rect(x=0, y=item_h, width=W, height=0.01 * H, stroke_width=0.2,
                                color='#FCC64A'))

        # ----------------body--------------------- #
        y0 = item_h + 10
        node_text_body = self.svg.draw(draw_any(tag='text'))
        self.svg.set_node(node_text_body, 'class', 'bodyText')

        dict_style = {'dy': "0.2em", 'x': "10"}
        for i, txts in enumerate(self.data_dict['quotes'], start=1):
            # dict_style['y'] = str(y0)
            for k, line_text in enumerate(txts, start=1):
                if k == 1:
                    s = str(i) + '. ' + line_text
                else:
                    s = line_text

                y0 += 30
                dict_style['y'] = str(y0)
                line = self.svg.new_node(draw_any(tag='tspan', text=s, **dict_style))
                self.svg.add_child(node_text_body, line)
            y0 += 20

    def draw_portrait(self, node, file, width, height, to_point=(0, 0)):
        image = get_binary_image(file, binary=True)
        W = image.shape[1]
        H = image.shape[0]
        paths = get_potrace_path(image)

        path = path_potrace_jagged_trans(paths, zoom_x=width / W, zoom_y=height / H,
                                         to_point=to_point)
        # print('len(path)=', len(path))
        self.svg.draw_node(node, draw_path(path, color='none', fill_color='black',
                                           fill_rule='evenodd'))


def Nietzsche():
    file = join_path(IMAGE_OUTPUT_PATH, r'Nietzsche.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    data_dict = {}
    data_dict['name'] = 'Friedrich Wilhelm Nietzsche'
    data_dict['name_cn'] = '弗里德里希·威廉·尼采'
    data_dict['wiki'] = 'https://en.wikipedia.org/wiki/Friedrich_Nietzsche'
    data_dict['date_birth'] = '15 October 1844'
    data_dict['date_death'] = '25 August 1900'
    data_dict['photo'] = abs_path(r'.\res\download\nicai.jpg')
    data_dict['profile'] = 'German philosopher, cultural critic, composer, poet, writer.'
    data_dict['quotes'] = []

    data_dict['quotes'].append('Without music, life would be a mistake.'.splitlines())
    data_dict['quotes'].append('That which does not kill us makes us stronger.'.splitlines())
    data_dict['quotes'].append('To live is to suffer, to survive is to find some \rmeaning in the suffering.'.splitlines())
    data_dict['quotes'].append('We should consider every day lost on which we have not \rdanced at least once.'.splitlines())
    data_dict['quotes'].append('A person who knows why he lives, can endure any kind of life.'.splitlines())
    data_dict['quotes'].append('An unfortunate marriage is not a lack of love, but \ra lack of friendship.'.splitlines())
    data_dict['quotes'].append('God is dead.'.splitlines())
    data_dict['quotes'].append('My time has not come, and some people are born after death.'.splitlines())
    data_dict['quotes'].append('You might as well take a bold risk in life because \ryou have to lose it.'.splitlines())
    data_dict['quotes'].append('The man of knowledge must be able not only to \rlove his enemies but also to hate his friends.'.splitlines())

    ProfileStyleSimple(svg, data_dict)


def KarlPopper():
    file = join_path(IMAGE_OUTPUT_PATH, r'KarlPopper.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    data_dict = {}
    data_dict['name'] = 'Karl Raimund Popper'
    data_dict['name_cn'] = '卡尔·雷蒙德·波普尔'
    data_dict['wiki'] = 'https://en.wikipedia.org/wiki/Karl_Popper'
    data_dict['date_birth'] = '28 July 1902'
    data_dict['date_death'] = '17 September 1994'
    data_dict['photo'] = abs_path(r'.\res\download\Karl_Popper.jpg')
    data_dict['profile'] = ' Austrian-British philosopher, \rand social commentator'
    data_dict['quotes'] = []

    data_dict['quotes'].append('Science must begin with myths, and with the criticism of myths.'.splitlines())
    data_dict['quotes'].append('Unlimited tolerance must lead to the disappearance of tolerance.'.splitlines())
    data_dict['quotes'].append('Our knowledge can only be finite, while our ignorance must \rnecessarily be infinite.'.splitlines())
    data_dict['quotes'].append('True ignorance is not the absence of knowledge, \rbut the refusal to acquire it.'.splitlines())
    data_dict['quotes'].append('Those who promise us paradise on earth never \rproduced anything but a hell.'.splitlines())
    data_dict['quotes'].append('A theory that explains everything, explains nothing.'.splitlines())
    data_dict['quotes'].append('All life is problem solving.'.splitlines())
    data_dict['quotes'].append('While differing widely in the various little bits we know, \rin our infinite ignorance we are all equal.'.splitlines())
    data_dict['quotes'].append('Science may be described as the art of systematic \roversimplification.'.splitlines())
    ProfileStyleSimple(svg, data_dict)


def Socrates():
    file = join_path(IMAGE_OUTPUT_PATH, r'Socrates.svg')
    svg = SVGFileV2(file, W=660, H=800, border=True)

    data_dict = {}
    data_dict['name'] = 'Socrates'
    data_dict['name_cn'] = '苏格拉底'
    data_dict['wiki'] = 'https://en.wikipedia.org/wiki/Socrates'
    data_dict['date_birth'] = '470 BC'
    data_dict['date_death'] = '399 BC'
    data_dict['photo'] = abs_path(r'.\res\download\Socrates.jpg')
    data_dict['profile'] = 'Ancient Greek philosopher'
    data_dict['quotes'] = []

    data_dict['quotes'].append('An unexamined life is not worth living.'.splitlines())
    data_dict['quotes'].append('One thing only I know, and that is that I know nothing.'.splitlines())
    data_dict['quotes'].append('True knowledge exists in knowing that you know nothing.'.splitlines())
    data_dict['quotes'].append('I know that I am intelligent, because I know that I know nothing.'.splitlines())
    data_dict['quotes'].append('I cannot teach anybody anything, I can only make them think.'.splitlines())
    data_dict['quotes'].append('To find yourself, think for yourself.'.splitlines())
    data_dict['quotes'].append('Education is the kindling of a flame, not the filling of a vessel.'.splitlines())
    data_dict['quotes'].append('An honest man is always a child.'.splitlines())
    data_dict['quotes'].append('The only true wisdom is in knowing you know nothing.'.splitlines())
    data_dict['quotes'].append('There is only one good, knowledge, and one evil, ignorance.'.splitlines())
    data_dict['quotes'].append('Wonder is the beginning of wisdom.'.splitlines())
    data_dict['quotes'].append('He who is not contented with what he has, would not \rbe contented with what he would like to have.'.splitlines())

    ProfileStyleSimple(svg, data_dict)


def main():
    """ main function """
    # Socrates()
    # Nietzsche()
    KarlPopper()


if __name__ == "__main__":
    main()
