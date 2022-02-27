import os
import cv2
import potrace  # pip install potracer
import numpy as np
from svg.file import SVGFileV2
from svg.basic import random_color, color_fader, draw_circle, draw_rect, random_color_hsv
from svg.basic import convert_rgb, draw_any, clip_float, draw_path
from svg.basic import draw_only_path, add_style, get_styles
from svg.geo_transformation import translation_pts, translation_pts_xy
from svg.geo_transformation import zoom_pts_xy, split_points, combine_xy, zoom_non_pts_xy
from svgSmile import drawSmileSVG
from common import gImageOutputPath


def getImgHW(img):
    return img.shape[0], img.shape[1]


def changeBgr2Rbg(img):  # input color img
    if getImagChannel(img) == 3:
        b, g, r = cv2.split(img)       # get b,g,r
        img = cv2.merge([r, g, b])
    return img


def loadImg(file, mode=cv2.IMREAD_COLOR):
    # mode = cv2.IMREAD_COLOR cv2.IMREAD_GRAYSCALE cv2.IMREAD_UNCHANGED
    try:
        img = cv2.imread(file, mode)
    except BaseException:
        print("Load image error,file=", file)

    if getImagChannel(img) == 3:
        img = changeBgr2Rbg(img)
    return img


def getImagChannel(img):
    if img.ndim == 3:  # color r g b channel
        return 3
    return 1  # only one channel


def blur_img(img, size=(5, 5)):
    return cv2.GaussianBlur(img, size, 0)


def OtsuMethodThresHold(img):
    _, threshold = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold


