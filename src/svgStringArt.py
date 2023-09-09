# -*- encoding: utf-8 -*-
# Date: 23/Jul/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Simulate drawing pixel images using only svg line elements
Inspired by: https://www.youtube.com/watch?v=WGccIFf6MF8
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from itertools import combinations
from dataclasses import dataclass, field
import numpy as np
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svg.file import SVGFileV2
from svg.geo_math import get_regular_ngons, distance_pt_line, distance_array
from svg.basic import draw_any, draw_ring, draw_circle, draw_text, draw_rect
from svg.basic import draw_only_line, line_style
from svg.geo_transformation import translation_pts
from svg.progress_bar import SimpleProgressBar
from svgPointLine import drawPointsCircle_style, drawlinePoints
from svgImageMask import showimage, resizeImg, get_binary_image, rotateImg, loadGrayImg


def pseudo_inverse(matrix, b):
    """ https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse """
    return np.linalg.pinv(matrix).dot(b)


def test_pseudo_inverse():
    """ test pseudo inverse """
    a = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    b = np.array([[1], [2]])
    c = a.dot(b)

    d = pseudo_inverse(a, c)
    print('a=', a, a.shape)
    print('b=', b, b.shape)
    print('c=', c, c.shape)
    print('d=', d, d.shape)


@dataclass(slots=True)
class QuantumizeGrid:
    """ Cardioid class"""
    center: tuple
    radius: float
    quantum_divisions: int
    circle_division: int
    circle_points: np.array = None
    circle_lines: list[tuple] = field(default_factory=list)
    circle_lines_index: list[tuple] = field(default_factory=list)

    """ target image """
    pixel_image: str = None
    show_image: bool = True
    img_target: np.array = None

    """ optimization """
    search_batch: int = 1
    initial_strings: bool = False
    cumulative: bool = True

    """ quantum """
    grid_inter: float = 0
    diagonal_dis: float = 0
    circle_inner: bool = False
    grid_lines: list[tuple] = field(default_factory=list)
    grid_pts: list[tuple] = field(default_factory=list)
    grid_rects: list[tuple] = field(default_factory=list)
    grid_rects_center: list[tuple] = field(default_factory=list)
    grid_rect_matrix: np.array = None
    grid_matrix_all: np.array = None

    string_list: list[tuple] = field(default_factory=list)  # final enabled string list

    def __post_init__(self):
        self._calculate()

    def __repr__(self):
        return (rf'QuantumizeGrid object: radius={self.radius}, w/h={2*self.radius},'
                rf' circle_divisions={self.circle_division}, quantum_divisions={self.quantum_divisions}, '
                rf' lines={len(self.circle_lines_index)}, center={self.center}, inter={self.grid_inter}, diagonal_dis={self.diagonal_dis}')

    def _calculate(self):
        self.img_target = self._get_image()
        self._calculate_points_circle()
        self._calculate_quantum()
        self._calculate_lines()
        self._calculate_rects()
        self._calculate_rect_matrix()
        self._enabled_lines()

    def _calculate_points_circle(self):
        """ points on circle calculation """
        pts = get_regular_ngons(R=self.radius, N=self.circle_division)  # circle
        pts = translation_pts(pts, np.array([self.center[0], self.center[1]]), True)
        self.circle_points = pts
        # the order of pts is from far-east, clockwise
        # print('circle_points=', self.circle_points)
        for i in list(combinations(range(pts.shape[0]), 2)):
            # print(i)
            self.circle_lines_index.append((i[0], i[1]))
            start_pt = pts[i[0]]
            stop_pt = pts[i[1]]
            self.circle_lines.append((start_pt[0], start_pt[1], stop_pt[0], stop_pt[1]))

        self.circle_lines = np.round(self.circle_lines, decimals=4)
        # print('lines_index=', self.circle_lines_index)

    def _calculate_quantum(self):
        """ quantum calculation """
        self.grid_inter = 2 * self.radius / self.quantum_divisions
        self.diagonal_dis = np.sqrt(2 * np.square(self.grid_inter)) / 2.0
        for i in range(self.quantum_divisions + 1):
            x = -1 * self.radius + i * self.grid_inter
            y = self.radius
            if self.circle_inner:
                y = np.sqrt(np.square(self.radius) - np.square(x))
            self.grid_pts.append([x, -1 * y])  # start point
            self.grid_pts.append([x, y])  # stop point

        for i in range(self.quantum_divisions + 1):
            y = -1 * self.radius + i * self.grid_inter
            x = self.radius
            if self.circle_inner:
                x = np.sqrt(np.square(self.radius) - np.square(y))
            self.grid_pts.append([-1 * x, y])
            self.grid_pts.append([x, y])

        self.grid_pts = np.asarray(self.grid_pts)
        # print('self.grid_pts=', self.grid_pts, self.grid_pts.shape, len(self.grid_pts))
        self.grid_pts = translation_pts(self.grid_pts, np.array([self.center[0], self.center[1]]), True)

    def _calculate_lines(self):
        for i in range(len(self.grid_pts) // 2):
            start_pt = self.grid_pts[i * 2]
            stop_pt = self.grid_pts[i * 2 + 1]
            self.grid_lines.append((start_pt[0], start_pt[1], stop_pt[0], stop_pt[1]))

    def _calculate_rects(self):
        st_rect = []  # rect left up point
        for i in range(self.quantum_divisions):
            for j in range(self.quantum_divisions):
                x = -1 * self.radius + i * self.grid_inter
                y = -1 * self.radius + j * self.grid_inter
                st_rect.append([x, y])
        st_rect = np.asarray(st_rect)
        st_rect = translation_pts(st_rect, np.array([self.center[0], self.center[1]]), True)
        for i in st_rect:
            self.grid_rects.append([i[0], i[1], self.grid_inter, self.grid_inter])
            self.grid_rects_center.append([i[0] + self.grid_inter / 2, i[1] + self.grid_inter / 2])
        self.grid_rects = np.asarray(self.grid_rects)
        self.grid_rects_center = np.asarray(self.grid_rects_center)

    def _handle_line_matrix(self, m):
        m[m <= 1] = 0
        m[m >= 3] = 1
        m[m > 1] /= 3.0

        eff = 0.12 / m.shape[0]
        m *= (255 * eff)
        return m.flatten()

    def _calculate_rect_matrix(self):
        """ line matrix """
        self.grid_rect_matrix = np.zeros((self.quantum_divisions, self.quantum_divisions))

        line_num = len(self.circle_lines_index)
        all_matrix = np.zeros((line_num, self.quantum_divisions * self.quantum_divisions))

        progress = SimpleProgressBar(total=line_num, title='Calculate string\'s matrics')
        for i, index in enumerate(self.circle_lines_index):
            progress.update(i + 1)

            tmp = np.ones((self.quantum_divisions, self.quantum_divisions), dtype=np.float32)
            line = self.circle_lines[i]
            start_pt = np.array([line[0], line[1]])
            stop_pt = np.array([line[2], line[3]])

            # print('line:', i, index, line)
            for n, pt in enumerate(self.grid_rects_center):
                dis = distance_pt_line(pt, start_pt, stop_pt)
                # print(pt, 'dis=', dis)
                # calculate center of quantum rect to string's distance
                tmp[n // self.quantum_divisions][n % self.quantum_divisions] = dis / self.diagonal_dis
                # break

            all_matrix[i] = self._handle_line_matrix(tmp)
            # print('\all_matrix[i]=', i, '\n', all_matrix[i], all_matrix[i].shape)
            # print(i, all_matrix[i], all_matrix[i].shape, np.min(all_matrix[i]), np.max(all_matrix[i]))
        self.grid_matrix_all = all_matrix.T
        # print('grid_matrix_all.shape=', self.grid_matrix_all.shape)  # 45*64,  x(64*45), b(45x1), c: 64*1

    def _get_image(self):
        img = loadGrayImg(self.pixel_image)
        # img = get_binary_image(self.pixel_image, binary=True)
        img = resizeImg(img, self.quantum_divisions, self.quantum_divisions)
        if self.show_image:
            showimage(img)
        img = rotateImg(img, 270)
        print('img=', img, img.shape)
        return img.flatten()

    def _method_pseudo_inverse(self, matrix_all, target):
        """ pseudo inverse """
        c = pseudo_inverse(matrix_all, target)
        # print('before c.shape=', c, c.shape, np.min(c), np.max(c), np.mean(c), np.median(c), 'len=', len(c), 'sum=', np.sum(c))
        m = np.mean(c)  # 0  # np.median(c)
        m = m if m > 0 else 0
        c[c <= m] = 0
        c[c > m] = 1
        print('after c.shape=', c, c.shape, np.min(c), np.max(c), np.mean(c), np.median(c), 'len=', len(c), 'sum=', np.sum(c))
        self.string_list = c
        return c

    def _set_top_c(self, c, top=0.02):
        c[c < 0] = 0

        ind = c.argsort()[-1 * int(top * len(c)):][0]
        # ind = np.argpartition(c, 0)[-1 * int(top):]
        # min_c = np.min(c[ind])
        min_c = c[ind]
        c[c <= min_c] = 0
        c[c > min_c] = 1

    def _method_greedy_alg(self, matrix_all, target):
        """ greedy algorithm """
        c = np.zeros(matrix_all.shape[1])
        if self.initial_strings:
            c = pseudo_inverse(matrix_all, target)
            self._set_top_c(c)

        self.string_list = greedy_algorithm(matrix_all, target, c,
                                            self.circle_lines_index,
                                            self.search_batch, self.cumulative)

    def _enabled_lines(self):
        # self._method_pseudo_inverse(self.grid_matrix_all, self.img_target) # method 1: pseudo inverse
        self._method_greedy_alg(self.grid_matrix_all, self.img_target)   # method 2: greedy algorithm


def dis_target(cur_c, matrix_all, target, cumulative=True):
    """ calculate distance of current selected strings with target """
    # print('matrix_all: ', matrix_all, matrix_all.shape)
    # print('cur_c: ', cur_c, cur_c.shape)
    # print('target: ', target, target.shape)

    if cumulative:
        d = np.dot(matrix_all, cur_c)
    else:
        d = np.zeros(matrix_all.shape[0])
        columns = [i for i, v in enumerate(cur_c) if v == 1]
        # print('columns: ', columns)
        if len(columns) != 0:
            tmp = matrix_all[:, columns]
            # print('tmp: ', tmp, tmp.shape)
            # tmp = np.cumsum(tmp, axis=1)
            # print('tmp cumsun: ', tmp, tmp.shape)
            d = np.max(tmp, axis=1)
            # print('d: ', d, d.shape)

    d[d > 255] = 255
    # print('d: ', d, d.shape, np.min(d), np.max(d))
    return distance_array(d, target)


def get_next_search_indexs(cur_c, pts_indexs, last_indexs=None):
    res = []
    if last_indexs is None:
        for i in range(len(pts_indexs)):
            res.append(i)
    else:
        last_index = last_indexs[0]
        end_pt = pts_indexs[last_index][1]
        for n, i in enumerate(pts_indexs):
            if n != last_index and cur_c[n] == 0:
                if end_pt in (i[0], i[1]):
                    res.append(n)

        if len(res) == 0:
            indexs = [i for i, v in enumerate(cur_c) if v == 0]
            if len(indexs) == 0:
                return None
            return get_next_search_indexs(cur_c, pts_indexs, indexs)
    return res


def get_best_index(cur_c, matrix_all, target, batch, cumulative, pts_indexs, last_indexs):
    """ get new string index by finding the smallest distance to the target """
    indexs = [i for i, v in enumerate(cur_c) if v == 0]  # avaliable indexs
    # indexs = get_next_search_indexs(cur_c, pts_indexs, last_indexs)
    cur_dis = dis_target(cur_c, matrix_all, target, cumulative)

    cur_num = int(np.sum(cur_c))
    str_tmp = f'{cur_num}/{cur_c.shape[0]}/({round(cur_num * 100 /cur_c.shape[0], 2)}%)'
    # print('search indexs len: ', len(indexs), ', last_indexs: ', last_indexs)
    # print('cur_c:', cur_c, cur_c.shape)
    print('Cur strings:', str_tmp, ', cur distance:', np.round(cur_dis, 4), ', batch:', batch, ', last_indexs:', last_indexs)
    # print('cur_dis: ', cur_dis)

    dis_dict = {}
    progress = SimpleProgressBar(total=len(indexs), title='Search next best string')
    for n, i in enumerate(indexs):
        tmp_c = np.copy(cur_c)
        tmp_c[i] = 1
        # print('tmp_c=', tmp_c)
        dis = dis_target(tmp_c, matrix_all, target, cumulative)
        # print('\ni=', i, dis, cur_dis)
        if dis < cur_dis:
            dis_dict[i] = dis
        progress.update(n + 1)

    len_dis = len(dis_dict)
    # print('len_dis=', len_dis)
    if len_dis > 0:
        batch = batch if batch < len_dis else len_dis
        dis_dict = sorted(dis_dict.items(), key=lambda x: x[1], reverse=False)
        # print('dis_dict=', dis_dict)
        return [dis_dict[i][0] for i in range(batch)]
        # return dis_dict[0][0]  # index # dis_dict[0][1]  distance
    return None


def greedy_algorithm(matrix_all, target, c, pts_indexs, batch=1, cumulative=False):
    """ greedy algorithm to get the best strings to draw """
    print('matrix_all.shape=', matrix_all.shape, '[target vector/string numbers]')
    print('target=', target, target.shape)
    print('initial c: ', c, c.shape, 'string num=', int(np.sum(c)))
    print('batch=', batch)
    # print('pts_indexs=', pts_indexs)

    last_indexs = []
    while True:
        indexs = get_best_index(c, matrix_all, target, batch, cumulative, pts_indexs, last_indexs)
        if indexs is None:
            break
        for i in indexs:
            c[i] = 1
        last_indexs = indexs

    print('\nfinal c: ', c, c.shape, 'string num=', int(np.sum(c)))
    return c


def draw_basic_circle_bg(svg, g, data: QuantumizeGrid):
    """ draw background points and lines """
    cx, cy = data.center[0], data.center[1]

    ###### draw circle center ########
    svg.draw_node(g, draw_circle(cx, cy, radius=1, color='black'))

    ###### draw big circle ########
    svg.draw_node(g, draw_ring(cx, cy, radius=data.radius, stroke_width=0.5, stroke_color='green'))

    ###### draw points on circle ########
    drawPointsCircle_style(svg, data.circle_points, node=g, r=1, color='red', style_class='points')


def draw_quantum_color(svg, data: QuantumizeGrid):
    """ draw quantum cell color

    Args:
        svg (_type_): _description_
        data (QuantumizeGrid): _description_
    """
    print('all shape=', data.grid_matrix_all.T[0].shape)

    data.grid_rect_matrix = data.grid_matrix_all.T[15]
    c_matrix = data.grid_rect_matrix.reshape((data.quantum_divisions, data.quantum_divisions))

    print('rect shape=', c_matrix)
    for i, rt in enumerate(data.grid_rects):
        x = rt[0] + rt[2] / 2
        y = rt[1] + rt[3] / 2
        # print(i, rt, type(rt), x, y)

        color_v = c_matrix[i // data.quantum_divisions][i % data.quantum_divisions]
        color = 'white'
        if color_v == 255:
            color = 'white'
        elif color_v == 0:
            color = 'black'
        else:
            color = 'grey'
        svg.draw(draw_rect(rt[0], rt[1], rt[2], rt[3], color=color))
        svg.draw(draw_text(x, y, str(i)))
        # break


def draw_quantum(svg, data: QuantumizeGrid):
    """ quantum a circle plane """
    drawlinePoints(svg, data.grid_lines, svg.draw(draw_any('g', 'bg quantum')), color='black', stroke_width=0.02)
    # print('rects shape=', data.grid_rects.shape)
    # print('matrix shape=', data.grid_rect_matrix.shape)
    # draw_quantum_color(svg, data)


def draw_strings(svg, data: QuantumizeGrid):
    """ draw strings

    Args:
        svg (SVGFileV2): svg
        data (QuantumizeGrid): _description_
    """
    string_class = 'string'
    style_dict = line_style(color='black', stroke_width=0.1)
    svg.add_svg_style('.' + string_class, style_dict)

    g = svg.draw(draw_any('g'))
    n = 0
    for i, v in enumerate(data.string_list):
        line = data.circle_lines[i]
        if v == 1:
            node = svg.draw_node(g, draw_only_line(line[0], line[1], line[2], line[3]))
            svg.set_node(node, 'class', string_class)
            n += 1
    print('string numbers: ', n)


def draw_string_art(svg, src_img, r=90, circle_n=120, quantum_n=120, batch=1, initial=False, show=False):
    """ draw pixel image by using only strings

    Args:
        svg (_type_): svg handle
        src_img(str): source pixel image to draw
        r (float, optional): circle radius. Defaults to 180
        circle_n (int, optional): point numbers on circle
        quantum_n (int, optional): quantum numbers of the draw canvas
        batch(int, optional): Search batch size
        initial(bool, optional): Initialize some enabled string indexes to speed up searches
    """
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2  # center point of svg

    parameters = f'r:{r}, circle_n:{circle_n}, quantum_n:{quantum_n}, batch:{batch}, initial:{initial}, img:{src_img}'
    svg.set_title('draw strings art:' + parameters)
    print('Start to draw strings:', parameters)

    q_data = QuantumizeGrid((cx, cy), r, quantum_n, circle_n, pixel_image=src_img, search_batch=batch, initial_strings=initial, show_image=show)
    print(q_data)

    ###### draw points on circle ########
    draw_basic_circle_bg(svg, svg.draw(draw_any('g')), q_data)

    ###### draw all lines between points on circle ########
    # drawlinePoints(svg, q_data.circle_lines, svg.draw(draw_any('g', )), color='green', stroke_width=0.1)

    ###### draw quantumize lines for the circle ########
    draw_quantum(svg, q_data)

    ###### draw final strings ########
    draw_strings(svg, q_data)


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'strings_art.svg')
    svg = SVGFileV2(file, W=160, H=160, border=True)

    # file = r'.\res\A.png'
    # file = r'.\res\Lenna.png'
    file = r'.\res\gg.png'
    # file = r'.\res\da-82.png'
    # draw_string_art(svg, file, show=True)
    # draw_string_art(svg, file, batch=2, initial=True)
    # draw_string_art(svg, file, batch=4)
    draw_string_art(svg, file, r=70, circle_n=100, quantum_n=150, batch=1, show=True)


if __name__ == "__main__":
    main()
