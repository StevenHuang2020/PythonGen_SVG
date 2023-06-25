#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Description: Graph structure
# Date: 09/Dec/2021
# Author: Steven Huang, Auckland, NZ
# Copyright (c) 2020-2021, Steven Huang
# License: MIT License
"""
Description: graph data struct definition
"""


class Graph:
    """ graph class """

    def __init__(self, gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict

    def get_vertices(self):
        """ return keys of the dictionary """
        return list(self.gdict.keys())

    def edges(self):
        """ return edges """
        return self.find_edges()

    def find_edges(self):
        """ Find the distinct list of edges """
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename

    def add_vertex(self, vrtx):
        """ Add the vertex as a key """
        if vrtx not in self.gdict:
            self.gdict[vrtx] = []

    def add_edge(self, edge):
        """ Add the new edge """
        (vrtx1, vrtx2) = tuple(set(edge))
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]


class GraphW(Graph):
    """ weighted graph """

    def find_edges(self):
        """ Find the distinct list of edges """
        edgename = {}
        print('dict=', self.gdict)
        for vrtx in self.gdict:
            for nxtvrtx, weight in self.gdict[vrtx].items():
                if (vrtx, nxtvrtx) not in edgename and \
                        (nxtvrtx, vrtx) not in edgename:
                    edgename[(vrtx, nxtvrtx)] = weight
                # print(vrtx, nxtvrtx, weight)
        return edgename

    def add_vertex(self, vrtx):
        """ Add the vertex as a key """
        if vrtx not in self.gdict:
            self.gdict[vrtx] = {}

    def add_edge(self, edge):
        """ Add the new edge """
        (vrtx1, vrtx2) = tuple(set(edge))
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]


def test_graph():
    """ test graph """
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
    g.add_vertex('f')
    g.add_edge(['f', 'a'])
    # g.add_edge({'b','a'})
    # g.add_edge({'d','a'})
    print('vertices:', g.get_vertices())
    print('edges:', g.find_edges())


def test_graph_weighted():
    """ test weighted graph """
    # d = {("a", "b"): 20}
    graph_elements = {
        "a": {"b": 20, "c": 3},
        "b": {"a": 20, "d": 5},
        "c": {"a": 3, "d": 5}
    }
    g = GraphW(graph_elements)
    g.add_vertex('d')
    print('vertices:', g.get_vertices())
    print('edges:', g.find_edges())
    # g.add_edge({"a", "d", 8})


def main():
    """ main function """
    # test_graph()
    test_graph_weighted()


if __name__ == "__main__":
    main()
