import copy
import numpy
import math
import lab3_1
import operator


# from goto import with_goto

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


def mass_cent(simplex, h):
    return (sum(simplex) - simplex[h]) / (len(simplex) - 1)


def nelder_mead(f, x0, alpha=1, beta=0.5, gamma=2, delta=0.5, mu=0.0001, phi=0.01, eps=10**-5, maxiters=100000):
    n = len(x0)
    simx = [x0]
    k = 0

    s = 0.1
    l1 = s * (math.sqrt(n + 1) + n - 1) / (n * math.sqrt(2))
    l2 = s * (math.sqrt(n + 1) - 1) / (n * math.sqrt(2))

    for i in range(n):
        li_arr = [l2 for i in range(n)]
        li_arr[i] = l1
        simx.append(x0 + numpy.array(li_arr))

    def sort(lst):
        d = [(x, f(x)) for x in lst]
        d.sort(key=operator.itemgetter(1))
        lst = list(map(operator.itemgetter(0), d))
        return lst

    while k < maxiters:
        k += 1



        simx = sort(simx)
        xc = mass_cent(simx, n)

        if sum([(f(x) - f(xc)) ** 2 for x in simx]) / (n + 1) <= eps:
            return simx[0],k

        #exp reflection
        xr = xc + alpha * (xc - simx[-1])
        xe = xr + gamma * (xr - xc)
        if f(xr) < f(simx[-1]) or f(xe) < f(simx[-1]):
            minx = min(xr, xe, key=f)
            simx[-1] = minx
            continue

        #contraction
        c1 = (simx[-1] + xc)/2
        c2 = (xc + xr)/2
        if f(c1) < f(simx[-1]) or f(c2) < f(simx[-1]):
            minx = min(c1, c2, key=f)
            simx[-1] = minx
            continue

        for i in range(1, len(simx)):
            simx[i] = simx[0] + mu * (simx[i] - simx[0])


    return simx[0], k


def hooke_jeeves(f, x0, eps=10**-5, delta=[0.001, 0.001, 0.001, 0.001], l=2, beta=2, n=4, max_iters=10000):
    k = 0
    while k < max_iters:
        k += 1
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
        res = lab3_1.golden([0, 2], new_f)[0]

        x0 = (numpy.array(x0) + res * numpy.array(dir)).tolist()

    return x_next


def main():
    f = rosenbrock(30, 2, 80)
    hj = hooke_jeeves(rosenbrock(30, 2, 80), [1, 3, 2, 1])
    print(hj, f(hj[0]))
    nm = nelder_mead(rosenbrock(30, 2, 80), numpy.array([0.5, 0.5, 0.5, 0.5]))
    print(nm,f(nm[0]))


if __name__ == "__main__":
    main()
