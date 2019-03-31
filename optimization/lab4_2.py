import numpy
import math
import sympy
import lab3_1
import scipy.optimize


def rosenbrock_func(n):
    x = []
    for i in range(n):
        x.append(sympy.Symbol('x' + str(i)))

    a_s = sympy.Symbol('a')
    b_s = sympy.Symbol('b')
    f_s = sympy.Symbol('f')

    sum = f_s
    for i in range(n - 1):
        sum += a_s * (x[i] ** 2 - x[i + 1]) ** 2 + b_s * (x[i] - 1) ** 2
    return sum


def hessian(a, b):
    def f(x):
        x0, x1, x2, x3 = x
        return numpy.array([[4 * a * (x0 ** 2 - x1) + 8 * a * x0 ** 2 + 2 * b, -4 * a * x0, 0, 0],
                            [-4 * a * x0, 4 * a * (x1 ** 2 - x2) + 8 * a * x1 ** 2 + 2 * b + 2 * a, -4 * a * x1, 0],
                            [0, -4 * a * x1, 4 * a * (x2 ** 2 - x3) + 8 * a * x2 ** 2 + 2 * b + 2 * a, -4 * a * x2],
                            [0, 0, -4 * a * x2, 2 * a]])

    return f


def rosenbrock(a, b, f0):
    def f(x):
        sum = f0
        for i in range(len(x) - 1):
            sum += a * (x[i] ** 2 - x[i + 1]) ** 2 + b * (x[i] - 1) ** 2
        return sum

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


def grad_descent(f, grad, x0, e1=0.00001, e2=0.00001, cons=None):
    x = [x0]
    i = 0
    while True:
        dir = -grad(x[i])

        vec_f = lambda t: x[i] + t * dir
        new_f = lambda t: f(vec_f(t))

        interval = lab3_1.get_start_interval(new_f, 0, 10**-2, cons, vec_f)
        alpha = lab3_1.golden(interval, new_f, e1)[0]
        # alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x

        x.append(x[i] + alpha * dir)
        if numpy.linalg.norm(grad(x[i])) < e1 and abs(f(x[i + 1]) - f(x[i])) < e2:
            return x[i + 1]

        i += 1


def fletcher_powell(f, grad, x0, e1=0.00001, e2=0.00001, delta=0.000001, max_iters=100000):
    x = [x0]
    i = 0
    A = [numpy.eye(len(x0))]
    dir = [-grad(x0)]

    new_f = lambda t: f(x[i] + t * dir[i])
    alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x
    x.append(x[i] + alpha * dir[i])
    while i < max_iters:
        dx = numpy.array([x[i + 1] - x[i]])
        dg = numpy.array([grad(x[i + 1]) - grad(x[i])])
        A.append(A[i] +
                 numpy.matmul(dx.transpose(), dx) / (numpy.matmul(dx, dg.transpose())) -
                 numpy.matmul(numpy.matmul(A[i], dg.transpose()), numpy.matmul(dg, A[i])) / (
                     numpy.matmul(dg, numpy.matmul(A[i], dg.transpose()))))

        dir.append(numpy.matmul(-A[i + 1], numpy.array([grad(x[i + 1])]).transpose()).transpose()[0])

        new_f = lambda t: f(x[i + 1] + t * dir[i + 1])
        alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x
        x.append(x[i + 1] + alpha * dir[i + 1])

        if numpy.linalg.norm(grad(x[i + 1])) < e1 and abs(f(x[i + 2]) - f(x[i + 1])) < e2:
            return x[i + 2]

        i += 1

    return x[-1]


def fletcher_reevs(f, grad, x0, e1=0.00001, e2=0.00001, delta=0.00001, max_iters=100000):
    x = [x0]
    i = 0
    dir = [-grad(x0)]

    new_f = lambda t: f(x[i] + t * dir[i])
    alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x
    x.append(x[i] + alpha * dir[i])
    while True:
        dir.append(
            -grad(x[i + 1]) + (numpy.linalg.norm(grad(x[i + 1]))) ** 2 / (numpy.linalg.norm(grad(x[i]))) ** 2 * dir[i])

        new_f = lambda t: f(x[i + 1] + t * dir[i + 1])
        alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x
        x.append(x[i + 1] + alpha * dir[i + 1])

        if numpy.linalg.norm(grad(x[i + 1])) < e1 and abs(f(x[i + 2]) - f(x[i + 1])) < e2:
            return x[i + 2]

        i += 1


def levenberg_marquardt(f, grad, hessian, x0, e1=0.00001, e2=0.00001, max_iters=100000):
    x = [x0]
    l = 2
    i = 0
    while True:
        gi = grad(x[i])
        hi = hessian(x[i])
        dir = numpy.matmul(-numpy.linalg.inv(hi + l * numpy.eye(len(x0))), numpy.array([gi]).transpose()).transpose()[0]

        new_f = lambda t: f(x[i] + t * dir)
        alpha = scipy.optimize.minimize_scalar(new_f, method='Golden').x
        x.append(x[i] + alpha * dir)

        if f(x[i + 1]) < f(x[i]):
            l = l / 2
        else:
            l = 2 * l

        if numpy.linalg.norm(grad(x[i])) < e2 and abs(f(x[i + 1]) - f(x[i])) < e1:
            return x[i + 1]
        i += 1


def main():
    func = rosenbrock(30, 2, 80)
    print(rosenbrock_func(4))
    # print(func([1, 1]))
    print(grad_descent(rosenbrock(30, 2, 80),
                       prime_rosenbrock(30, 2),
                       numpy.array([3, 2, 3, 2]),
                       ))
    print(fletcher_reevs(rosenbrock(30, 2, 80),
                         prime_rosenbrock(30, 2),
                         numpy.array([3, 2, 3, 2]),
                         ))
    print(fletcher_powell(rosenbrock(30, 2, 80),
                          prime_rosenbrock(30, 2),
                          numpy.array([3, 2, 3, 2]),
                          ))
    print(levenberg_marquardt(rosenbrock(30, 2, 80),
                              prime_rosenbrock(30, 2),
                              hessian(30, 2),
                              numpy.array([3, 2, 3, 2]),
                              ))


if __name__ == "__main__":
    main()
