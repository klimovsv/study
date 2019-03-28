import copy
import scipy
import numpy
import math
import lab3_1
import operator


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


def mass_cent(simplex, h):
    return (sum(simplex) - simplex[h]) / len(simplex)

def condition(simplex, l_ind, eps , f):
    res = 0
    for i, x in enumerate(simplex):
        res += (f(simplex[i]) - f(simplex[l_ind]))**2
    return math.sqrt(res/(len(simplex)+1)) <= eps


def nelder_mead(f, x0, alpha=1, beta=0.5, gamma=2, mu=0.5, phi=0.01, eps=0.001):
    n = len(x0)
    simplex = [x0]
    k = 0

    s = 0.1
    l1 = s * (math.sqrt(n + 1) + n - 1) / (n * math.sqrt(2))
    l2 = s * (math.sqrt(n + 1) - 1) / (n * math.sqrt(2))

    for i in range(n):
        li_arr = [l2 for i in range(n)]
        li_arr[i] = l1
        simplex.append(x0 + li_arr)

    fi = []
    for x in simplex:
        fi.append(f(x))

    while True:
        k += 1
        zipped = list(zip(simplex, fi, range(n + 1)))
        xh_z = max(zipped, key=operator.itemgetter(1))
        xl_z = min(zipped, key=operator.itemgetter(1))
        cent = mass_cent(simplex, xh_z[2])
        h_ind = xh_z[2]
        l_ind = xl_z[2]

        xr = (1 + alpha) * cent - alpha * simplex[h_ind]
        fr = f(xr)

        if fr < f(simplex[l_ind]):
            xe = (1 - gamma) * cent + gamma * xr
            fe = f(xe)
            if fe < fr:
                simplex[h_ind] = xe
            elif fr < fe:
                simplex[h_ind] = xr
            if condition(simplex, l_ind, eps, f):
                return simplex[l_ind]
            else:
                continue

        elif f(simplex[l_ind]) < fr < f(simplex[h_ind]):
            simplex[h_ind], xr = xr, simplex[h_ind]
            fr = f(xr)
        xs = beta * simplex[h_ind] + (1 - beta) * cent
        fs = f(xs)
        if fs < f(simplex[h_ind]):
            simplex[h_ind] = xs
            if condition(simplex, l_ind, eps, f):
                return simplex[l_ind]
            else:
                continue
        elif fs > f(simplex[h_ind]):
            for i, x in enumerate(simplex):
                if i != l_ind:
                    simplex[i] = simplex[l_ind] + (x - simplex[l_ind]) * mu

        if condition(simplex, l_ind, eps, f):
            return simplex[l_ind]


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
    # print(hooke_jeeves(rosenbrock(30, 2, 80),
    #                    [1.5, 1.5, 1.5, 1.5],
    #                    0.00001,
    #                    [0.1, 0.1, 0.1, 0.1],
    #                    1,
    #                    2))
    print(nelder_mead(rosenbrock(30, 2, 80), numpy.array([2, 2])))


if __name__ == "__main__":
    main()
