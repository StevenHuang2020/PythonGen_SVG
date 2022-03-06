"""
#python3 Steven Scalable Vector Graphics(SVG)
#reference: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
#SVG: https://www.w3.org/Graphics/SVG/
#svg elements: https://developer.mozilla.org/en-US/docs/Web/SVG/Element

"""
import svg.basic as sb
from svg.basic import draw_line, random_color
from svg.file import SVGFileV2
from svgDrawArt import drawArtSvg
from common import gImageOutputPath


def draw_first(svg):
    H, W = svg.get_size()
    svg.draw(draw_line(0, 0, W, H))


def draw_basic_shapes(svg):
    svg.draw(sb.draw_rect(x=3, y=3, width=20, height=20, stroke_width=1,
                          color='transparent', stroke_color='black'))
    rt = svg.draw(sb.draw_rect(x=28, y=3, width=20, height=20, stroke_width=1,
                               color='transparent', stroke_color='red'))

    svg.set_node(rt, 'rx', '2')
    svg.set_node(rt, 'ry', '2')
    svg.draw(sb.draw_circle(x=60, y=13, radius=10, color='green'))
    svg.draw(sb.draw_ring(x=85, y=13, radius=8, stroke_color='red', stroke_width=3))
    svg.draw(sb.draw_ellipse(cx=25, cy=35, rx=20, ry=8))
    svg.draw(sb.draw_line(x=50, y=30, x2=90, y2=45, stroke_width=1, color='#23ff67'))

    points = '8 50 18 70 28 50 38 70 48 50 58 70 68 50 78 70 88 50 98 70'
    svg.draw(sb.draw_polyline(points, stroke_width=0.5, stroke_color=random_color()))

    points = '8 75 25 75 30 95 5 95'
    svg.draw(sb.draw_polygon(points, stroke_width=0.5, stroke_color=random_color()))

    path = 'M 35 90 Q 55 60 98 90'
    svg.draw(sb.draw_path(path, stroke_width=0.2, color=random_color()))


def main():
    file = gImageOutputPath + r'\test.svg'
    H, W = 100, 100
    svg = SVGFileV2(file, W, H, border=True)
    # drawArtSvg()
    # draw_first(svg)
    draw_basic_shapes(svg)


if __name__ == '__main__':
    main()