def showimage(img, str='image', autoSize=False):
    flag = cv2.WINDOW_NORMAL
    if autoSize:
        flag = cv2.WINDOW_AUTOSIZE

    cv2.namedWindow(str, flag)
    cv2.imshow(str, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


class SVGImageMask:
    def __init__(self, imageFile, dstSvgfile, step=1):
        # cv2.IMREAD_GRAYSCALE
        self.image = loadImg(imageFile, cv2.IMREAD_COLOR)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.step = step
        self.svgH = int((self.height // step) * step)
        self.svgW = int((self.width // step) * step)
        self.svg = SVGFileV2(dstSvgfile, W=self.svgW, H=self.svgH)
        print('step=', step, 'image H,W=', self.height,
              self.width, 'SVG H,W=', self.svgH, self.svgW)

    def drawStep(self):
        r = self.step / 2
        for i in range(0, self.svgH, self.step):
            for j in range(0, self.svgW, self.step):
                x = i + 1 / 2 * self.step
                y = j + 1 / 2 * self.step

                roi = self.image[i:i + self.step, j:j + self.step]
                # print(i,j,self.svgH,self.svgW,i+self.step,j+self.step)
                color = color_fader(mix=np.mean(roi)/255)
                if 0:
                    self.svg.draw(draw_circle(y, x, r, color=color))
                else:
                    self.svg.draw(
                        draw_rect(y, x, self.step, self.step, color=color))

    def get_coordinates_color(self):
        coords = []
        colors = []
        for i in range(0, self.svgH, self.step):
            for j in range(0, self.svgW, self.step):
                y = i + 1 / 2 * self.step
                x = j + 1 / 2 * self.step

                c = self.image[i:i + self.step, j:j + self.step, :]
                # print('c, c.shape=', c, c.shape)

                c = np.mean(c, axis=0)
                c = np.mean(c, axis=0)
                c = convert_rgb(c)
                # print('c=', c)
                coords.append([x, y])
                colors.append(c)
                # break
            # break
        return np.array(coords), np.array(colors)

    def drawColor(self):
        r = 1
        for i in range(0, self.svgH, self.step):
            for j in range(0, self.svgW, self.step):
                color = convert_rgb(self.image[i, j, :])
                self.svg.draw(
                    draw_rect(j, i, r, r, stroke_width=0, color=color))


def maskImage():
    f = r'.\res\trumps.jpg'
    d = gImageOutputPath + r'\trump.svg'
    svg = SVGImageMask(f, d, step=1)  # 4, 8
    svg.drawStep()


def maskColorImg():
    f = r'.\res\trumps.jpg'
    d = gImageOutputPath + r'\trumpX.svg'
    # SVGImageMask(f,d).drawStep()
    svg = SVGImageMask(f, d)
    svg.drawColor()

    drawSmileSVG(svg.svg, ridus=10, offsetX=10, offsetY=20)  # draw a smile


def imgSvgElement():
    file = gImageOutputPath + r'\image.svg'
    svg = SVGFileV2(file, W=200, H=200, border=False)
    W, H = svg.get_size()

    styleDict = {}
    styleDict['x'] = '0'
    styleDict['y'] = '0'  # 'green'
    styleDict['width'] = 100
    styleDict['height'] = 100
    # styleDict['href'] = 'https://www.python.org/static/img/python-logo@2x.png'
    styleDict['href'] = r'../images/download.png'
    # styleDict['preserveAspectRatio'] = 'none'
    # styleDict['crossorigin'] = ''
    svg.draw(draw_any('image ', **styleDict))
    styleDict['x'] = '20'
    styleDict['y'] = '20'  # 'green'
    svg.draw(draw_any('image ', **styleDict))


def image2_svg():
    def drawPointsCircle_colors(svg, pts, r, colors):
        for i, pt in enumerate(pts):
            x = clip_float(pt[0])
            y = clip_float(pt[1])
            svg.draw(draw_circle(x, y, radius=r, color=colors[i]))

    def drawPointsRect_colors(svg, pts, r, colors):
        for i, pt in enumerate(pts):
            x = clip_float(pt[0])
            y = clip_float(pt[1])
            svg.draw(draw_rect(x, y, r, r, color=colors[i]))

    f = r'.\res\trumps.jpg'
    d = gImageOutputPath + r'\trump.svg'
    step = 1
    mask = SVGImageMask(f, d, step=step)  # 4, 8
    coords, colors = mask.get_coordinates_color()
    print('coords, coords.shape', coords, coords.shape)
    print('colors, colors.shape', colors, colors.shape)

    # drawPointsCircle_colors(mask.svg, coords, r=step/2, colors=colors)
    drawPointsRect_colors(mask.svg, coords, r=step, colors=colors)


def my_path_potrace(paths, N=2):
    # print('len(path)=', len(paths))

    # Iterate over path curves
    for curve in paths:
        start_pt = curve.start_point
        # pts = curve.decomposition_points
        # print('pts=', pts)
        path = 'M %f %f ' % (clip_float(start_pt.x, N),
                             clip_float(start_pt.y, N))
        # print("start_point =", start_pt)

        for segment in curve:
            # print('end_pt=', end_pt, segment.is_corner)
            if segment.is_corner:
                c = segment.c
                # print('c=', c, 'x=', c.x, 'y=', c.y)

                end_pt = segment.end_point
                end = f'L {clip_float(end_pt.x, N)} {clip_float(end_pt.y, N)}'
                seg = f'L {clip_float(c.x, N)} {clip_float(c.y, N)} ' + end
            else:
                c1 = segment.c1
                c2 = segment.c2
                # print('c1=', c1, 'x=', c1.x, 'y=', c1.y)
                # print('c2=', c2, 'x=', c2.x, 'y=', c2.y)
                end_pt = segment.end_point
                end = f'{clip_float(end_pt.x, N)} {clip_float(end_pt.y, N)}'
                seg = f'C {clip_float(c1.x, N)},{clip_float(c1.y, N)} {clip_float(c2.x, N)},{clip_float(c2.y, N)} ' + end
            path += seg

        path += 'z'
        yield path


def get_potrace_path(data):
    """get path from raster image data

    Args:
        data (array): M*N array, white and black image
    """

    # Create a bitmap from the array
    bmp = potrace.Bitmap(data)
    # Trace the bitmap to a path
    path = bmp.trace()
    return path


def transform_points(de_points, zoom_x=0.5, zoom_y=0.5, to_point=(0, 0)):
    de_points = [[i.x, i.y] for i in de_points]
    de_points = np.asarray(de_points)
    # print('de_points=', de_points, de_points.shape)

    # start to translate
    x, y = split_points(de_points)
    # x, y = zoom_pts_xy(x, y, zoom)
    x, y = zoom_non_pts_xy(x, y, zoom_x, zoom_y)
    x, y = translation_pts_xy(x, y, to_point)
    return combine_xy(x, y)


def path_potrace_jagged(path):
    parts = []
    for curve in path:
        parts.append("M")

        points = curve.decomposition_points
        # print('points=',  points, len(points))
        for point in points:
            parts.append(" %f,%f" % (point.x, point.y))

        parts.append("z")
    return "".join(parts)


def path_potrace_jagged_trans(path, zoom_x, zoom_y, to_point):
    parts = []
    for curve in path:
        parts.append("M")

        points = curve.decomposition_points
        # print('points=',  points, len(points))
        points = transform_points(points, zoom_x, zoom_y, to_point)
        # print('points, pts.shape=', points, points.shape)
        for point in points:
            parts.append(" %f,%f" % (point[0], point[1]))

        parts.append("z")
    return "".join(parts)


def path_potrace(path):
    # print('len(path)=', len(path))
    parts = []
    for curve in path:
        fs = curve.start_point
        parts.append("M%f,%f" % (fs.x, fs.y))
        for segment in curve.segments:
            if segment.is_corner:
                a = segment.c
                parts.append("L%f,%f" % (a.x, a.y))
                b = segment.end_point
                parts.append("L%f,%f" % (b.x, b.y))
            else:
                a = segment.c1
                b = segment.c2
                c = segment.end_point
                parts.append("C%f,%f %f,%f %f,%f" %
                             (a.x, a.y, b.x, b.y, c.x, c.y))
        parts.append("z")

    return "".join(parts)


def get_binary_image(file, show=False, binary=True):
    image = loadImg(file, cv2.IMREAD_GRAYSCALE)
    if binary:
        image = blur_img(image)
        image = OtsuMethodThresHold(image)  # binary to white and black
        # print('image=', image, image.shape, np.unique(image))

    if show:
        showimage(image)
    return image


def image_svg_path(file, dst_file):
    """convert raster image to svg by using path element
    """
    image = get_binary_image(file)
    svg = SVGFileV2(dst_file, W=image.shape[1], H=image.shape[0], border=True)

    paths = get_potrace_path(image)
    # path = path_potrace(paths)
    path = path_potrace_jagged(paths)
    print('len(path)=', len(path))
    fill_color = random_color_hsv()  # 'black'
    svg.draw(draw_path(path, stroke_width=1.8, color='none',
             fill_color=fill_color, fill_rule='evenodd'))


def image_svg_path2(file, dst_file):
    """convert raster image to svg by using path element
    """
    image = get_binary_image(file)
    W = image.shape[1]
    H = image.shape[0]
    svg = SVGFileV2(dst_file, W=W, H=H, border=True)

    paths = get_potrace_path(image)
    N = 4
    zoom = 1/N

    for i in range(N):
        for j in range(N):
            to_point = (i * W / N, j * H / N)
            path = path_potrace_jagged_trans(
                paths, zoom_x=zoom, zoom_y=zoom, to_point=to_point)
            fill_color = random_color()
            svg.draw(draw_path(path, color='none',
                     fill_color=fill_color, fill_rule='evenodd'))


def image_svg_path3(file, dst_file):
    """potrace to multi <path/> elements
    """
    image = get_binary_image(file)
    svg = SVGFileV2(dst_file, W=image.shape[1], H=image.shape[0], border=False)

    paths = get_potrace_path(image)
    if 0:
        for i, path in enumerate(my_path_potrace(paths)):
            print(f'[{i}]', 'path=', path)
            svg.draw(draw_path(path, stroke_width=1.8, color='None',
                               fill_color='#000000', fill_rule='evenodd'))
    else:
        styleDict = {}
        styleDict['stroke_width'] = '1.8'
        styleDict['color'] = 'None'
        styleDict['fill_color'] = '#000000'
        styleDict['fill_rule'] = 'evenodd'
        svg.draw(add_style('path', get_styles(styleDict)))

        for i, path in enumerate(my_path_potrace(paths)):
            svg.draw(draw_only_path(path))


def main():
    # maskImage()
    # maskColorImg()
    # imgSvgElement()
    # image2_svg()

    file = r'.\res\Lenna.png'  # r'.\res\f.png'
    dst_file = os.path.join(gImageOutputPath, 'image_path3.svg')
    # image_svg_path(file, dst_file)
    # image_svg_path2(file, dst_file)
    image_svg_path3(file, dst_file)


if __name__ == '__main__':
    main()
