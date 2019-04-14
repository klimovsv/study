import GA
import lab5
import numpy as np
import scipy.optimize


def f1(x):
    x1, x2, x3 = x
    return 2 * x1 ** 2 + 2 * x1 + x2 ** 2 - 6 * x1 - 5 * x2


def f2(x):
    x1, x2, x3 = x
    return 3 * (x1 - 2) ** 2 + 2 * (x2 - 5) ** 2


def c1(x):
    x1, x2, x3 = x
    return 3 * x1 + x2 + x3 - 8


def c2(x):
    x1, x2, x3 = x
    return 5 * x2 - x1 - 10


def constraints():
    return [c1, c2]


def main():
    x0 = np.array([1, 1, 0])
    xf1 = lab5.barier_functions(x0, func=f1, cons=constraints())[0]
    xf2 = lab5.barier_functions(x0, func=f2, cons=constraints())[0]
    f_star = np.array([f1(xf1), f2(xf2)])
    print(f_star)

    fs = [f1, f2]
    for i in range(1, 10):
        w = [i/10, 1 - i/10]
        new_f = lambda x: sum([w[j] * (fs[j](x) - f_star[j]) for j in range(len(w))])
        x = lab5.barier_functions(x0, func=new_f, cons=constraints())[0]
        print(f1(x), f2(x))

        alpha = -1000
        beta = 1000

        mut = GA.mutate_function(alpha, beta)
        x = GA.ga(new_f, mutation=mut, alpha=alpha, beta=beta, epoch=1000)
        print(f1(x[0]), f2(x[0]))

    f = lambda x: f1(x) + f2(x)
    alpha = -10
    beta = 10
    mut = GA.mutate_function(alpha, beta)
    x = GA.ga(f, mutation=mut, alpha=alpha, beta=beta, epoch=1000)
    print(x)
    print(f(x[0]))


if __name__ == '__main__':
    main()
