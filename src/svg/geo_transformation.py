# -*- encoding: utf-8 -*-
# Date: 27/Jan/2022
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Geometry transformaion operation for coordiantes
Used to translate, rotate, and zoom coordinates.
Basic 2D Transformations:
Reference: https://en.wikipedia.org/wiki/Transformation_matrix
1.Translation
2.Rotation
3.Uniform scaling/Nonuniform scaling
4.Shear
5.Reflection
6.Affine
7.Identity
"""

import numpy as np


def split_points(points):
    """split points coordinates to x and y

    Args:
        points (np.array): shape (N,2) array

    Returns:
        tuple: x, y
    """
    res = np.hsplit(points, 2)
    x, y = res[0].flatten(), res[1].flatten()
    return x, y


def combine_xy(x, y):
    """combine x and y to points

    Args:
        x (np.array): shape (N, ) array
        y (np.array): shape (N, ) array

    Returns:
        np.array: shape(N, 2)
    """
    x = x.reshape((x.shape[0], 1))
    y = y.reshape((y.shape[0], 1))
    return np.hstack(([x, y]))


def translation_pts(points, to_pt, combine=False):
    """translation points matrix to a target point

    Args:
        points (np.array): shape (N,2) array, 2d points coordinate
        to_pt (np.array or tuple): target point

    Returns:
        tuple: (dst_x, dst_y) or points array when combine is True
    """

    x, y = split_points(points)
    x, y = translation_pts_xy(x, y, to_pt)
    if combine:
        return combine_xy(x, y)
    return x, y


def translation_pts_xy(x, y, to_pt):
    """translation points (x,y) to a target point

    Args:
        x (np.array): x, shape(N,)
        y (np.array): y, shape(N,)
        to_pt (np.array or tuple): target point

    Returns:
        tuple: dst_x, dst_y
    """
    matrix = np.array([[to_pt[0]], [to_pt[1]]])
    a = np.stack(([x, y]))
    res = a + matrix
    return res[0], res[1]


def translation_matrix(x, y, to_pt):
    """translation matrix, for moving shape.
    Deprecated, use translation_pts_xy instead.
    """

    a = np.stack(([x, y]))
    one = np.array([[to_pt[0]], [to_pt[1]]])
    # one = np.array([to_pt[0], to_pt[1]]).T.reshape((2,1))

    # print('a.shape=', a.shape, a, one)
    M = one
    for _ in range(a.shape[1] - 1):
        M = np.concatenate((M, one), axis=1)

    res = a + M
    # print('a=',a)
    # print('M=',M)
    # print('res=',res)
    return res[0][:], res[1][:]


def transform(a, matrix):
    """array dot transform

    Args:
        a (np.array): array
        matrix (np.array): transform matrix
    Returns:
        tuple: dst_x, dst_y
    """
    res = np.dot(matrix, a)
    return res[0], res[1]


def rotation_pts_xy(x, y, theta):
    """ rotation points with (0,0),
    x' = x*cos(theta)-y*sin(theta), y' = x*sin(theta)+y*cos(theta) """
    a = np.stack(([x, y]))
    c, s = np.cos(theta), np.sin(theta)
    matrix = np.array([[c, -s], [s, c]])
    return transform(a, matrix)


def rotation_pts_xy_point(x, y, rotPoint, theta):
    """rotation with a point"""
    transPt = (-1 * rotPoint[0], -1 * rotPoint[1])
    x, y = translation_pts_xy(x, y, transPt)  # move to (0,0)
    x, y = rotation_pts_xy(x, y, theta)  # rotation

    transPt = (rotPoint[0], rotPoint[1])
    return translation_pts_xy(x, y, transPt)  # move to rotPoint


def zoom_pts_xy(x, y, z=2):
    """Uniform zoom or scaling points with (0,0), x' = x*z; y' = y*z """
    # return x * z, y * z  #method 1
    return zoom_non_pts_xy(x, y, z1=z, z2=z)


def zoom_non_pts_xy(x, y, z1=1, z2=1):
    """Nonuniform zoom or scaling points with (0,0), x' = x*z1; y' = y*z2 """
    a = np.stack(([x, y]))
    matrix = np.array([[z1, 0], [0, z2]])
    return transform(a, matrix)


def zoom_pts_xy_point(x, y, zooPoint, z=2):
    """ zoom or scaling points with a point"""
    transPt = (-1 * zooPoint[0], -1 * zooPoint[1])
    x, y = translation_pts_xy(x, y, transPt)  # move to (0,0)
    x, y = zoom_pts_xy(x, y, z=z)  # zoom

    transPt = (zooPoint[0], zooPoint[1])
    return translation_pts_xy(x, y, transPt)  # move to zooPoint


def identity_trans(x, y):
    """ identity transform:  x' = x; y' = y
    """
    matrix = np.array([[1, 0],
                       [0, 1]])
    a = np.stack(([x, y]))
    return transform(a, matrix)


def shear_points(points, r=0.5, shearx=True):
    """ shear transform:
    shear by x axis: x' = x + r * y; y' = y
    shear by y axis: x' = x; y' = r * x + y
    """

    if shearx:
        matrix = np.array([[1, r], [0, 1]])
    else:
        matrix = np.array([[1, 0], [r, 1]])

    return transform_any_points(points, matrix)


def reflection_points(points, reflectx=True):
    """ reflection transform:
    reflection by x axis: x' = -1 * x; y' = y
    reflection by y axis: x' = x; y' = -1*y
    """

    if reflectx:
        matrix = np.array([[-1, 0], [0, 1]])
    else:
        matrix = np.array([[1, 0], [0, -1]])

    return transform_any_points(points, matrix)


def transform_any_points(points, matrix):
    """any transform

    Args:
        points (np.array): shape (N,2) array, 2d points coordinate
        matrix (np.array): matrix(2,2)

    Returns:
        tuple: dst_x, dst_y
    """

    x, y = split_points(points)
    a = np.stack(([x, y]))
    return transform(a, matrix)


def center_cordinates(points, center):
    """align points  to a center point

    Args:
        points ([np.ndarray]): [points need to adjust, shape (N, 2)]
        center ([tuple or array]): [center point]

    Returns:
        [np.ndarray]: [aligned points]
    """

    cx, cy = center[0], center[1]

    s = np.hsplit(points, 2)
    x, y = s[0], s[1]

    x_min, x_max = np.amin(x), np.amax(x)
    y_min, y_max = np.amin(y), np.amax(y)
    # print('x_min, x_max=', x_min, x_max)
    delta_x = cx - (x_max + x_min) / 2
    delta_y = cy - (y_max + y_min) / 2
    x = x + delta_x
    y = y + delta_y

    return np.concatenate((x, y), axis=1).astype(int)


def main():
    """translation examples """
    x = np.array([1, 2, 5])
    y = np.array([3, 4, 6])

    # translation_pts_xy(x, y, (-1.5,-3.5))
    new_x, new_y = translation_pts_xy(x, y, (1, 2))
    print('new_x, new_y=', new_x, new_y)

    points = np.array([[1, 2],
                       [3, 4],
                       [5, 6]])  # (N,2)
    new_x, new_y = translation_pts(points, (1, 2))
    print('new_x, new_y=', new_x, new_y)


if __name__ == '__main__':
    main()
