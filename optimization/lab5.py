import numpy
import scipy.optimize
import math
import scipy.misc
import lab4_2
import lab4_1
from goto import with_goto

def rosenbrock(a, b, f0):
    def f(x):
        return sum([a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2 for i in range(len(x) - 1)]) + f0

    return f


def prime_rosenbrock(a, b):
    def f(x):
        n = len(x) - 1
        grad_arr = []
        for i in range(1, len(x) - 1):
            grad_arr.append(
                -2 * a * (x[i - 1] ** 2 - x[i]) + 2 * a * 2 * x[i] * (x[i] ** 2 - x[i + 1]) + 2 * b * (x[i] - 1))

        return numpy.array(
            [2 * a * 2 * x[0] * (x[0] ** 2 - x[1]) + 2 * b * (x[0] - 1)] + grad_arr + [-2 * a * (x[n - 1] ** 2 - x[n])])

    return f


def barier(r, g):
    return lambda x: r * sum(1 / gi(x) for gi in g)


def penalty(r, g):
    return lambda x: r * sum([max(0, gi(x)) ** 2 for gi in g]) / 2


def lagr_pen(mu, r, g):
    return lambda x: sum([max(0, mu[i] + r * g[i](x)) ** 2 - mu[i] ** 2 for i in range(len(x))]) / (2 * r)


def prime_constraints():
    def g1(x):
        x1, x2, x3, x4 = x
        return numpy.array([2 * x1, 2 * x2, -3, 2 * x4])

    def g2(x):
        return numpy.array([-1, 0, 0, 0])

    def g3(x):
        return numpy.array([0, -1, 0, 0])

    def g4(x):
        return numpy.array([0, 0, -1, 0])

    def g5(x):
        return numpy.array([0, 0, 0, -1])

    return [g1, g2, g3, g4, g5]


def constraints():
    def g1(x):
        x1, x2, x3, x4 = x
        return (x1 ** 2 + x2 ** 2 - 3 * x3 + x4 ** 2 - 5)

    def g2(x):
        x1, x2, x3, x4 = x
        return -x1

    def g3(x):
        x1, x2, x3, x4 = x
        return -x2

    def g4(x):
        x1, x2, x3, x4 = x
        return -x3

    def g5(x):
        x1, x2, x3, x4 = x
        return -x4

    return [g1, g2, g3, g4, g5]


def mixed(x0, func=rosenbrock(30, 2, 80), eps=0.0000000001):
    rb = 0.5
    Cb = 10

    r = 1
    C = 10

    cons = constraints()
    while True:
        bar = barier(rb, cons)
        pen = penalty(r, cons)
        added = lambda x: pen(x) - bar(x)
        f = lambda x: func(x) + added(x)

        x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if abs(added(x0)) <= eps:
            return x0
        else:
            rb = rb / Cb
            r = r * C


def barier_functions(x0, func=rosenbrock(30, 2, 80), eps=0.0000000001):
    r = 0.5
    C = 10
    cons = constraints()
    while True:
        bar = barier(r, cons)
        f = lambda x: func(x) - bar(x)

        x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if abs(bar(x0)) <= eps:
            return x0
        else:
            r = r / C


def penalty_functions(x0, func=rosenbrock(30, 2, 80), eps=0.0000000001):
    r = 1
    C = 10
    cons = constraints()
    while True:
        pen = penalty(r, cons)
        f = lambda x: func(x) + pen(x)

        x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if pen(x0) <= eps:
            return x0
        else:
            r = C * r


def lagr(x0, func=rosenbrock(30, 2, 80), eps=10 ** -9):
    r = 1
    C = 2
    cons = constraints()
    mu = numpy.random.random(len(cons))
    while True:
        pen = lagr_pen(mu, r, cons)
        f = lambda x: func(x) + pen(x)

        x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if pen(x0) <= eps:
            return x0
        else:
            mu = numpy.array([max(0, mu[i] + r * cons[i](x0)) for i in range(len(mu))])
            r = C * r

@with_goto
def projection(x0, e1, e2, max_iters):
    cons = constraints()



def main():
    target = numpy.array([1, 1, 1, 1])
    x0 = numpy.array([2, 2, 5, 2])
    pen = penalty_functions(x0)
    bar = barier_functions(x0)
    m = mixed(x0)
    l = lagr(x0)
    print(numpy.abs(target - pen))
    print(numpy.abs(target - bar))
    print(numpy.abs(target - m))
    print(numpy.abs(target - l))


if __name__ == "__main__":
    main()
