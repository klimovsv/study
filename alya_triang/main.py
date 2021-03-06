from structs import *
import random
import sys
from typing import *
import matplotlib.pyplot as plt

xrange = (2, 10)
yrange = (2, 10)


def show_plot(triangles=None, points=None, vecs=None, circles=None):
    t = 1
    lenx = xrange[1] - xrange[0] + 2 * t
    leny = yrange[1] - yrange[0] + 2 * t

    fig = plt.figure(figsize=[lenx, leny])
    plt.autoscale(False)
    ax = fig.add_subplot(111)

    if triangles:
        for t in triangles:
            patch = t.get_patch()
            ax.add_patch(patch)

    if points:
        for p in points:
            ax.scatter(p.x, p.y)

    if not vecs is None:
        for line in vecs:
            ax.add_line(line.get_line())

    if not circles is None:
        for c in circles:
            circle = plt.Circle((c[0].x, c[0].y), c[1], color='r', fill=False)
            ax.add_artist(circle)

    t = 1
    ax.set_xlim(xrange[0] - t , xrange[1] + t )
    ax.set_ylim(yrange[0] - t , yrange[1] + t )
    plt.show()
    plt.close()


def generate_new(edges: List[Edge], point: Point):
    # создание новых треугольников из списка ребер и точки
    # с соблюдением согласованности ребер
    triangles = []
    edges_d = {}

    for edge in edges:
        if not edge.a.id in edges_d:
            e = Edge(point, edge.a)
            edges_d[edge.a.id] = e
        if not edge.b.id in edges_d:
            e = Edge(point, edge.b)
            edges_d[edge.b.id] = e

        triangle = Triangle()
        triangles.append(triangle)
        triangle.add_edges(edge, edges_d[edge.a.id], edges_d[edge.b.id])
        triangle.get_vertices()

    return triangles


def find(point, triangle: Triangle):
    k = 0
    while True:
        k += 1
        edges = triangle.edges
        # берем любую точку внутри треугольника и
        # проводим отрезок из нее к искомому треуугольнику
        center = triangle.point_inside()
        line = Vec(center, point)
        ind = -1

        # находим ребро, которое пересекает отрезок
        for i, e in enumerate(edges):
            if line.intersect(Vec(e.a, e.b)):
                ind = i
                break

        # если не пересекает => найден нужный треугольник
        if ind == -1:
            return triangle, k

        # иначе переходим к следующему через пересеченное ребро
        triangle = edges[ind].get_another_triangle(triangle.id)


def get_connected_edges(edge, edges):
    for e in edges:
        if not get_common_point(e, edge) is None:
            return e, edge


def get_common_point(e1, e2):
    e1p = set([e1.a, e1.b])
    if e2.a in e1p:
        return e2.a
    elif e2.b in e1p:
        return e2.b
    return None


def get_common_edge(t1, t2):
    t1e = set()
    for e in t1.edges:
        t1e.add(e)

    for e in t2.edges:
        if e in t1e:
            return e


