from sympy import *


def derivative(x):
    return 30 * x ** 5 - 36 * 5 * x ** 4 - 165 * 2 * x ** 3 - 180 * x ** 2


def function(x):
    return 5 * x ** 6 - 36 * x ** 5 - 165 * x ** 4 / 2 - 60 * x ** 3 + 36


def qubic_interpolation(s0, step, eps, delta, f, f_der):
    y_der_0 = f_der(s0)
    k = 0
    dir = -1 if y_der_0 > 0 else 1
    while True:
        s_n = s0 + dir * 2 ** k * step

        if f_der(s_n) * f_der(s0) <= 0:
            break

        k += 1
        s0 = s_n

    s1 = s0
    s2 = s_n

    while True:
        print(s1, s2)
        f1 = f(s1)
        fd1 = f_der(s1)
        f2 = f(s2)
        fd2 = f_der(s2)

        z = 3 * (f1 - f2) / (s2 - s1) + fd1 + fd2
        w = math.sqrt(z ** 2 - fd1 * fd2)
        w = -w if s1 > s2 else w
        mu = (fd2 + w - z) / (fd2 - fd1 + 2 * w)

        sapr = s2 if mu < 0 else s1 if mu > 1 else s2 - mu * (s2 - s1)

        if f(sapr) >= f(s1):
            while True:
                sapr = sapr - (sapr - s1) / 2
                if f(sapr) <= f(s1):
                    break

        if math.fabs(f_der(sapr)) <= eps and math.fabs((sapr - s1) / sapr) <= delta:
            return sapr

        s2 = s1 if f_der(sapr) * f_der(s1) < 0 else s2
        s1 = sapr


def quadric_interpolation(s1, step, eps, delta, f):
    def get_left_right(p, arr):
        left = max(filter(lambda a: p >= a, arr))
        right = min(filter(lambda a: p <= a, arr))
        return left, p, right

    s2 = s1 + step

    f1 = f(s1)
    f2 = f(s2)

    if f(s1) > f(s2):
        s3 = s1 + 2 * step
    else:
        s3 = s1 - step

    while True:
        f1 = f(s1)
        f2 = f(s2)
        f3 = f(s3)

        minf = min(f1, f2, f3)
        mins = s1 if minf == f1 else s2 if minf == f2 else s3

        try:
            aprs = ((s2 ** 2 - s3 ** 2) * f1 + (s3 ** 2 - s1 ** 2) * f2 + (s1 ** 2 - s2 ** 2) * f3) \
                   / (2 * ((s2 - s3) * f1 + (s3 - s1) * f2 + (s1 - s2) * f3))
        except ZeroDivisionError:
            return quadric_interpolation(mins, step, eps, delta, f)

        fapr = f(aprs)
        clause1 = math.fabs((minf - fapr) / fapr) < eps
        clause2 = math.fabs((mins - aprs) / aprs) < delta
        print(1, math.fabs((minf - fapr) / fapr))
        print(2, math.fabs((mins - aprs) / aprs))

        if clause1 and clause2:
            return aprs
        if s1 <= aprs <= s3:
            if fapr < minf:
                s1, s2, s3 = get_left_right(aprs, [s1, s2, s3, mins])
            else:
                s1, s2, s3 = get_left_right(mins, [s1, s2, s3, aprs])
        else:
            return quadric_interpolation(aprs, step, eps, delta, f)


def main():
    step = 0.00001
    eps = 0.000001
    x0 = 10
    target = 7.56001
    print(quadric_interpolation(x0, step, eps, eps, function))
    print(qubic_interpolation(x0, step, eps, eps, function, derivative))


if __name__ == "__main__":
    main()
