import GA
import lab5
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


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

    fs = [f1, f2]
    f1s = []
    f2s = []
    n = 50
    for i in range(1, n):
        w = [i/n, 1 - i/n]
        new_f = lambda x: sum([w[j] * (fs[j](x) - f_star[j]) for j in range(len(w))])
        x = lab5.barier_functions(x0, func=new_f, cons=constraints())[0]
        f1s.append(f1(x))
        f2s.append(f2(x))

    plt.scatter(f1s, f2s, color='lightblue', linewidth=3)
    plt.show()


if __name__ == '__main__':
    main()
