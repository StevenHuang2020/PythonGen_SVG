# python3 Steven 10/24/20 Auckland,NZ
# https://developer.mozilla.org/en-US/docs/Web/SVG
# https://css-tricks.com/guide-svg-animations-smil/
import random
import numpy as np
from svg.basic import draw_circle, clip_float, draw_text
from svg.basic import random_color, rainbow_colors, reverse_hex, random_color_hsv
from svg.basic import rand_str, draw_tag, draw_any, draw_polygon, random_point
from svg.basic import random_points, draw_path
from svg.file import SVGFileV2
from svg.geo_math import get_distance
from common import gImageOutputPath
from svg.geo_transformation import rotation_pts_xy_point, reflection_points
from svg.geo_transformation import combine_xy, translation_pts, translation_pts_xy
from svgPointLine import drawPloygonNode


def addNodeAnitmation(svg, objectNode, animateDict, elementName='animate'):
    animate = svg.draw_node(objectNode, draw_tag(elementName))
    svg.set_node_dict(animate, animateDict)


def createCircle(svg, x, y, r, color=None):
    id = 'circle_' + rand_str(4)
    color = color or random_color()
    circle = svg.draw(draw_circle(x, y, r, color=color))
    svg.set_node(circle, 'id', id)

    if 1:  # rings
        svg.set_node(circle, 'fill', 'none')
        svg.set_node(circle, 'stroke-width', "2")
        svg.set_node(circle, 'stroke', color)
    return id, circle


def circleInflation(svg, x, y, r, color=None, fromR=0, toR=0, durS=5, begin=None):
    x, y, r = clip_float(x), clip_float(y), clip_float(r)
    fromR, toR = clip_float(fromR), clip_float(toR)

    id, circle = createCircle(svg, x, y, r, color)

    animateDict = {}
    # animateDict['xlink:href'] = f'#{id}'
    animateDict["{{{}}}".format(svg.xlink) + 'href'] = f'#{id}'
    animateDict['id'] = 'ani_' + id + '_' + rand_str(2)
    animateDict['fill'] = 'freeze'
    animateDict['attributeName'] = 'r'
    animateDict['from'] = str(fromR)  # '10'
    animateDict['to'] = str(toR)  # '50'
    animateDict['dur'] = str(durS)  # str(random.randint(0,durS)) #'5'
    animateDict['begin'] = begin or str(random.randint(0, 5)) + 's'  # '0s' #'click' #
    animateDict["repeatCount"] = "indefinite"  # "5"

    addNodeAnitmation(svg, circle, animateDict)
    return id, circle


