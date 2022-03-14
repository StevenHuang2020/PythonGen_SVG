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
    """get line slope and bias from two points
    y = slope * x + bias
    """
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


def get_velocity_line(pt, vx, vy):
    """get line slope and bias from a start point and x, y change velocity,
    y = slope*x + bias
    """
    slope, bias = None, None
    if vx != 0:
        slope = vy / vx
        bias = pt[1] - slope * pt[0]
    return slope, bias


def get_velocity_line_abc(pt, vx, vy):
    """get line slope and bias from a start point and x, y change velocity,
    A*x + B*y + C = 0
    """
    return get_line_ABC(pt, (pt[0]+vx, pt[1]+vy))


def get_line_ABC(pt1, pt2):
    """get line parameters from two points
    A*x + B*y + C = 0, A=y1-y2, B=x2-x1, C=x1*y2-x2*y1
    """
    A = pt1[1] - pt2[1]
    B = pt2[0] - pt1[0]
    C = pt1[0] * pt2[1] - pt2[0] * pt1[1]
    return [A, B, C]


def get_line_ABC_inter(line1, line2):
    """get line intersection point,
    line1: A1*x + B1*y + C1 = 0, [A1, B1, C1]
    line2: A2*x + B2*y + C2 = 0, [A2, B2, C2]
    inter = B1*A2 - A1*B2
    x = (C1*B2-B1*C2)/inter, y=(A1*C2-A2*C1)/inter
    """
    inter = line1[1]*line2[0] - line1[0]*line2[1]
    if inter != 0:
        x = (line1[2]*line2[1]-line1[1]*line2[2])/inter
        y = (line1[0]*line2[2] - line2[0]*line1[2])/inter
        return (x, y)
    return None


def get_line_ABC_y(line, x):
    """line: a*x + b*y + c = 0, line=[a, b, c]"""
    a, b, c = line[0], line[1], line[2]
    if b == 0:
        return None
    return (-c - a * x) / b


def get_line_ABC_x(line, y):
    """line: a*x + b*y + c = 0, line=[a, b, c]"""
    a, b, c = line[0], line[1], line[2]
    if a == 0:
        return None
    return (-c - b * y) / a


def get_perpendicular_point_line_ABC(line, pt, reflect=False):
    """get foot point of the perpendicular from a point (x1,y1) to the line,
    line: A*x + B*y + C = 0, [A, B, C]
    tmp = -(A*x1+B*y1+c)/(A^2 + B^2)
    x = A*tmp + x1, y= B*tmp + y1
    """
    deno = line[0]**2 + line[1]**2  # denominator
    if deno != 0:
        tmp = -1*(line[0]*pt[0] + line[1]*pt[1] + line[2])/deno
        if reflect:
            tmp = tmp*2
        x = line[0]*tmp + pt[0]
        y = line[1]*tmp + pt[1]
        return (x, y)
    return None


def get_inter_pt(line):
    pass


def main():
    x = [1, 2]
    y = [3, 4]
    # print(get_line(x, y))
    print(get_distance(x, y))


if __name__ == '__main__':
    main()
