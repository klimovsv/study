def function(x):
    return 5 * x ** 6 - 36 * x ** 5 - 165 * x ** 4 / 2 - 60 * x ** 3 + 36


def get_start_interval(f, x0, t):
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
        print(x_next, f(x_next))
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


def bisection(interval, f, eps, k=0):
    a = interval[0]
    b = interval[1]
    x_mid = (a + b) / 2
    length = b - a

    if length <= eps:
        return x_mid

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


def main():
    print(bisection(get_start_interval(function, -13, 0.1), function, 0.001))


if __name__ == "__main__":
    main()
