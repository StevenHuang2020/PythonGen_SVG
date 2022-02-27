#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Graph structure
# Date: 09/Dec/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License


class Graph:
    def __init__(self, gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict

    def getVertices(self):  # Get the keys of the dictionary
        return list(self.gdict.keys())

    def edges(self):
        return self.findedges()

    def findedges(self):  # Find the distinct list of edges
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename

    def addVertex(self, vrtx):  # Add the vertex as a key
        if vrtx not in self.gdict:
            self.gdict[vrtx] = []

    def addEdge(self, edge):  # Add the new edge
        (vrtx1, vrtx2) = tuple(set(edge))
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]


class GraphW(Graph):
    # weighted graph
    def __init__(self, gdict=None):
        # graph.__init__(self,gdict)
        super().__init__(gdict)

    def findedges(self):  # Find the distinct list of edges
        edgename = {}
        print('dict=', self.gdict)
        for vrtx in self.gdict:
            for nxtvrtx, weight in self.gdict[vrtx].items():
                if (vrtx, nxtvrtx) not in edgename and \
                        (nxtvrtx, vrtx) not in edgename:
                    edgename[(vrtx, nxtvrtx)] = weight
                # print(vrtx, nxtvrtx, weight)
        return edgename

    def addVertex(self, vrtx):  # Add the vertex as a key
        if vrtx not in self.gdict:
            self.gdict[vrtx] = {}

    def addEdge(self, edge):  # Add the new edge
        (vrtx1, vrtx2) = tuple(set(edge))
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]


def testGraph():
    graph_elements = {
        "a": ["b", "c"],
        "b": ["a", "d"],
        "c": ["a", "d"],
        "d": ["e"],
        "e": ["d"]
    }

    # graph_elements = {
    #     "0" : ["1","2"],
    #     "1" : ["0", "3"],
    #     "2" : ["0", "3"],
    #     "3" : ["4"],
    #     "4" : ["3"]
    #     }

    g = Graph(graph_elements)
    g.addVertex('f')
    g.addEdge(['f', 'a'])
    # g.addEdge({'b','a'})
    # g.addEdge({'d','a'})
    print('vertices:', g.getVertices())
    print('edges:', g.findedges())


def testGraphW():
    # d = {("a", "b"): 20}
    graph_elements = {
        "a": {"b": 20, "c": 3},
        "b": {"a": 20, "d": 5},
        "c": {"a": 3, "d": 5}
    }
    g = GraphW(graph_elements)
    g.addVertex('d')
    print('vertices:', g.getVertices())
    print('edges:', g.findedges())
    # g.addEdge({"a", "d", 8})


def main():
    # testGraph()
    testGraphW()


if __name__ == "__main__":
    main()
