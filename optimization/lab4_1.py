import copy
import scipy.optimize
import numpy
import math
import lab3_1
import operator
from goto import with_goto

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

@with_goto
def nelder_mead(f, x0, alpha=1, beta=0.5, gamma=2, mu=0.0001, phi=0.01, eps=0.0001):
    n = len(x0)
    simplex = [x0]
    k = 0

    s = 0.1
    l1 = s * (math.sqrt(n + 1) + n - 1) / (n * math.sqrt(2))
    l2 = s * (math.sqrt(n + 1) - 1) / (n * math.sqrt(2))

    for i in range(n):
        li_arr = [l2 for i in range(n)]
        li_arr[i] = l1
        simplex.append(x0 + numpy.array(li_arr))

    label .step1
    print("step1")
    simplex.sort(key=lambda v: f(v))



    label .step2
    print("step2")
    x_cent = (sum(simplex) - simplex[-1])/n

    label .step3
    print("step3")
    xr = x_cent + alpha*(x_cent - simplex[-1])
    if f(xr) <= f(simplex[-2]):
        simplex[-1] = xr
        goto .step1

    label .step31

    print("step31")
    if f(xr) <= f(simplex[0]):
        xe = x_cent + gamma*(x_cent - simplex[-1])
        if f(xe) <= f(xr):
            simplex[-1] = xe
            goto .step1
        else:
            simplex[-1] = xr
    else:
        goto .step5

    label .step4
    print("step4")
    x_cont = x_cent + beta * (x_cent - simplex[-1])
    if f(x_cont) <= f(simplex[-1]):
        simplex[-1] =x_cont
        goto .step1

    label .step5

    for i in range(1,len(simplex)):
        simplex[i] = simplex[0] + mu * (simplex[i] - simplex[0])

    print("step5")
    if sum(map(lambda x: (f(x) - f(x_cent))**2, simplex))/(n+1) <= eps:
        return simplex[0]

    goto .step1


def hooke_jeeves(f, x0, eps=0.00001, delta=[0.001,0.001,0.001,0.001], l=2, beta=2, n=4):
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
        res = scipy.optimize.minimize_scalar(new_f, method='Golden').x

        x0 = (numpy.array(x0) + res * numpy.array(dir)).tolist()


def main():
    print(nelder_mead(rosenbrock(30, 2, 80), numpy.array([2, 2, 2, 2])))


if __name__ == "__main__":
    main()
