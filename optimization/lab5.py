import numpy
import scipy.optimize
import math
import scipy.misc
import lab4_2
import lab4_1


def rosenbrock(a, b, f0):
    def f(x):
        return sum([a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2 for i in range(len(x) - 1)]) + f0

    return f


def barier(r, g):
    return lambda x: -r * sum(1/gi(x) for gi in g)


def penalty(r, g):
    return lambda x: r * sum([max(0, gi(x))**2 for gi in g]) / 2


def F(ros, pen):
    return lambda x: ros(x) + pen(x)


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


def barier_functions(x0, dx=numpy.array([10 ** -9 for i in range(4)]), eps=0.0001):
    rosenbr = rosenbrock(30, 2, 80)
    r = 0.5
    C = 10
    cons = constraints()
    while True:
        # pen = barier(r, cons)
        bar = barier(r, cons)
        f = lambda x: rosenbr(x) + bar(x)

        def prime(x):
            grad_vec = []
            for i in range(len(x0)):
                tmp = numpy.zeros(len(x0))
                tmp[i] = dx[i]
                grad_vec.append(tmp)
            return numpy.array([(f(x + grad_vec[i]) - f(x)) / dx[i] for i in range(len(x0))])

        x0 = lab4_2.grad_descent(f, prime, x0, e1=eps, e2=eps, delta=eps)
        print(x0)
        if abs(bar(x0)) <= eps:
            return x0
        else:
            r = r / C


def penalty_functions(x0, dx=numpy.array([10 ** -9 for i in range(4)]), eps=0.0001):
    rosenbr = rosenbrock(30, 2, 80)
    r = 1
    C = 0.5
    cons = constraints()
    while True:
        pen = penalty(r, cons)
        f = F(rosenbr, pen)

        def prime(x):
            grad_vec = []
            for i in range(len(x0)):
                tmp = numpy.zeros(len(x0))
                tmp[i] = dx[i]
                grad_vec.append(tmp)
            return numpy.array([(f(x + grad_vec[i]) - f(x)) / dx[i] for i in range(len(x0))])

        x0 = lab4_2.fletcher_powell(f, prime, x0, e1=eps, e2=eps, delta=eps)

        if pen(x0) <= eps:
            return x0
        else:
            r = C * r


def main():
    print(penalty_functions(numpy.array([2, 2, 5, 2])))
    print(barier_functions(numpy.array([2, 2, 5, 2])))


if __name__ == "__main__":
    main()
