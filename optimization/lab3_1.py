import math


def function(x):
    return 5 * x ** 6 - 36 * x ** 5 - 165 * x ** 4 / 2 - 60 * x ** 3 + 36


def get_start_interval(f, x0, t=0.001):
    y1, y2, y3 = f(x0 - t), f(x0), f(x0 + t)

    if y1 >= y2 and y2 <= y3:
        return [y1, y3]
    elif y1 <= y2 and y2 >= y3:
        raise Exception("не унимодальная, выберите новую начальную точку")

    delta = None
    a0 = None
    x_start = None
    k = 1
    b0 = None
    if y1 >= y2 >= y3:
        delta = t
        a0 = x0
        x_start = x0 + t
    elif y1 <= y2 <= y3:
        delta = -t
        b0 = x0
        x_start = x0 - t

    while True:
        x_next = x_start + 2 ** k * delta

        if f(x_next) < f(x_start):
            if delta == -t:
                b0 = x_start
            elif delta == t:
                a0 = x_start
            k += 1
        else:
            break

        x_start = x_next

    if delta == -t:
        a0 = x_next
    else:
        b0 = x_next
    return [a0, b0]


def bisection(interval, f, eps, k=1):
    a = interval[0]
    b = interval[1]
    x_mid = (a + b) / 2
    length = b - a

    if length <= eps:
        return x_mid, k

    y_mid = f(x_mid)
    y = a + length / 4
    z = b - length / 4
    fy = f(y)
    fz = f(z)

    if fy < y_mid:
        return bisection([a, x_mid], f, eps, k + 1)
    if fz < y_mid:
        return bisection([x_mid, b], f, eps, k + 1)
    else:
        return bisection([y, z], f, eps, k + 1)


def golden(interval, f, eps=10**-8, k=1):
    a, b = interval[0], interval[1]

    if (b - a) <= eps:
        return (a + b) / 2, k

    y = a + (3 - math.sqrt(5)) * (b - a) / 2
    z = a + b - y
    fy, fz = f(y), f(z)

    if fy <= fz:
        return golden([a, z], f, eps, k + 1)
    elif fy > fz:
        return golden([y, b], f, eps, k + 1)


def memoized(f):
    d = {}

    def memoized_f(x):
        if x not in d:
            d[x] = f(x)
        return d[x]

    return memoized_f


@memoized
def fib(n):
    return 1 if n < 2 else fib(n - 1) + fib(n - 2)


def get_n(l, eps):
    n = 0
    while fib(n) <= l / eps:
        n += 1
    return n


def fib_method(interval, f, eps, k=0):
    a, b = interval[0], interval[1]
    N = get_n(b - a, eps)

    y_s = a + (b - a) * fib(N - 2) / fib(N)
    z_s = a + (b - a) * fib(N - 1) / fib(N)
    y_n = None
    z_n = None

    if k > N - 3:
        return (a + b) / 2

    while True:
        if f(y_s) <= f(z_s):
            b = z_s
            z_n = y_s
            y_n = a + (b - a) * fib(N - k - 3) / fib(N - k - 1)
        else:
            a = y_s
            y_n = z_s
            z_n = a + (b - a) * fib(N - k - 2) / fib(N - k - 1)

        if k != N - 3:
            y_s = y_n
            z_s = z_n
            k += 1
        else:
            y_n1 = z_n
            z_n1 = y_n1 + eps
            if f(y_n1) <= f(z_n1):
                b = z_n1
            else:
                a = y_n1
            return (a + b) / 2, k


def main():
    step = 0.0001
    eps = 0.00001
    x0 = -13
    target = 7.56001
    # target = 2 + math.pow(596 - 3*math.sqrt(2703), 1/3)/3 +  math.pow(198 + math.sqrt(2703), 1/3)/ math.pow(3,2/3)
    interval = get_start_interval(function, x0, step)
    bis = bisection(interval, function, eps)
    gol = golden(interval, function, eps)
    fibbon = fib_method(interval, function, eps)
    print(x0, interval)
    print(math.fabs(bis[0] - target), "bisection", bis[1], bis[0], function(bis[0]))
    print(math.fabs(gol[0] - target), "gold", gol[1], gol[0], function(gol[0]))
    print(math.fabs(fibbon[0] - target), "fib", fibbon[1], fibbon[0], function(fibbon[0]))


if __name__ == "__main__":
    main()
