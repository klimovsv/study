import copy
import scipy
import numpy
import lab3_1


def rosenbrock(a, b, f0):
    def f(x):
        res = 0
        for i in range(len(x) - 1):
            res += a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2
        return res + f0

    return f


def to_scipy(f, x, dir):
    d = numpy.array(dir)
    x0 = numpy.array(x)

    def new_f(t):
        return f((x0 + t * d).tolist())

    return new_f


def dir_step(x, delta, factor):
    tmp = []
    for i in range(len(x)):
        tmp.append(step(x, delta, i, factor)[i])
    return tmp


def step(x, delta, i, factor):
    tmp = copy.copy(x)
    tmp[i] += delta[i] * factor
    return tmp


def find_new(x0, delta, n, f):
    x_next = x0

    for i in range(n):
        xl = step(x_next, delta, i, -1)
        xr = step(x_next, delta, i, 1)
        if f(xl) < f(x_next):
            x_next = xl
        elif f(xr) < f(x_next):
            x_next = xr

    return x_next


def next_point(x1, x2, l):
    x3 = []
    for x1i, x2i in zip(x1, x2):
        x3.append(x1i + l * (x2i - x1i))
    return x3


def hooke_jeeves(f, x0, eps, delta, l, beta, n=4):
    while True:
        x_next = find_new(x0, delta, n, f)

        if x_next == x0:
            flag = False
            for i, d in enumerate(delta):
                if d > eps:
                    flag = True
                    delta[i] = d / beta
            if flag:
                continue
            else:
                return x_next

        dir = [l * (x2 - x1) for x2, x1 in zip(x_next, x0)]
        new_f = to_scipy(f, x0, dir)

        interval = lab3_1.get_start_interval(new_f, 0, 0.001)
        res = lab3_1.bisection(interval, new_f, eps)[0]

        x0 = (numpy.array(x0) + res * numpy.array(dir)).tolist()


def main():
    print(hooke_jeeves(rosenbrock(30, 2, 80),
                       [1.5, 1.5, 1.5, 1.5],
                       0.00001,
                       [0.1, 0.1, 0.1, 0.1],
                       1,
                       2))


if __name__ == "__main__":
    main()
