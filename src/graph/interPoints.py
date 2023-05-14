#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Get the intersection of two line segment
# Date: 09/Dec/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License


class GetLineSegInterPoint():
    def __init__(self, line1, line2):
        self.line1 = line1
        self.line2 = line2
        self.interPoint = self.calculate_cross_point(line1, line2)

    def get_inter(self):
        return self.interPoint

    def inSegment(self, p, line1, line2):
        """"check the cross point is on line segment """

        if p[0] >= min(line1[0][0], line1[1][0]) and p[0] <= max(line1[0][0], line1[1][0]):
            if p[0] >= min(line2[0][0], line2[1][0]) and p[0] <= max(line2[0][0], line2[1][0]):
                if p[1] >= min(line1[0][1], line1[1][1]) and p[1] <= max(line1[0][1], line1[1][1]):
                    if p[1] >= min(line2[0][1], line2[1][1]) and p[1] <= max(line2[0][1], line2[1][1]):
                        return True
        return False

    def calculate_cross_point(self, line1, line2):
        """line[0]: line start point, line[1]: stop point"""
        def getLinePara(line):
            a = line[0][1] - line[1][1]
            b = line[1][0] - line[0][0]
            c = line[0][0] * line[1][1] - line[1][0] * line[0][1]
            return a, b, c

        a1, b1, c1 = getLinePara(line1)
        a2, b2, c2 = getLinePara(line2)
        d = a1 * b2 - a2 * b1
        p = [0, 0]
        if d == 0:  # parallel
            return None

        # p[0] = round((b1 * c2 - b2 * c1) * 1.0 / d, 2)
        # p[1] = round((c1 * a2 - c2 * a1) * 1.0 / d, 2)
        p[0] = (b1 * c2 - b2 * c1) * 1.0 / d
        p[1] = (c1 * a2 - c2 * a1) * 1.0 / d
        # p = tuple(p)
        if self.inSegment(p, line1, line2):
            return p
        return None


def main():
    line1 = [[0, 0], [1, 0]]
    line2 = [[0.5, 1], [0.5, -1.5]]

    p = GetLineSegInterPoint(line1, line2).get_inter()
    print('p=', p)


if __name__ == '__main__':
    main()
