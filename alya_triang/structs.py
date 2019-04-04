import operator
import math
import sys
from collections import namedtuple
from pprint import pformat
import numpy as np


import uuid
import math
from typing import *
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.lines import Line2D

Point = None
Triangle = None


class Vec:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.x = b.x - a.x
        self.y = b.y - a.y

    def length(self):
        return math.sqrt(self.x**2+self.y**2)
    def get_line(self):
        return Line2D([self.a.x, self.b.x], [self.a.y, self.b.y])

    def cross(self, other):
        return np.cross([self.x, self.y], [other.x, other.y])


    def intersect(self, other):
        start1 = self.a
        start2 = other.a
        end1 = self.b
        end2 = other.b
        dir1 = Point(self.x, self.y)
        dir2 = Point(other.x, other.y)
        a1 = -dir1.y
        b1 = +dir1.x
        d1 = -(a1 * start1.x + b1 * start1.y)
        a2 = -dir2.y
        b2 = +dir2.x
        d2 = -(a2 * start2.x + b2 * start2.y)


        seg1_line2_start = a2 * start1.x + b2 * start1.y + d2
        seg1_line2_end = a2 * end1.x + b2 * end1.y + d2
        seg2_line1_start = a1 * start2.x + b1 * start2.y + d1
        seg2_line1_end = a1 * end2.x + b1 * end2.y + d1

        if seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0:
            return False
        else:
            return True

    @staticmethod
    def inside_triangle(vec1, vec2, p):
        diag = Vec(Point(0, 0), Point(vec1.x + vec2.x, vec1.y + vec2.y))
        x = p.x + diag.x / 4
        y = p.y + diag.y / 4
        return Point(x, y)


class Edge:
    def __init__(self, a: Point, b: Point, edged=False):
        self.id = uuid.uuid4().int
        self.a = a
        self.b = b
        self.edged = edged
        self.triangles = {}

    def get_another_triangle(self, t_id):
        for id, t in self.triangles.items():
            if id != t_id:
                return t

    def add_triangle(self, triangle: Triangle):
        self.triangles[triangle.id] = triangle

    def delete_triangle(self, t_id: uuid.UUID):
        self.triangles.pop(t_id)

    def unvisit(self):
        for t in self.triangles.values():
            t.visited = False

    def __hash__(self):
        return self.id

class Point:
    def __init__(self, x, y, edged=False):
        self.id = uuid.uuid4().int
        self.x = x
        self.y = y
        self.edged = edged

    def __str__(self):
        return "({} , {})".format(self.x, self.y)

    def __repr__(self):
        return "({} , {})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def inside(self, t):
        triangle = Path([(p.x, p.y) for p in t.p])
        points = np.array([self.x, self.y]).reshape(1, 2)
        res = triangle.contains_points(points)
        return res[0]

    def __hash__(self):
        return self.id


