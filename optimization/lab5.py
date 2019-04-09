import numpy
from numpy.linalg import inv
import scipy.optimize
import math
import scipy.misc
import lab4_2
import lab3_2
import lab4_1




def rosenbrock(a, b, f0):
    def f(x):
        return sum([a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2 for i in range(len(x) - 1)]) + f0

    return f


def gradient(fun, tol=10 ** -8):
    def func(x):
        res = []
        for i in range(len(x)):
            tmp = numpy.copy(x)
            tmp[i] += tol
            res.append((fun(tmp) - fun(x)) / tol)
        return numpy.array(res)

    return func


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


def mixed(x0, func=rosenbrock(30, 2, 80), eps=10**-8):
    rb = 0.5
    Cb = 10

    r = 1
    C = 10
    k = 0
    x0 = x0.tolist()
    cons = constraints()
    while True:
        k+=1
        bar = barier(rb, cons)
        pen = penalty(r, cons)
        added = lambda x: pen(x) - bar(x)
        f = lambda x: func(x) + added(x)

        # x0 = lab4_1.hooke_jeeves(f, x0)
        x0 = lab4_2.grad_descent(f, gradient(f), x0)
        # x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if abs(added(x0)) <= eps:
            return x0,k
        else:
            rb = rb / Cb
            r = r * C


def barier_functions(x0, func=rosenbrock(30, 2, 80), eps=10**-8):
    r = 0.5
    C = 10
    k=0
    cons = constraints()

    x0 = x0.tolist()
    while True:
        k+=1
        bar = barier(r, cons)
        f = lambda x: func(x) - bar(x)

        x0 = lab4_2.grad_descent(f, gradient(f), x0)
        # x0 = lab4_1.hooke_jeeves(f, x0)
        # print(x0)
        # x0 = scipy.optimize.minimize(f, x0, method='CG').x

        if abs(bar(x0)) <= eps:
            return x0,k
        else:
            r = r / C


def penalty_functions(x0, func=rosenbrock(30, 2, 80), eps=10**-8):
    r = 1
    C = 10
    cons = constraints()
    k = 0
    x0 = x0.tolist()
    while True:
        k+=1
        pen = penalty(r, cons)
        f = lambda x: func(x) + pen(x)

        x0 = lab4_1.hooke_jeeves(f, x0)

        if abs(pen(x0)) <= eps:
            return x0,k
        else:
            r = C * r


def lagr(x0, func=rosenbrock(30, 2, 80), eps=10**-8):
    r = 1
    C = 2
    k=0
    cons = constraints()
    mu = numpy.random.random(len(cons))
    x0 = x0.tolist()
    while True:
        k+=1
        pen = lagr_pen(mu, r, cons)
        f = lambda x: func(x) + pen(x)

        x0 = lab4_2.grad_descent(f, gradient(f), x0)

        if abs(pen(x0)) <= eps:
            return x0,k
        else:
            mu = numpy.array([max(0, mu[i] + r * cons[i](x0)) for i in range(len(mu))])
            r = C * r


def projection(f, x0, e1 = -10,e=10 ** -8, max_iter=100):
    x = x0
    k = 0
    case = 0
    deltax = numpy.array([0.0001,0.0001,0.0001,0.0001])
    g = constraints()
    dg = prime_constraints()
    gradf = prime_rosenbrock(30,2)
    id = numpy.eye(5)
    numpy.delete(id, 4)

    while k < max_iter:
        k += 1
        for gf in g:
            if e1 <= gf(x) <= 0:
                case = 1
                break
        if case:
            gf = gradf(x)
            A = dg(x)
            if numpy.all(gf == 0):
                print(2)
                la = numpy.matmul(numpy.matmul(inv(numpy.matmul(dg(x), A.transpose())), A),
                                  numpy.array([gradf(x).tolist()]).transpose()).transpose().reshape(-1)
                if la <= 0:
                    return [k, x, f(x)]
                max_la = 0
                max_i = 0
                for i, elem in enumerate(la):
                    if elem < 0:
                        max_la = min([max_la, elem])
                        max_i = i
                numpy.delete(A, max_i)
            else:
                print(1)
                deltax = - inv(id - numpy.matmul(A.transpose(), numpy.matmul(A, A.transpose())))
                if deltax < e:
                    la = numpy.matmul(numpy.matmul(inv(numpy.matmul(dg(x), A.transpose())), A),
                                      numpy.array([gradf(x).tolist()]).transpose()).transpose().reshape(-1)

                    if la <= 0:
                        return [k, x, f(x)]
                    max_la = 0
                    max_i = 0
                    for i, elem in enumerate(la):
                        if elem < 0:
                            max_la = min([max_la, elem])
                            max_i = i
                    numpy.delete(A, max_i)
            helper = lambda alpha: x + alpha * deltax
            alpha = scipy.optimize.minimize_scalar(helper, method='Golden')
            x = x + alpha * deltax

    return [k, x, f(x)]


def main():
    target = numpy.array([1, 1, 1, 1])
    # print(numpy.array([g(target) for g in prime_constraints()]))
    x0 = numpy.array([0.7, 0.7, 0.7, 0.7])
    f = rosenbrock(30,2,80)
    # pen = penalty_functions(x0)
    # print(numpy.abs(pen[0]), pen[1], f(pen[0]))
    # bar = barier_functions(x0)
    # print(numpy.abs(bar[0]), bar[1], f(bar[0]))
    # m = mixed(x0)
    # print(numpy.abs(m[0]), m[1], f(m[0]))
    # l = lagr(x0)
    # print(numpy.abs(l[0]), l[1], f(l[0]))

    proj = barier_functions(numpy.array([3,2,3,5]))
    print(proj, f(proj[0]))


if __name__ == "__main__":
    main()
