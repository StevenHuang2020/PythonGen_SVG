# -*- encoding: utf-8 -*-
# Date: 24/Oct/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: svg animation
"""""""""""""""""""""""""""""""""""""""""""""""""""""

# https://developer.mozilla.org/en-US/docs/Web/SVG
# https://css-tricks.com/guide-svg-animations-smil/

from dataclasses import dataclass, field
import random
import numpy as np
from svg.basic import draw_circle, clip_float, draw_text
from svg.basic import random_color, reverse_hex, random_color_hsv
from svg.basic import rand_str, draw_tag, draw_any, random_point
from svg.basic import random_points, draw_path, draw_line, transfrom_dict
from svg.file import SVGFileV2
from svg.geo_math import get_distance, get_velocity_line_abc
from svg.geo_math import get_line_ABC_inter, get_perpendicular_point_line_ABC
from svg.geo_math import get_line_ABC, get_line_ABC_y, get_line_ABC_x
from svg.geo_transformation import rotation_pts_xy_point
from common import IMAGE_OUTPUT_PATH
from common_path import join_path
from svgPointLine import drawPloygonNode, drawlinePoints


def addNodeAnitmation(svg, object_node, animate_dict, element_name='animate'):
    animate = svg.draw_node(object_node, draw_tag(element_name))
    svg.set_node_dict(animate, animate_dict)


def createCircle(svg, x, y, r, color=None):
    id_str = 'circle_' + rand_str(4)
    color = color or random_color()
    circle = svg.draw(draw_circle(x, y, r, color=color))
    svg.set_node(circle, 'id', id_str)

    # rings
    svg.set_node(circle, 'fill', 'none')
    svg.set_node(circle, 'stroke-width', "2")
    svg.set_node(circle, 'stroke', color)
    return id, circle


def circleInflation(svg, x, y, r, color=None, from_r=0, to_r=0, dur_s=5, begin=None):
    x, y, r = clip_float(x), clip_float(y), clip_float(r)
    from_r, to_r = clip_float(from_r), clip_float(to_r)

    id_obj, circle = createCircle(svg, x, y, r, color)

    animate_dict = {}
    # animate_dict['xlink:href'] = f'#{id_obj}'
    animate_dict[f"{{{svg.xlink}}}" + 'href'] = f'#{id_obj}'
    animate_dict['id'] = 'ani_' + id_obj + '_' + rand_str(2)
    animate_dict['fill'] = 'freeze'
    animate_dict['attributeName'] = 'r'
    animate_dict['from'] = str(from_r)  # '10'
    animate_dict['to'] = str(to_r)  # '50'
    animate_dict['dur'] = str(dur_s)  # str(random.randint(0,dur_s)) #'5'
    animate_dict['begin'] = begin or str(random.randint(0, 5)) + 's'  # '0s' #'click' #
    animate_dict["repeatCount"] = "indefinite"  # "5"

    addNodeAnitmation(svg, circle, animate_dict)
    return id_obj, circle


def animCircleInflation(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    circleInflation(svg, cx, cy, r=10, from_r=10, to_r=50, dur_s=3)


def animCircleInflation2(svg):
    H, W = svg.get_size()

    N = 30  # total points
    offset = 10  # margin to border
    pts = random_points((N, 2), a=offset, b=W - offset)
    # print(pts)

    color = None  # "black" #None
    for pt in pts:
        r = random.randint(1, 6)
        circleInflation(svg, pt[0], pt[1], r=r, color=color, from_r=r, to_r=r * 5, dur_s=3)


def animCircleInflation3(svg):
    H, W = svg.get_size()

    block_size = 20  # blocksize
    color = "black"  # None #
    r0 = block_size / 2
    r_list = np.linspace(1, r0 * 3 / 4, 20)
    for i in range(0, W, block_size):
        for j in range(0, H, block_size):
            x = i + r0
            y = j + r0
            r = random.choice(r_list)
            circleInflation(svg, x, y, r=r, color=color, from_r=r, to_r=r0 * 3 / 4,
                            dur_s=random.randint(0, 10))


def animCircleInflation4(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 20  # total points
    r0 = 5
    r1 = 60

    color = "black"  # None #
    for i in range(N):
        begin = str(i) + 's'
        circleInflation(svg, cx, cy, r=r0, color=color, from_r=r0, to_r=r1, dur_s=4, begin=begin)


def animCircleInflation5(svg, N=20, r0=5, r1=60, offset=10, color=None):
    H, W = svg.get_size()
    # cx, cy = W // 2, H // 2

    pts = random_points((N, 2), a=offset, b=W - offset)
    r_list = np.linspace(1, r1 / 2, 20)
    for i in range(N):
        begin = str(random.randint(1, 4)) + 's'  # str(i)+'s' #'0s'
        id_obj, circle = circleInflation(svg, pts[i][0], pts[i][1],
                                         r=random.choice(r_list), color=color, from_r=r0, to_r=r1,
                                         dur_s=random.randint(3, 6), begin=begin)

        animate_dict = {}
        animate_dict[f"{{{svg.xlink}}}" + 'href'] = f'#{id_obj}'
        animate_dict['id'] = 'ani_' + id_obj + '_' + rand_str(2)
        animate_dict['attributeName'] = 'stroke-width'
        animate_dict['values'] = '0;2;4;2;1;0'
        animate_dict['dur'] = '5s'  # str(random.randint(0,dur_s)) #'5'
        animate_dict['begin'] = begin  # '0s'
        animate_dict["repeatCount"] = "indefinite"  # "5"
        addNodeAnitmation(svg, circle, animate_dict)


def drawNodeShape(svg, node, r=45, angle=np.pi / 5, times=8, theta=0):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    x0 = [cx, cx + 2 * r, cx + r]
    y0 = [cy, cy, cy - r * np.tan(angle)]
    # print('x0 ,y0=', x0 ,y0)

    for i in range(times):
        theta = i * (2 * np.pi / times)
        x, y = rotation_pts_xy_point(x0, y0, (cx, cy), theta)
        color = random_color_hsv()
        # color = random_color()
        drawPloygonNode(svg, node=node, pts=[(x[0], y[0]), (x[1], y[1]), (x[2], y[2])],
                        color=color)
        # drawPloygonNode(svg, node=node, pts=[(x[0],y[0]), (x[1],y[1]), (x[2],y[2])],
        # color=rainbow_color[i])

        # --------- draw text-------------- #
        dis = get_distance([x0[0], y0[0]], [x0[1], y0[1]])
        x_t = x0[0] + dis * 1.5 / 3
        y_t = y0[0] - (dis * 1.5 / 3) * np.tan(angle) * 0.6 / 2

        x_t = clip_float(x_t, 2)
        y_t = clip_float(y_t, 2)

        # print('x_t, y_t=', x_t, y_t)
        txt_child = svg.draw_node(node, draw_text(x_t, y_t, 'Love', color=reverse_hex(color)))
        svg.set_node(txt_child, 'transform', f'rotate({i * 360 / times},{x0[0]},{y0[0]})')
        svg.set_node(txt_child, 'text-anchor', 'middle')
        svg.set_node(txt_child, 'dominant-baseline', 'central')


def anim_Windmill(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')
    drawNodeShape(svg, g)

    trans_dict = transfrom_dict(cx, cy, cx, cy, dur=8)
    addNodeAnitmation(svg, g, trans_dict, element_name='animateTransform')


def drawAny(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    svg.set_title('you can draw anything by using draw_any()')

    g = svg.draw(draw_any('g', opacity=1.0))
    # anyNode = svg.draw_node(g, draw_any('test','222', a=10, b="4",c='red',xml='www.ss'))
    svg.draw_node(g, draw_any('test', 'hello'))

    any_dict = {}
    any_dict['test'] = 1
    any_dict['xml'] = 'www.ggg'
    any_dict['a'] = 'aaaaa anything else'
    any_dict['b'] = 'red black xxxxxxxxxxxxxxxxx anything you want'
    svg.draw_node(g, draw_any('test2', **any_dict))
    svg.draw_node(g, draw_any('hello', **any_dict))
    svg.draw_node(g, draw_any('anything', **any_dict))

    for i in range(20):
        any_dict = {}
        any_dict['cx'] = cx
        any_dict['cy'] = cy
        any_dict['r'] = '5'
        any_dict['stroke'] = '#80ff00'
        any_dict['stroke-width'] = '2'
        any_dict['fill'] = 'none'

        circle = svg.draw_node(g, draw_any('circle', **any_dict))
        # 'from' is a key word of python for import libs, but here last resort change parameter
        # from(attribute of animate element for svg) to 'From' to avoid conflict.
        svg.draw_node(circle, draw_any('animate', fill='freeze', attributeName='r', From="5", to="80",
                                       dur="4s", begin=str(i), repeatCount="indefinite"))

        any_dict = {}
        any_dict['fill'] = 'freeze'
        any_dict['attributeName'] = 'fill'
        any_dict['from'] = '#ff0000'
        any_dict['to'] = '#00ff40'
        any_dict['dur'] = '6s'
        any_dict['begin'] = '0s'
        any_dict['repeatCount'] = 'indefinite'
        # svg.draw_node(circle, draw_any('animate', **any_dict))

        any_dict['attributeName'] = 'stroke-width'
        any_dict['values'] = '1;2;3;2;1'
        any_dict.pop("from", None)
        any_dict.pop("to", None)
        svg.draw_node(circle, draw_any('animate', **any_dict))

        any_dict['attributeName'] = 'stroke'
        any_dict['from'] = '#80ff00'
        any_dict['to'] = '#0000ff'
        any_dict['begin'] = '1s'
        any_dict.pop("values", None)
        svg.draw_node(circle, draw_any('animate', **any_dict))


def draw_circle_path_anim(svg, node, path, radius, color='red', duration=None):
    circle = svg.draw_node(node, draw_circle(0, 0, radius=radius, color=color))

    animate_dict = {}

    if duration is None:
        animate_dict['dur'] = '5s'
    else:
        animate_dict['dur'] = f'{duration}s'
    animate_dict["repeatCount"] = "indefinite"
    animate_dict["path"] = path

    addNodeAnitmation(svg, circle, animate_dict, element_name='animateMotion')


def anim6(svg):
    def draw_moving_circle(svg, g, radius, y, offset_x, color='red', duration=None):
        path = f'M{radius + offset_x} {y} H{W - (radius + offset_x)} H{radius + offset_x}'
        # svg.draw_node(g, draw_path(path, stroke_width=0.5, color='green'))
        draw_circle_path_anim(svg, g, path, radius, color, duration)

    H, W = svg.get_size()
    print('H, W=', H, W)
    cx, cy = W // 2, H // 2

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')

    ver = cy
    r = 8
    offset_x = 0
    offset_y = 0

    draw_moving_circle(svg, g, radius=r, y=ver, offset_x=offset_x)

    N = 20
    for _ in range(N):
        rand_r = random.randint(2, r)
        rand_ver = random.randint(offset_y + rand_r, H - 2 * rand_r - offset_y)
        draw_moving_circle(svg, g, radius=rand_r, y=rand_ver,
                           offset_x=offset_x, duration=random.randint(3, 10),
                           color=random_color_hsv())


def get_points_path(pts, close=False):
    x = pts[0][0]
    y = pts[0][1]
    path = f'M {x:.1f} {y:.1f} L'
    for pt in pts[1:]:
        path = path + ' ' + str(pt[0]) + ' ' + str(pt[1])

    if close:
        path += ' Z'
    return path


def draw_ball_movin(svg, node, radius, start_pt, step_x, step_y, N=500,
                    color=None, draw_path_line=False):
    H, W = svg.get_size()
    ball = BallCoordinates(x=start_pt[0], y=start_pt[1],
                           vx=step_x, vy=step_y,
                           width=W, height=H, offset=radius, N=N)
    coords = ball.get_coordinates()
    # print('coords=', coords, len(coords))

    path = get_points_path(coords, False)

    # draw path line
    if draw_path_line:
        svg.draw_node(node, draw_path(path, stroke_width=0.5, color='green'))

    # print('path=', path[:50])
    draw_circle_path_anim(svg, node, path, radius, duration=len(coords) * 2.8, color=color)


def anim7(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    # define gradient color
    color_id = 'myGradient'
    defs = svg.draw(draw_any('defs'))
    grad = svg.draw_node(defs, draw_any('radialGradient ', id=f'{color_id}'))

    stop_dict = {}
    stop_dict['offset'] = '2%'
    stop_dict['stop-color'] = 'gold'
    svg.draw_node(grad, draw_any('stop', None, **stop_dict))
    stop_dict['offset'] = '90%'
    stop_dict['stop-color'] = 'red'
    svg.draw_node(grad, draw_any('stop', None, **stop_dict))

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')

    r = 8
    pt = [cx, cy]
    # color = 'red'
    color = f"url('#{color_id}')"
    draw_ball_movin(svg, g, r, start_pt=pt, step_x=-2, step_y=3, N=500,
                    color=color, draw_path_line=True)


def anim8(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')
    pt = (cx, cy)
    for _ in range(100):
        r = random.randint(2, 8)
        # pt = (random.randint(2+r, W-2-r), random.randint(2+r, H-2-r))
        sx = random.randint(1, 8) * [-1, 1][random.randrange(2)]
        sy = random.randint(1, 8) * [-1, 1][random.randrange(2)]
        # print('r, sx, sy=', r, sx, sy)
        draw_ball_movin(svg, g, r, start_pt=pt, step_x=sx, step_y=sy, N=800,
                        color=random_color_hsv())


@dataclass(slots=True)
class BallCoordinates:
    """get coordinates of a bouncing ball in a rect[0, 0, W, H]
    """
    x: float
    y: float
    vx: float
    vy: float
    width: int
    height: int
    offset: int
    N: int
    coordinates: list[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        self.coordinates.append([self.x, self.y])
        self.generate(N=self.N)

    def generate(self, N=100):
        for _ in range(N):
            self.move_offset()  # self.move()
        # print(self.coordinates, len(self.coordinates))

    def get_coordinates(self):
        return np.asarray(self.coordinates)

    def move_offset(self):
        # Add the velocity to position.
        self.x += self.vx
        self.y += self.vy

        # Bounce off vertical walls, if necessary.
        if (self.x < self.offset or self.x > self.width - self.offset):
            # Flip the horizontal velocity.
            self.vx = -1 * self.vx

            if self.x < self.offset:  # if now negative, must be 2nd case
                self.x = self.offset
            else:
                self.x = self.width - self.offset

            self.coordinates.append([self.x, self.y])

        # Bounce off horizontal walls, if necessary.
        if (self.y < self.offset or self.y > self.height - self.offset):
            # Follow the same logic as above.
            self.vy = -1 * self.vy

            if self.y < self.offset:
                self.y = self.offset
            else:
                self.y = self.height - self.offset

            self.coordinates.append([self.x, self.y])
        # self.coordinates.append([self.x, self.y])

    # Called every frame with the current screen width and height.
    def move(self):
        # Add the velocity to position.
        self.x += self.vx
        self.y += self.vy

        # Bounce off vertical walls, if necessary.
        if (self.x < 0 or self.x > self.width):
            # Flip the horizontal velocity.
            self.vx = -1 * self.vx

            # If x is negative (the ball is off the screen to the left),
            # then simply flipping its sign is enough to move it to where
            # we want it to be. Otherwise (the ball is off the screen to
            # the right), we need to take the excess x - width and subtract
            # it from the screen width, yielding x = width - (x - width) =
            # width - x + width = 2*width - x. Either way, we negate x. In
            # the first case, we’re done in the second, we just need to
            # add 2*width.

            if self.x < 0:  # if now negative, must be 2nd case
                self.x = -1 * self.x
            else:
                self.x = 2 * self.width - self.x

            # self.coordinates.append([self.x, self.y])

        # Bounce off horizontal walls, if necessary.
        if (self.y < 0 or self.y > self.height):
            # Follow the same logic as above.
            self.vy = -1 * self.vy

            if self.y < 0:
                self.y = -1 * self.y
            else:
                self.y = 2 * self.height - self.y

            # self.coordinates.append([self.x, self.y])
        self.coordinates.append([self.x, self.y])


def draw_line_param(svg, node, a, b, min_x=0, max_x=100):
    """draw line  y= a*x + b"""

    def fun(x):
        return a * x + b

    # x = np.linspace(min_x, max_x, N)
    # y = a * x + b
    # start_pt = [min_x, fun(min_x)]
    # stop_pt = [max_x, fun(max_x)]
    pts = [[min_x, fun(min_x), max_x, fun(max_x)]]
    drawlinePoints(svg, pts, node)


def draw_line_param_abc(line, min_x=0, max_x=100, min_y=0, max_y=100):
    """draw line  a*x + b*y + c = 0, line=[a, b, c]"""
    a, b, _ = line[0], line[1], line[2]
    pts = []
    if a == 0 and b == 0:
        print('Warning, line parameters error!')
        return pts

    if b == 0:
        pts = [[get_line_ABC_x(line, min_y), min_y, get_line_ABC_x(line, max_y), max_y]]
    else:
        pts = [[min_x, get_line_ABC_y(line, min_x), max_x, get_line_ABC_y(line, max_x)]]

    return pts


def get_math_bounce_parameter(line, pt, vx, vy):
    """get math parameter of a ball bounce with a line from point pt

    Args:
        line (array): [a, b, c], a*x + b*y + c = 0
        pt (point): [x, y] or (x, y)
        vx (real value): x speed
        vy (real value): y speed
    """
    perpend_pt = get_perpendicular_point_line_ABC(line, pt)  # perpendicular root point
    reflect_pt = get_perpendicular_point_line_ABC(line, pt, True)  # reflection point
    path_line = get_velocity_line_abc(pt, vx, vy)
    inter_pt = get_line_ABC_inter(line, path_line)
    reflect_line = get_line_ABC(inter_pt, reflect_pt)
    return (perpend_pt, reflect_pt, inter_pt, path_line, reflect_line)


def anim9(svg, vx=-2, vy=1):
    """moving ball bounce with a line"""
    H, W = svg.get_size()

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')

    wall_line = [2, -1.8, 1]  # line parameters
    pt = random_point(4, W - 5)
    # print(pt, type(pt))

    res = get_math_bounce_parameter(wall_line, pt, vx, vy)
    perpend_pt, reflect_pt, inter_pt, path_line, reflect_line = res

    # draw_line_param(svg, g, a, b, 0, W)
    pts = draw_line_param_abc(wall_line, 0, W, 0, H)
    drawlinePoints(svg, pts, g, color='black')

    svg.draw_node(g, draw_circle(pt[0], pt[1], 1, color='black'))
    svg.draw_node(g, draw_circle(perpend_pt[0], perpend_pt[1], 1, color='red'))
    svg.draw_node(g, draw_circle(reflect_pt[0], reflect_pt[1], 1, color='red'))
    svg.draw_node(g, draw_circle(inter_pt[0], inter_pt[1], 1, color='black'))

    svg.draw_node(g, draw_line(pt[0], pt[1], reflect_pt[0], reflect_pt[1], stroke_dasharray="2"))
    svg.draw_node(g, draw_line(inter_pt[0], inter_pt[1], reflect_pt[0], reflect_pt[1],
                               stroke_dasharray="2"))

    if inter_pt is not None:
        min_x = min(pt[0], inter_pt[0])
        max_x = max(pt[0], inter_pt[0])
        min_y = min(pt[1], inter_pt[1])
        max_y = min(pt[1], inter_pt[1])
        pts = draw_line_param_abc(path_line, min_x, max_x, min_y, max_y)
        drawlinePoints(svg, pts, g, color='black')

    coords = [pt, inter_pt]
    if reflect_pt is not None:
        min_x, max_x = 0, W
        min_y, max_y = 0, H

        far_pt = [0, 0]
        if reflect_pt[0] < inter_pt[0]:
            min_x = inter_pt[0]

            far_pt[0] = max_x
            far_pt[1] = get_line_ABC_y(reflect_line, far_pt[0])
        else:
            max_x = inter_pt[0]
            far_pt[0] = min_x
            far_pt[1] = get_line_ABC_y(reflect_line, far_pt[0])

        pts = draw_line_param_abc(reflect_line, min_x, max_x, min_y, max_y)
        drawlinePoints(svg, pts, g, color='black')

        coords.append(far_pt)
        coords = np.asarray(coords)
        print('coords=', coords, coords.shape)
    path = get_points_path(coords, False)
    draw_circle_path_anim(svg, g, path, radius=6, duration=len(coords) * 1.0, color='red')


def anim10(svg):
    """moving ball bounce with a line"""
    H, W = svg.get_size()

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')

    wall_line = [2, -1.8, 1]  # line parameters

    drawlinePoints(svg, draw_line_param_abc(wall_line, 0, W, 0, H),
                   g, color='black')

    for _ in range(50):
        pt = random_point(4, W - 5)
        # print(pt, type(pt))
        vx = random.randint(1, 5) * [-1, 1][random.randrange(2)]
        vy = random.randint(1, 5) * [-1, 1][random.randrange(2)]

        res = get_math_bounce_parameter(wall_line, pt, vx, vy)
        _, reflect_pt, inter_pt, _, reflect_line = res

        coords = [pt, inter_pt]
        if reflect_pt is not None:
            min_x, max_x = 0, W

            far_pt = [0, 0]
            if reflect_pt[0] < inter_pt[0]:
                min_x = inter_pt[0]

                far_pt[0] = max_x
                far_pt[1] = get_line_ABC_y(reflect_line, far_pt[0])
            else:
                max_x = inter_pt[0]
                far_pt[0] = min_x
                far_pt[1] = get_line_ABC_y(reflect_line, far_pt[0])

            coords.append(far_pt)
            coords = np.asarray(coords)

        path = get_points_path(coords, False)
        draw_circle_path_anim(svg, g, path, radius=5, duration=len(coords) * 1.0, color='red')


def main():
    """ main function """
    file = join_path(IMAGE_OUTPUT_PATH, r'animation.svg')
    svg = SVGFileV2(file, W=200, H=200, border=True)

    # animCircleInflation(svg)
    # animCircleInflation2(svg)
    # animCircleInflation3(svg)
    # animCircleInflation4(svg)
    # animCircleInflation5(svg)
    # anim_Windmill(svg)
    # drawAny(svg)
    # anim6(svg)
    # anim7(svg)
    # anim8(svg)
    anim9(svg)
    # anim10(svg)


if __name__ == '__main__':
    main()