def animCircleInflation(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    circleInflation(svg, cx, cy, r=10, fromR=10, toR=50, durS=3)


def animCircleInflation2(svg):
    H, W = svg.get_size()

    N = 30  # total points
    offset = 10  # margin to border
    pts = random_points((N, 2), min=offset, max=W - offset)
    # print(pts)

    color = None  # "black" #None
    for pt in pts:
        r = random.randint(1, 6)
        circleInflation(svg, pt[0], pt[1], r=r, color=color, fromR=r, toR=r * 5, durS=3)


def animCircleInflation3(svg):
    H, W = svg.get_size()

    blockSize = 20  # blocksize
    color = "black"  # None #
    r0 = blockSize / 2
    rList = np.linspace(1, r0 * 3 / 4, 20)
    for i in range(0, W, blockSize):
        for j in range(0, H, blockSize):
            x = i + r0
            y = j + r0
            r = random.choice(rList)
            circleInflation(svg, x, y, r=r, color=color, fromR=r, toR=r0 * 3 / 4, durS=random.randint(0, 10))


def animCircleInflation4(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 20  # total points
    r0 = 5
    r1 = 60

    color = "black"  # None #
    for i in range(N):
        begin = str(i) + 's'
        circleInflation(svg, cx, cy, r=r0, color=color, fromR=r0, toR=r1, durS=4, begin=begin)


def animCircleInflation5(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    N = 20  # total points
    r0 = 5
    r1 = 60

    offset = 10  # margin to border
    pts = random_points((N, 2), min=offset, max=W - offset)

    color = None  # "black"#
    rList = np.linspace(1, r1 / 2, 20)
    for i in range(N):
        begin = str(random.randint(1, 4)) + 's'  # str(i)+'s' #'0s'
        dur = random.randint(3, 6)
        r = random.choice(rList)
        id, circle = circleInflation(svg, pts[i][0], pts[i][1], r=r, color=color, fromR=r0, toR=r1, durS=dur, begin=begin)

        animateDict = {}
        animateDict["{{{}}}".format(svg.xlink) + 'href'] = f'#{id}'
        animateDict['id'] = 'ani_' + id + '_' + rand_str(2)
        animateDict['attributeName'] = 'stroke-width'
        animateDict['values'] = '0;2;4;2;1;0'
        animateDict['dur'] = '5s'  # str(random.randint(0,durS)) #'5'
        animateDict['begin'] = begin  # '0s'
        animateDict["repeatCount"] = "indefinite"  # "5"
        addNodeAnitmation(svg, circle, animateDict)


def drawNodeShape(svg, node):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    r = 45

    angle = np.pi / 5
    x0 = [cx, cx + 2 * r, cx + r]
    y0 = [cy, cy, cy - r * np.tan(angle)]
    # print('x0 ,y0=', x0 ,y0)

    times = 8
    theta = 0
    rainbowC = rainbow_colors(times)
    for i in range(times):
        theta = i * (2 * np.pi / times)
        x, y = rotation_pts_xy_point(x0, y0, (cx, cy), theta)
        color = random_color_hsv()
        # color = random_color()
        drawPloygonNode(svg, node=node, pts=[(x[0], y[0]), (x[1], y[1]), (x[2], y[2])], color=color)
        # drawPloygonNode(svg, node=node, pts=[(x[0],y[0]), (x[1],y[1]), (x[2],y[2])], color=rainbowC[i])

        # --------- draw text-------------- #
        dis = get_distance([x0[0], y0[0]], [x0[1], y0[1]])
        x_t = x0[0] + dis * 1.5 / 3
        y_t = y0[0] - (dis * 1.5 / 3) * np.tan(angle) * 0.6 / 2

        x_t = clip_float(x_t, 2)
        y_t = clip_float(y_t, 2)

        # print('x_t, y_t=', x_t, y_t)
        txt_child = svg.draw_node(node, draw_text(x_t, y_t, 'Love', color=reverse_hex(color)))

        strTmp = 'rotate({},{},{})'.format(i * 360 / times, x0[0], y0[0])
        svg.set_node(txt_child, 'transform', strTmp)
        svg.set_node(txt_child, 'text-anchor', 'middle')
        svg.set_node(txt_child, 'dominant-baseline', 'central')


def anim_Windmill(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')
    drawNodeShape(svg, g)

    animateTransDict = {}
    animateTransDict['attributeName'] = 'transform'
    animateTransDict['attributeType'] = 'xml'
    animateTransDict['type'] = 'rotate'
    animateTransDict['from'] = f'0 {cx} {cy}'
    animateTransDict['to'] = f'360 {cx} {cy}'
    animateTransDict['dur'] = '8s'
    animateTransDict["repeatCount"] = "indefinite"  # "5"

    addNodeAnitmation(svg, g, animateTransDict, elementName='animateTransform')


def drawAny(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2
    svg.set_title('you can draw anything by using draw_any()')

    g = svg.draw(draw_any('g', opacity=1.0))
    # anyNode = svg.draw_node(g, draw_any('test','222', a=10, b="4",c='red',xml='www.ss'))
    svg.draw_node(g, draw_any('test', 'hello'))

    anyDict = {}
    anyDict['test'] = 1
    anyDict['xml'] = 'www.ggg'
    anyDict['a'] = 'aaaaa anything else'
    anyDict['b'] = 'red black xxxxxxxxxxxxxxxxx anything you want'
    svg.draw_node(g, draw_any('test2', **anyDict))
    svg.draw_node(g, draw_any('hello', **anyDict))
    svg.draw_node(g, draw_any('anything', **anyDict))

    for i in range(20):
        anyDict = {}
        anyDict['cx'] = cx
        anyDict['cy'] = cy
        anyDict['r'] = '5'
        anyDict['stroke'] = '#80ff00'
        anyDict['stroke-width'] = '2'
        anyDict['fill'] = 'none'

        circle = svg.draw_node(g, draw_any('circle', **anyDict))
        # 'from' is a key word of python for import libs, but here last resort change parameter
        # from(attribute of animate element for svg) to 'From' to avoid conflict.
        svg.draw_node(circle, draw_any('animate', fill='freeze', attributeName='r', From="5", to="80", dur="4s", begin=str(i), repeatCount="indefinite"))

        anyDict = {}
        anyDict['fill'] = 'freeze'
        anyDict['attributeName'] = 'fill'
        anyDict['from'] = '#ff0000'
        anyDict['to'] = '#00ff40'
        anyDict['dur'] = '6s'
        anyDict['begin'] = '0s'
        anyDict['repeatCount'] = 'indefinite'
        # svg.draw_node(circle, draw_any('animate', **anyDict))

        anyDict['attributeName'] = 'stroke-width'
        anyDict['values'] = '1;2;3;2;1'
        anyDict.pop("from", None)
        anyDict.pop("to", None)
        svg.draw_node(circle, draw_any('animate', **anyDict))

        anyDict['attributeName'] = 'stroke'
        anyDict['from'] = '#80ff00'
        anyDict['to'] = '#0000ff'
        anyDict['begin'] = '1s'
        anyDict.pop("values", None)
        svg.draw_node(circle, draw_any('animate', **anyDict))


def draw_circle_path_anim(svg, node, path, radius, color='red', duration=None):
    circle = svg.draw_node(node, draw_circle(0, 0, radius=radius, color=color))

    animate_dict = {}

    if duration is None:
        animate_dict['dur'] = '5s'
    else:
        animate_dict['dur'] = f'{duration}s'
    animate_dict["repeatCount"] = "indefinite"
    animate_dict["path"] = path

    addNodeAnitmation(svg, circle, animate_dict, elementName='animateMotion')


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
    for i in range(N):
        rand_r = random.randint(2, r)
        rand_ver = random.randint(offset_y + rand_r, H - 2 * rand_r - offset_y)
        draw_moving_circle(svg, g, radius=rand_r, y=rand_ver,
                           offset_x=offset_x, duration=random.randint(3, 10),
                           color=random_color_hsv())


def get_points_path(pts, close=False):
    x = pts[0][0]
    y = pts[0][1]
    path = 'M %.1f %.1f L' % (x, y)
    for pt in pts[1:]:
        path = path + ' ' + str(pt[0]) + ' ' + str(pt[1])

    if close:
        path += ' Z'
    return path


def draw_ball_movin(svg, node, radius, W, H, start_pt, step_x, step_y, N=500, color=None, draw_path_line=False):
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
    draw_circle_path_anim(svg, node, path, radius, duration=len(coords)*2.8, color=color)


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
    draw_ball_movin(svg, g, r, W, H, start_pt=pt, step_x=-2, step_y=3, N=500, color=color, draw_path_line=True)


def anim8(svg):
    H, W = svg.get_size()
    cx, cy = W // 2, H // 2

    g = svg.draw(draw_tag('g'))
    svg.set_node(g, 'opacity', '1.0')
    pt = (cx, cy)
    for i in range(100):
        r = random.randint(2, 8)
        # pt = (random.randint(2+r, W-2-r), random.randint(2+r, H-2-r))
        sx = random.randint(1, 8) * [-1, 1][random.randrange(2)]
        sy = random.randint(1, 8) * [-1, 1][random.randrange(2)]
        # print('r, sx, sy=', r, sx, sy)
        draw_ball_movin(svg, g, r, W, H, start_pt=pt, step_x=sx, step_y=sy, N=800, color=random_color_hsv())


class BallCoordinates:
    """get coordinates of a bouncing ball in a rect[0, 0, W, H]
    """
    def __init__(self, x, y, vx, vy, width, height, offset=1, N=100):
        """init parameters

        Args:
            x (int): start point x value
            y (int): start point y value
            vx (int): moving speed in x-axis
            vy (int): moving speed in y-axis
            width (int): width of moving rect
            height (int): height of moving rect
            offset (int, optional): border offset, equal to ball's radius. Defaults to 1.
            N (int, optional): moving times. Defaults to 100.
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.offset = offset
        self.coordinates = []

        self.coordinates.append([x, y])
        self.generate(N=N)

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
        if(self.x < self.offset or self.x > self.width - self.offset):
            # Flip the horizontal velocity.
            self.vx = -1 * self.vx

            if (self.x < self.offset):  # if now negative, must be 2nd case
                self.x = self.offset
            else:
                self.x = self.width - self.offset

            self.coordinates.append([self.x, self.y])

        # Bounce off horizontal walls, if necessary.
        if (self.y < self.offset or self.y > self.height - self.offset):
            # Follow the same logic as above.
            self.vy = -1 * self.vy

            if(self.y < self.offset):
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
        if(self.x < 0 or self.x > self.width):
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

            if (self.x < 0):  # if now negative, must be 2nd case
                self.x = -1 * self.x
            else:
                self.x = (2 * self.width - self.x)

            # self.coordinates.append([self.x, self.y])

        # Bounce off horizontal walls, if necessary.
        if (self.y < 0 or self.y > self.height):
            # Follow the same logic as above.
            self.vy = -1 * self.vy

            if(self.y < 0):
                self.y = -1 * self.y
            else:
                self.y = (2 * self.height - self.y)

            # self.coordinates.append([self.x, self.y])
        self.coordinates.append([self.x, self.y])


def main():
    file = gImageOutputPath + r'\animation.svg'
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
    anim8(svg)


if __name__ == '__main__':
    main()
