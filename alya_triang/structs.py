import operator
import math
import sys

def dist(p1 , p2):
    return math.sqrt((p2['x']-p1['x'])**2 + (p2['y']-p1['y'])**2)

def search(node, point, best_node, min_dist=sys.maxsize):
    d = dist(node['item'], point)

    if d < min_dist:
        mindist = d
        best_node = node






def kdtree(point_list, depth=0):
    if not point_list:
        return None

    k = len(point_list[0])

    axis = 'x' if depth % k == 0 else 'y'
    point_list.sort(key=lambda v: v[axis])
    median = len(point_list) // 2

    return {
        'item': point_list[median],
        'axis': axis,
        'left': kdtree(point_list[:median], depth + 1),
        'right': kdtree(point_list[median + 1:], depth + 1)
    }


def main():
    point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    point_list = [dict(zip('xy', [p[0], p[1]])) for p in point_list]
    print(point_list)
    tree_root = kdtree(point_list)
    print(tree_root)


if __name__ == "__main__":
    main()