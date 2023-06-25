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
    return res[0].flatten(), res[1].flatten()


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
    res = np.stack(([x, y])) + matrix
    return res[0], res[1]


def translation_matrix(x, y, to_pt):
    """translation matrix, for moving shape.
    Deprecated, use translation_pts_xy instead.
    """

    a = np.stack(([x, y]))
    one = np.array([[to_pt[0]], [to_pt[1]]])

    M = one
    for _ in range(a.shape[1] - 1):
        M = np.concatenate((M, one), axis=1)

    res = a + M
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


def rotation_pts_xy_point(x, y, rot_point, theta):
    """rotation with a point"""
    trans_pt = (-1 * rot_point[0], -1 * rot_point[1])
    x, y = translation_pts_xy(x, y, trans_pt)  # move to (0,0)
    x, y = rotation_pts_xy(x, y, theta)  # rotation

    trans_pt = (rot_point[0], rot_point[1])
    return translation_pts_xy(x, y, trans_pt)  # move to rot_point


def zoom_pts(points, z=1.0):
    """ Uniform zoom points with (0, 0)"""
    x, y = split_points(points)
    x, y = zoom_pts_xy(x, y, z)
    return combine_xy(x, y)


def zoom_pts_point(points, point, z=1.0):
    """ Uniform zoom points with point"""
    x, y = split_points(points)
    x, y = zoom_pts_xy_point(x, y, point, z)
    return combine_xy(x, y)


def zoom_pts_xy(x, y, z=1.0):
    """Uniform zoom or scaling points with (0,0), x' = x*z; y' = y*z """
    # return x * z, y * z  #method 1
    return zoom_non_pts_xy(x, y, z1=z, z2=z)


def zoom_non_pts_xy(x, y, z1=1, z2=1):
    """Nonuniform zoom or scaling points with (0,0), x' = x*z1; y' = y*z2 """
    a = np.stack(([x, y]))
    matrix = np.array([[z1, 0], [0, z2]])
    return transform(a, matrix)


def zoom_pts_xy_point(x, y, zoo_point, z=2):
    """ zoom or scaling points with a point"""
    trans_pt = (-1 * zoo_point[0], -1 * zoo_point[1])
    x, y = translation_pts_xy(x, y, trans_pt)  # move to (0,0)
    x, y = zoom_pts_xy(x, y, z=z)  # zoom

    trans_pt = (zoo_point[0], zoo_point[1])
    return translation_pts_xy(x, y, trans_pt)  # move to zoo_point


def identity_trans(x, y):
    """ identity transform:  x' = x; y' = y
    """
    matrix = np.array([[1, 0],
                       [0, 1]])
    a = np.stack(([x, y]))
    return transform(a, matrix)


def shear_points(points, r=0.5, shear_x=True):
    """ shear transform:
    shear by x axis: x' = x + r * y; y' = y
    shear by y axis: x' = x; y' = r * x + y
    """
    matrix = np.array([[1, 0], [r, 1]])
    if shear_x:
        matrix = np.array([[1, r], [0, 1]])

    return transform_any_points(points, matrix)


def reflection_points(points, reflect_x=True):
    """ reflection transform:
    reflection by x axis: x' = -1 * x; y' = y
    reflection by y axis: x' = x; y' = -1*y
    """

    matrix = np.array([[1, 0], [0, -1]])
    if reflect_x:
        matrix = np.array([[-1, 0], [0, 1]])

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
    return transform(np.stack(([x, y])), matrix)


def center_cordinates(points, center):
    """ align points to a center point

    Args:
        points ([np.ndarray]): [points need to adjust, shape (N, 2)]
        center ([tuple or array]): [center point]

    Returns:
        [np.ndarray]: [aligned points]
    """

    points += (center - center_of_cordinates(points))
    return points


def center_of_cordinates(points):
    """ get center of points """
    x_min, x_max, y_min, y_max = bounding_cordinates(points)
    return np.array([(x_max + x_min) / 2, (y_max + y_min) / 2])


def bounding_cordinates(points):
    """ calculate points' bounding cordinates

    Args:
        points (np.array): (N, 2)
    """
    x, y = np.hsplit(points, 2)
    return np.amin(x), np.amax(x), np.amin(y), np.amax(y)


def main():
    """ translation examples """
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