def main_loop(triangles: Dict[str, Triangle], points: List[Point]):
    # инициализация начального дерева
    tree_root = kdtree(list(triangles.values()))
    count = 0
    iters = []
    for i in range(len(points)):
        p = points[i]

        best_node = [None]
        min_dist = [sys.maxsize]
        # пытаемся найти треугольник в котором находится точка
        search(p, tree_root, best_node, min_dist)
        triangle = best_node[0].item

        # если не находится в нем, то используем обычный поиск
        # (в среднем доходим  за 2-3 итерации)
        if not p.inside(triangle):
            count += 1
            triangle , k = find(p, triangle)
            iters.append(k)

        # удаляем найденный треугольник и информацию о нем из ребер
        triangles.pop(triangle.id)
        for e in triangle.edges:
            e.delete_triangle(triangle.id)

        # создаем 3 новых, формируемых из точки и ребер старого треугольника
        new_t = generate_new(triangle.edges, p)
        for t in new_t:
            triangles[t.id] = t

        # инициализируем очередь на проверку условий делоне
        next_triangles = new_t

        while len(next_triangles) != 0:
            # получаем следующий треугольник на проерку
            next_t = next_triangles.pop()

            # если его уже нет в триангуляции, то пропускаем и берем следующий
            if not next_t.id in triangles:
                continue

            neighbours = []
            # сбор всех соседей у текущего треугольника
            for e in next_t.edges:
                if not e.edged:
                    neighbours.append(e.get_another_triangle(next_t.id))

            # проверка для каждого соседа уловия делоне
            for t in neighbours:
                # находим общее ребро
                edge = get_common_edge(t, next_t)
                # оставшиеся ребра 1-го треугольника
                aedges = next_t.get_other_edges(edge.id)
                # оставшиеся ребра 2-го треугольника
                bedges = t.get_other_edges(edge.id)
                # находим противолежащие вершины
                x = get_common_point(aedges[0], aedges[1])
                y = get_common_point(bedges[0], bedges[1])
                # если не выполняется условие делоне то перестраиваем
                if not next_t.delauney(y) or not t.delauney(x):
                    # формируем новое ребро между противолежащими вершинами
                    new_edge = Edge(x, y)

                    # удаляем старые треугольники из триангуляции
                    # а также информацию о них из ребер
                    triangles.pop(t.id)
                    for e in t.edges:
                        e.delete_triangle(t.id)
                    triangles.pop(next_t.id)
                    for e in next_t.edges:
                        e.delete_triangle(next_t.id)

                    # формируем ребра для новых треугольников
                    edges1 = get_connected_edges(aedges[0], bedges)
                    edges2 = get_connected_edges(aedges[1], bedges)

                    # создаем новые треугольники из данных ребер
                    t1 = Triangle()
                    t2 = Triangle()
                    t1.add_edges(new_edge, edges1[0], edges1[1])
                    t2.add_edges(new_edge, edges2[0], edges2[1])

                    # добавляем треугольники в триангуляцию и в очередь проверки
                    next_triangles.append(t1)
                    triangles[t1.id] = t1
                    next_triangles.append(t2)
                    triangles[t2.id] = t2
                    break

        # перестроение дерева с новыми треугольниками из триангуляции
        tree_root = kdtree(list(triangles.values()))
    # статистика по общему количеству точек
    # количеству точек, для которых не был найден точный треугольник при помощи дерева
    # и среднее количество итерации на доп поиск
    print(len(points), count, np.average(iters))
    return triangles


def generate(xrange, yrange, n):
    points = []
    for i in range(n):
        points.append(Point(random.uniform(*xrange),
                            random.uniform(*yrange)))
    return points


def generate_points(xrange, yrange, n, divisions):
    lenx = xrange[1] - xrange[0]
    leny = yrange[1] - yrange[0]
    points = []
    sx = lenx / divisions
    sy = leny / divisions
    for i in range(divisions):
        for j in range(divisions):
            points += generate((xrange[0] + sx * i, xrange[0] + sx * (i + 1)),
                               (yrange[0] + sy * j, yrange[0] + sy * (j + 1)),
                               n)

    return points


def generate_from_points(points, p):
    points.append(points[0])
    edges = []
    for i in range(len(points) - 1):
        edges.append(Edge(points[i], points[i + 1], edged=True))

    return generate_new(edges, p)


def init(xrange, yrange):
    # генерация точек на плоскости
    # принимает отрезок по x, отрезок по y
    # количество точек в разбиении плоскости
    # и количество разбиений (формируется сетка NxN)
    points = generate_points(xrange, yrange, 100, 1)
    ind = 0
    p = points[ind]

    t = 0.2
    n = 1
    lenx = xrange[1] - xrange[0]
    leny = yrange[1] - yrange[0]

    # создание суперструктуры прямоугольника
    # с равномерно распределенными точками по периметру
    # количество точек на ребрах прямоугольнкиа - n
    p_s = [Point(xrange[0] - t, yrange[0] - t)]

    for i in range(n):
        p_s.append(Point(xrange[0] + lenx / (n + 1) * (i + 1), yrange[0] - t))

    p_s.append(Point(xrange[1] + t, yrange[0] - t))

    for i in range(n):
        p_s.append(Point(xrange[1] + t, yrange[0] + leny / (n + 1) * (i + 1)))

    p_s.append(Point(xrange[1] + t, yrange[1] + t))

    for i in range(n):
        p_s.append(Point(xrange[1] - lenx / (n + 1) * (i + 1), yrange[1] + t))

    p_s.append(Point(xrange[0] - t, yrange[1] + t))

    for i in range(n):
        p_s.append(Point(xrange[0] - t, yrange[1] - leny / (n + 1) * (i + 1)))

    return generate_from_points(p_s, p), points[ind + 1:]


def main():
    triangles, points = init(xrange, yrange)

    t_d = {}
    for t in triangles:
        t_d[t.id] = t

    triangles = list(main_loop(t_d, points).values())
    circles = []

    for t in triangles:
        cent = t.cent()
        p1 = t.get_vertices()[0]
        circles.append([cent, Vec(cent, p1).length()])

    show_plot(triangles=triangles)


if __name__ == "__main__":
    main()
