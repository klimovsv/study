import numpy as np
import math
import uuid
from itertools import product
import scipy.optimize
import operator
import lab5


def minimize(f, x0):
    return scipy.optimize.minimize(f, x0, method='CG').x
    # return lab5.penalty_functions(x0, f, cons=[])[0]


def dist(x1, x2):
    return math.sqrt(sum(map(lambda v: (v[0] - v[1]) ** 2, zip(x1, x2))))


class Cluster:
    def __init__(self, point):
        self.points = [point]
        self.id = uuid.uuid4()
        self.main_point = point
        self.metric = dist

    def __hash__(self):
        return self.id.int

    def add_point(self, point):
        self.points.append(point)

    def add_points(self, points):
        for p in points:
            self.points.append(p)

    def dist(self, cluster):
        point_pairs = list(product(self.points, cluster.points))
        d = min(map(lambda pair: dist(pair[0], pair[1]), point_pairs))
        return d

    def get_delegate(self, func):
        return min(self.points, key=func)

    def union(self, cluster):
        points = self.points + cluster.points
        new_cluster = Cluster(points[0])
        new_cluster.add_points(points[1:])
        return new_cluster

    def __repr__(self):
        return "{}".format(self.main_point)


def shekel(a, b, c, A, f):
    def func(x):
        res = 0
        for i in range(A.shape[0]):
            loc_res = 0
            for j in range(len(x)):
                loc_res += (x[j] - A[i][j]) ** 2
            loc_res = b * loc_res + f[i]

            res += a / loc_res
        return -res

    return func


def comp_points(points, f, eps=10 ** -8):
    opt_points = list(map(lambda x: minimize(f, x), points))
    clusters = k_nearest(opt_points, eps)

    if len(clusters) == 1:
        delegate = clusters[0].get_delegate(f)
        return minimize(f, delegate)

    delegate_points = list(map(lambda c: c.get_delegate(f), clusters))
    print(len(delegate_points), len(points), eps)
    if len(delegate_points) == len(points):
        return comp_points(delegate_points, f, eps * 10)
    return comp_points(delegate_points, f, eps)


def k_nearest(points, eps):
    clusters = list(map(lambda p: Cluster(p), points))
    while True:
        pairs = []
        for i, c in enumerate(clusters):
            pairs += list(product([c], clusters[:i] + clusters[i + 1:]))

        if len(pairs) == 0:
            return clusters

        c1, c2 = min(pairs, key=lambda pair: pair[0].dist(pair[1]))

        if c1.dist(c2) < eps:
            new_cluster = c1.union(c2)
            clusters.remove(c1)
            clusters.remove(c2)
            clusters.append(new_cluster)
        else:
            return clusters

        if len(clusters) == 1:
            return clusters


def main():
    a, b, c = 1, 1, 2
    A = np.array([[0, 2, 5],
                  [2, 3, 5],
                  [1, 6, 7]])
    f_arr = np.array([2 / 6, 4 / 6, 6/ 6])
    f = shekel(a, b, c, A, f_arr)

    K = 200
    print(f(A[0]),f(A[1]),f(A[2]))
    points = np.random.uniform(low=0, high=8, size=(K, 3))
    print(comp_points(points, f))


if __name__ == '__main__':
    main()