class Triangle:
    def __init__(self, points=None):
        self.id = uuid.uuid4().int
        self.edges = []
        self.color = "#0000ff"
        self.p = points
        self.visited = False
        self.x = None
        self.y = None
        self.cent_prop = None

    def __repr__(self):
        return self.centroid().__repr__()

    def centroid(self):
        if self.x is None:
            res = Point(0,0)
            for p in self.get_vertices():
                res += p
            self.x = res.x/3
            self.y = res.y/3
        return Point(self.x, self.y)

    def get_vertices(self):
        if self.p is None:
            p = {}
            for e in self.edges:
                if e.a.id not in p:
                    p[e.a.id] = e.a
                if e.b.id not in p:
                    p[e.b.id] = e.b
            self.p = list(p.values())
            self.centroid()
        return self.p

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        edge.add_triangle(self)

    def add_edges(self, *args):
        for e in args:
            self.edges.append(e)
            e.add_triangle(self)

    def set_color(self, color):
        self.color = color

    def get_patch(self):
        p = self.get_vertices()
        verts = [(p.x, p.y) for p in p] + [(p[0].x, p[0].y)]
        codes = [Path.MOVETO] + [Path.LINETO for i in range(len(p) - 1)] + [Path.CLOSEPOLY]
        return patches.PathPatch(Path(verts, codes), edgecolor=self.color,
                                 facecolor='none', lw=2, linewidth=0.01)

    def inside(self, point: Point):
        area = self.area()
        res = 0
        eps = 10 ** -5
        for edge in self.edges:
            t = Triangle()
            t.add_edges(Edge(point, edge.a), Edge(edge.a, edge.b), Edge(point, edge.b))
            res += t.area()
        return res - area <= 0 and abs(res - area) <= eps


    def get_other_edges(self, id):
        return list(filter(lambda v: v.id != id, self.edges))

    def cent(self):

        if self.cent_prop is not None:
            return self.cent_prop

        [p1, p2, p3] = self.get_vertices()
        ax, ay, bx, by, cx, cy = p1.x, p1.y, p2.x, p2.y, p3.x, p3.y
        dx = bx - ax
        dy = by - ay
        ex = cx - ax
        ey = cy - ay
        bl = dx * dx + dy * dy
        cl = ex * ex + ey * ey
        d = dx * ey - dy * ex
        x = ax + (ey * bl - dy * cl) * 0.5 / d
        y = ay + (dx * cl - ex * bl) * 0.5 / d

        self.cent_prop = Point(x, y)
        return self.cent_prop

    def point_inside(self):
        [p1, p2, p3] = self.get_vertices()
        vec1 = Vec(p1, p2)
        vec2 = Vec(p1, p3)

        return Vec.inside_triangle(vec1, vec2, p1)


    def delauney(self, point: Point):
        x0, y0 = point.x, point.y
        [p1, p2, p3] = self.get_vertices()
        cent = self.cent()
        r = Vec(cent, p1).length()
        condition = (x0 - cent.x)**2 + (y0 - cent.y)**2 >= r**2
        return condition



class Node(namedtuple('Node', 'item axis left right')):
    def __repr__(self):
        return pformat(tuple(self))


def dist(p1, p2):
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def search(point, node, best_node, min_dist):
    if node is None:
        return

    d = dist(point, node.item)
    if d < min_dist[0]:
        best_node[0] = node
        min_dist[0] = d

    p_val = point.__getattribute__(node.axis)
    node_val = node.item.__getattribute__(node.axis)
    if p_val <= node_val:
        if p_val - min_dist[0] <= node_val:
            search(point, node.left, best_node, min_dist)
        if p_val + min_dist[0] > node_val:
            search(point, node.right, best_node, min_dist)
    else:
        if p_val + min_dist[0] > node_val:
            search(point, node.right, best_node, min_dist)
        if p_val - min_dist[0] <= node_val:
            search(point, node.left, best_node, min_dist)


def kdtree(triangles, depth=0):
    if not triangles:
        return None

    k = 2

    axis = 'x' if depth % k == 0 else 'y'
    triangles.sort(key=operator.attrgetter(axis))
    median = len(triangles) // 2

    return Node(
        item=triangles[median],
        axis=axis,
        left=kdtree(triangles[:median], depth + 1),
        right=kdtree(triangles[median + 1:], depth + 1)
    )


def main():
    points = [Point(0, 0), Point(0, 1), Point(1, 0)]
    t = Triangle(points)
    # print(t)

    p1 = Point(0, 0)
    p2 = Point(2, 0)
    p3 = Point(2, 2)
    p4 = Point(0, 2)
    p5 = Point(1, 1)
    t1 = Triangle([p1, p2, p5])
    t2 = Triangle([p1, p4, p5])
    t3 = Triangle([p2, p3, p5])
    t4 = Triangle([p3, p4, p5])
    print([t1, t2, t3, t4])
    tree_root = kdtree([t1, t2, t3, t4])
    # print(tree_root)
    p = Point(1.7, 1.2)
    best_node = [None]
    min_dist = [sys.maxsize]
    search(p, tree_root, best_node, min_dist)
    res_t = best_node[0].item
    print(res_t, p)
    print(p.inside(res_t))

if __name__ == "__main__":
    main()
