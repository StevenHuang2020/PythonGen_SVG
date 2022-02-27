# -*- encoding: utf-8 -*-
# Date: 27/Jan/2022
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: math functions
"""
import numpy as np


def get_distance(pt1, pt2):
    """get distance of two points"""
    return np.sqrt(np.power(pt1[0] - pt2[0], 2) + np.power(pt1[1] - pt2[1], 2))


def get_line(pt1, pt2):
    """get line slope and bias from two points"""
    slope, bias = None, None
    if pt1[0] != pt2[0]:
        slope = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
        bias = pt1[1] - slope * pt1[0]
    return slope, bias


def get_5star(R=10, r=3):
    """get five points star coordinates method, center(0,0)
    Outer points equation:{(R*cos(2πk/5+π/2),R*sin(2πk/5+π/2)) ∣ k=0,...,4}
    Inner points equation:{(r*cos(2πk/5+π/2+π/5),r*sin(2πk/5+π/2+π/5)) ∣ k=0,...,4}
    """
    # points = [[R*np.cos(i * 2 * np.pi / 5 + np.pi/2), R*np.sin(i*2*np.pi/5+np.pi/2)] for i in range(5)]

    points = []
    for i in range(5):
        """ add or sub π/2 to adjust start point """
        points.append([R*np.cos(i * 2 * np.pi / 5 - np.pi/2), R*np.sin(i*2*np.pi/5-np.pi/2)])
        points.append([r*np.cos(i*2*np.pi/5-np.pi/2+np.pi/5), r*np.sin(i*2*np.pi/5-np.pi/2+np.pi/5)])

    return np.asarray(points)


def get_regular_ngons(R=10, N=3, offset_angle=0):
    points = []
    for i in range(N):
        """ add or sub π/2 to adjust start point """
        theta = i * 2 * np.pi / N + offset_angle  # - np.pi/2
        points.append([R * np.cos(theta), R * np.sin(theta)])
    return np.asarray(points)


def points_on_triangle(v, n):
    """
    Give n random points uniformly on a triangle.

    The vertices of the triangle are given by the shape
    (2, 3) array *v*: one vertex per row.
    """
    x = np.sort(np.random.rand(2, n), axis=0)
    x = np.column_stack([x[0], x[1]-x[0], 1.0-x[1]])
    return np.dot(x, v)


def main():
    x = [1, 2]
    y = [3, 4]
    # print(get_line(x, y))
    print(get_distance(x, y))


if __name__ == '__main__':
    main()
