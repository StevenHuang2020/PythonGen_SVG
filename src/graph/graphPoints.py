#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Graph structure
# Date: 09/Dec/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License
"""
Description: For connecting random points
"""

import random
from itertools import combinations  # permutations
import numpy as np

__all__ = ['VertexPt', 'GraphPoints']


class VertexPt():
    """ vertex point """

    def __init__(self, vetex_id, point):
        self.point = point
        self.vetex_id = vetex_id
        self.distance = 0
        self.shortest_matrix = None

    def set_distance(self, distance):
        """ set weight """
        self.distance = distance

    def __str__(self):
        return 'Vertex: id=' + str(self.vetex_id) + ' point=' + str(self.point)

    def getDistanceVectorIds(self, K=2):
        """ get weight id """
        if K <= 0:
            K = len(self.distance)
            # print('all K=', K)
        # top_k_idx = self.distance.argsort()[::-1][0:K+1]
        # start from 1,skip self index
        return self.distance.argsort()[1:K + 1]


class GraphPoints():
    """ graph vertics """

    def __init__(self, points):
        self.vertex_list = []
        for i, pt in enumerate(points):
            self.vertex_list.append(VertexPt(i, pt))

        self.pt_matrix = None
        for _, ver in enumerate(self.vertex_list):
            v = self.getVertextPoint(ver)
            self.pt_matrix = np.concatenate(
                (self.pt_matrix, v), axis=1) if self.pt_matrix is not None else v

        # print('self.pt_matrix=',self.pt_matrix)
        for v in self.vertex_list:
            pt = self.getVertextPoint(v)

            # res = np.asarray(pt - self.pt_matrix)
            # print('res=',res.shape,res)
            # print('res**2=',res**2)

            # print('sum1 res**2=',np.sum(res**2, axis=1))
            # print('sum0 res**2=',np.sum(res**2, axis=0))
            distances = np.sqrt(
                np.sum(np.asarray(pt - self.pt_matrix) ** 2, axis=0))
            # print('distances=',len(distances),distances)
            v.set_distance(distances)
        self.shortest_matrix = None

    def getVertexNearstPtIndex(self, K=8):
        """ get nearst matrxi """
        # K = K if K < len(self.vertex_list) else len(self.vertex_list)

        ys = None
        for v in self.vertex_list:
            low_k_idx = v.getDistanceVectorIds(K)
            # print('low_k_idx=',low_k_idx)
            ys = np.vstack([ys, low_k_idx]) if ys is not None else low_k_idx

        # print('ys=',ys)
        self.shortest_matrix = ys
        return self.shortest_matrix

    def getVertextPoint(self, vertex):
        """ get point """
        # pt = self.vertex_list[index].point
        pt = vertex.point
        return np.array([[pt[0]], [pt[1]]])

    def show(self):
        """ print """
        for i in self.vertex_list:
            print(i)

    def getConnectionMatrix(self, K=2, k_nearst=4):
        """ get connection matrix """
        def removeItem(con_m, i):
            if con_m is not None:
                for con in con_m:
                    if con[1] == i:
                        yield con[0]

        self.getVertexNearstPtIndex(K=k_nearst)
        con_matrix = None
        for i, _ in enumerate(self.vertex_list):
            shortest = list(self.shortest_matrix[i])
            # print('---------')
            # print('cur con_matrix:',con_matrix)
            # print('---------')

            # print('start:',i,shortest)
            for v_index in removeItem(con_matrix, i):
                # v_index =  removeItem(con_matrix,i)
                # print('remove:',i,shortest,v_index)
                if v_index is not None and v_index in shortest:
                    shortest.remove(v_index)

            # print('after remove:',i,shortest)
            if len(shortest) == 0:
                con = np.array([[i, -1]])
            else:
                N = len(shortest) if K > len(shortest) else K
                # print('start to choice:',i,shortest)
                for s in random.sample(shortest, N):
                    con = np.array([[i, s]])
                    con_matrix = np.concatenate(
                        (con_matrix, con)) if con_matrix is not None else con
        # print('con_matrix=',con_matrix)
        return con_matrix

    def getAllConnectionMatrix(self):
        """ get all connection matrix """
        size = len(self.vertex_list)
        return np.array(list(combinations(range(size), 2)))

    def getConnectionMatrix2(self, k_nearst=4):
        """ get connextion matrix2 """
        con_all_matrix = self.getAllConnectionMatrix()
        # print('con_all_matrix=',con_all_matrix)

        con_matrix = None
        self.getVertexNearstPtIndex(K=k_nearst)
        for con in con_all_matrix:  # filter nearst points to connect
            index = con[0]
            con_id = con[1]
            shortest = list(self.shortest_matrix[index])
            # print('start:',index, shortest)
            if con_id in shortest:
                connect = np.array([[index, con_id]])
                con_matrix = np.concatenate(
                    (con_matrix, connect)) if con_matrix is not None else connect

        return con_matrix


def main():
    """ main function """
    points = []
    points.append((1, 2))
    points.append((3, 4))
    points.append((5, 6))
    points.append((7, 6))
    points.append((9, 8))
    points.append((9, 5))

    graph = GraphPoints(points)
    graph.show()

    mat = graph.getConnectionMatrix2(k_nearst=4)
    print('mat=', mat)


if __name__ == '__main__':
    main()
