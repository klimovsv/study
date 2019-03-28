import numpy
import math
import lab3_1
import scipy.optimize


def rosenbrock(a, b, f0):
    def f(x):
        res = 0
        for i in range(len(x) - 1):
            res += a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2
        return res + f0

    return f


def prime_rosenbrock(a, b, f0):
    def f(x):
        n = len(x) - 1
        grad_arr = []
        for i in range(1, len(x) - 1):
            grad_arr.append(
                -2 * a * (x[i - 1] ** 2 - x[i]) + 2 * a * 2 * x[i] * (x[i] ** 2 - x[i + 1]) + 2 * b * (x[i] - 1))

        return numpy.array([2 * a * 2 * x[0] * (x[0] ** 2 - x[1]) + 2 * b * (x[0] - 1)] +
                           grad_arr +
                           [-2 * a * (x[n - 1] ** 2 - x[n])])
    return f


def fletcher_reevs(f, grad, x0, e1=0.00001, e2=0.00001, delta=0.00001, max_iters=1000):
    k = 0
    x = [x0]
    gr = grad(x[0])
    w = []
    d = [-gr]

    while True:
        if numpy.linalg.norm(grad(x[k])) < e1 or k >= max_iters:
            return x[k]

        new_f = lambda t: f(x[k] + t*d[k])
        interval = lab3_1.get_start_interval(new_f, 0, 0.00001)
        alpha = lab3_1.golden(interval, new_f, 0.00001)[0]
        x.append(x[k] + alpha*d[k])
        if numpy.linalg.norm(x[k+1]-x[k]) < delta and abs(f(x[k+1])-f(x[k])) < e2:
            return x[k+1]
        k += 1
        w.append((numpy.linalg.norm(grad(x[k])))**2/(numpy.linalg.norm(grad(x[k-1])))**2)
        d.append(-grad(x[k]) + w[k-1]*d[k-1])



def main():
    print(fletcher_reevs(rosenbrock(30,2,80),
                         prime_rosenbrock(30,2,80),
                         [2, 2, 2, 2],
                         ))

if __name__ == "__main__":
    main()