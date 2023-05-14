# Python3 Steven
# For connecting random points
import numpy as np
import random
from itertools import combinations  # permutations


class VertexPt():
    def __init__(self, id, point):
        self.point = point
        self.id = id

    def setDistance(self, distance):
        self.distance = distance

    def __str__(self):
        return 'Vertex: id=' + str(self.id) + ' point=' + str(self.point)

    def getDistanceVectorIds(self, K=2):
        if K <= 0:
            K = len(self.distance)
            # print('all K=', K)
        # top_k_idx = self.distance.argsort()[::-1][0:K+1]
        # start from 1,skip self index
        low_k_idx = self.distance.argsort()[1:K + 1]
        return low_k_idx


class GraphPoints():
    def __init__(self, points):
        self.VertexPt_list = []
        for i, pt in enumerate(points):
            self.VertexPt_list.append(VertexPt(i, pt))

        self.ptMatrix = None
        for i in range(len(self.VertexPt_list)):
            v = self.getVertextPoint(self.VertexPt_list[i])
            self.ptMatrix = np.concatenate(
                (self.ptMatrix, v), axis=1) if self.ptMatrix is not None else v

        # print('self.ptMatrix=',self.ptMatrix)
        for v in self.VertexPt_list:
            pt = self.getVertextPoint(v)

            # res = np.asarray(pt - self.ptMatrix)
            # print('res=',res.shape,res)
            # print('res**2=',res**2)

            # print('sum1 res**2=',np.sum(res**2, axis=1))
            # print('sum0 res**2=',np.sum(res**2, axis=0))
            distances = np.sqrt(
                np.sum(np.asarray(pt - self.ptMatrix) ** 2, axis=0))
            # print('distances=',len(distances),distances)
            v.setDistance(distances)

    def getVertexNearstPtIndex(self, K=8):
        # K = K if K < len(self.VertexPt_list) else len(self.VertexPt_list)

        ys = None
        for v in self.VertexPt_list:
            low_k_idx = v.getDistanceVectorIds(K)
            # print('low_k_idx=',low_k_idx)
            ys = np.vstack([ys, low_k_idx]) if ys is not None else low_k_idx

        # print('ys=',ys)
        self.shortestMatrix = ys
        return self.shortestMatrix

    def getVertextPoint(self, vertex):
        # pt = self.VertexPt_list[index].point
        pt = vertex.point
        return np.array([[pt[0]], [pt[1]]])

    def show(self):
        for i in self.VertexPt_list:
            print(i)

    def getConnectionMatrix(self, K=2, KNearst=4):
        def removeItem(conM, i):
            if conM is not None:
                for con in conM:
                    if con[1] == i:
                        yield con[0]
            return None

        self.getVertexNearstPtIndex(K=KNearst)
        conMatrix = None
        for i, v in enumerate(self.VertexPt_list):
            shortest = list(self.shortestMatrix[i])
            # print('---------')
            # print('cur conMatrix:',conMatrix)
            # print('---------')

            # print('start:',i,shortest)
            for vIndex in removeItem(conMatrix, i):
                # vIndex =  removeItem(conMatrix,i)
                # print('remove:',i,shortest,vIndex)
                if vIndex is not None and vIndex in shortest:
                    shortest.remove(vIndex)

            # print('after remove:',i,shortest)
            if len(shortest) == 0:
                con = np.array([[i, -1]])
            else:
                N = len(shortest) if K > len(shortest) else K
                # print('start to choice:',i,shortest)
                for s in random.sample(shortest, N):
                    con = np.array([[i, s]])
                    conMatrix = np.concatenate(
                        (conMatrix, con)) if conMatrix is not None else con
        # print('conMatrix=',conMatrix)
        return conMatrix

    def getAllConnectionMatrix(self):
        size = len(self.VertexPt_list)
        conAllMatrix = np.array(list(combinations(range(size), 2)))
        return conAllMatrix

    def getConnectionMatrix2(self, KNearst=4):
        conAllMatrix = self.getAllConnectionMatrix()
        # print('conAllMatrix=',conAllMatrix)

        conMatrix = None
        self.getVertexNearstPtIndex(K=KNearst)
        for con in conAllMatrix:  # filter nearst points to connect
            id = con[0]
            conId = con[1]
            shortest = list(self.shortestMatrix[id])
            # print('start:',id, shortest)
            if conId in shortest:
                connect = np.array([[id, conId]])
                conMatrix = np.concatenate(
                    (conMatrix, connect)) if conMatrix is not None else connect

        return conMatrix


def main():
    points = []
    points.append((1, 2))
    points.append((3, 4))
    points.append((5, 6))
    points.append((7, 6))
    points.append((9, 8))
    points.append((9, 5))

    graph = GraphPoints(points)
    # graph.show()

    mat = graph.getConnectionMatrix2(KNearst=4)
    print('mat=', mat)


if __name__ == '__main__':
    main()
