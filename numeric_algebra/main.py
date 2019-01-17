from Matrix import *
import numpy as np
import math
import sys
e = 10 ** -1
iter = 15


def equals(a: float, b: float):
    return math.fabs(a - b) <= e


def step_outside(start, diag, p, u, depth):
    if depth == iter:
        return start

    def f(l):
        res = 0
        for i in range(len(diag)):
            res += u[i] ** 2 / (diag[i] - l)
        return 1 + res * p

    def f_der(l):
        res = 0
        for i in range(len(diag)):
            res += u[i] ** 2 / (diag[i] - l) ** 2
        return res * p

    d = diag[0] if p > 0 else diag[len(diag) - 1]

    # c1+c2/(d-l) = f
    # c2/(d-l)^2 = f'

    # c2 = f'*(d-l)^2
    # c1 = f - f'*(d-l)
    c1 = f(start) - f_der(start) * (d - start)
    c2 = f_der(start) * (d - start) ** 2

    next = c2 / c1 + d

    return step_outside(next, diag, p, u, depth + 1)

    # c1 + c2/(d - l) = 0
    # c2/-c1 = d - l
    # l = c2/c1 + d


def step_inside(start, diag, p, u, depth):
    def phi(s, e, l):
        k = s
        res = 0
        while k <= e:
            res += u[k] ** 2 / (diag[k] - l)
            k += 1
        return res * p

    def phi_der(s, e, l):
        k = s
        res = 0
        while k <= e:
            res += u[k] ** 2 / ((diag[k] - l) ** 2)
            k += 1
        return res * p

    if depth == iter:
        return start

    next = []
    # что делать при одинаковости di
    for i in range(len(start)):
        l = start[i]
        di = diag[i]
        di_1 = diag[i + 1]

        c1 = phi_der(0, i, l) * ((di - l) ** 2)
        c1_ = phi(0, i, l) - phi_der(0, i, l) * (di - l)
        c2 = phi_der(i + 1, len(start), l) * ((di_1 - l) ** 2)
        c2_ = phi(i + 1, len(start), l) - phi_der(i + 1, len(start), l) * (di_1 - l)
        c3 = 1 + c1_ + c2_

        a = c3
        b = -((di + di_1) * c3 + c1 + c2)
        c = (c3 * di * di_1 + c1 * di_1 + c2 * di)
        discr = math.sqrt(b ** 2 - 4 * a * c)
        x1 = (-b + discr) / (2 * a)
        x2 = (-b - discr) / (2 * a)
        # print(x1, x2)
        if di_1 <= x1 <= di:
            next.append(x1)
        elif di_1 <= x2 <= di:
            next.append(x2)
        else:
            next.append(l)
    # c3(di*di1 - l(di+di1) +l^2) + c1(di1 - l ) + c2(di-l)=0
    # c3 l^2 - l ( (di+di1)c3 + c1 + c2) c3didi1 + c1di1 + c2di = 0
    # discr = sqrt ( ( (di+di1)c3 + c1 + c2)^2 -4c3*(c3didi1 + c1di1 + c2di))
    # x1 = (- ( (di+di1)c3 + c1 + c2) +- discr)/2c3

    return step_inside(next, diag, p, u, depth + 1)


def century_eq(D, p, u):
    diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    u = [u.matr[i, 0] for i in range(u.matr.shape[0])]

    if p < 0:
        print("ALERT")

    start = []
    for i in range(len(diag) - 1):
        start.append((diag[i] + diag[i + 1]) / 2)

    if p > 0:
        return [step_outside(diag[0] + 1, diag, p, u, 0)] + step_inside(start, diag, p, u, 0)
    else:
        return step_inside(start, diag, p, u, 0) + [step_outside(diag[len(diag) - 1] - 1, diag, p, u, 0)]


def generate_w(alphas, diag, p):
    length = len(diag)
    w = [None for i in range(length)]

    for i in range(length):
        d = diag[i]
        top = 1

        bot = 1

        for j in range(length):
            top = top * (alphas[j] - d)

        for j in range(length):
            if j != i:
                bot = bot * (diag[j] - d)

        w[i] = math.sqrt(top / bot)

    return w


def spectral(m: Matrix) -> [Matrix, Matrix]:
    if m.matr.shape[0] == m.matr.shape[1] == 1:
        return Matrix.from_const(1), m

    t1, t2, b, v = m.cut()
    q1, l1 = spectral(t1)
    q2, l2 = spectral(t2)

    D = Matrix.diagonaled(l1, l2)
    Q = Matrix.diagonaled(q1, q2)
    u = Q.transpose() * v
    perm = D.sort()

    diag = perm * D * perm.transpose()
    # print(diag)
    alphas = century_eq(perm * D * perm.transpose(), b, perm * u)

    diag = [diag.matr[i, i] for i in range(diag.matr.shape[0])]

    w = Matrix.vector(generate_w(alphas, diag, b))
    eign_matr = Matrix.zeros(len(alphas))
    E = Matrix.identity(len(alphas))

    for i in range(len(w.matr.reshape(-1))):
        sign_u = 1 if u.matr[i, 0] > 0 else -1
        sign_w = 1 if w.matr[i, 0] > 0 else -1
        if sign_u != sign_w:
            w.matr[i, 0] = -1 * w.matr[i, 0]

    for i in range(len(alphas)):
        vec = []
        for j in range(D.matr.shape[0]):
            vec.append(w.matr[j, 0] / (D.matr[j, j] - alphas[i]))

        # max = vec[0]
        # ind = 0
        # for i in range(len(vec)):
        #     if vec[i] > max:
        #         ind = i
        #         max = vec[i]
        #
        # factor = (D.matr[ind, ind] - alphas[i])
        #
        # vec = []
        # for j in range(D.matr.shape[0]):
        #     vec.append(factor * w.matr[j, 0] / (D.matr[j, j] - alphas[i]))

        eign_matr.set_vector_eign(vec, i)

        if equals(u.matr[i, 0], 0):
            eign_matr.set_vector(E.getCol(i) , i)

    L = Matrix.diag_from_vector(alphas)

    print()
    print("d ", diag)
    print("alph ", alphas)
    print(eign_matr)
    print(eign_matr * eign_matr.transpose())
    print(np.linalg.det((eign_matr * eign_matr.transpose()).matr))
    print()
    return Q * eign_matr, L


t = np.array([
    [500, 200, 0, 0],
    [200, 400, 3, 0],
    [0, 3, 1000, 6],
    [0, 0, 6, 100]
], np.float)


def own():
    tm = Matrix(t)
    Q, D = spectral(tm)

    print(tm)
    print(Q * D * Q.transpose())
    print()

    print(D)
    print(np.linalg.eig(t)[0])

    print(Q)
    print(np.linalg.eig(t)[1])


def generated():
    m = Matrix.generate(3)
    Q, D = spectral(m)
    print(D)
    print(np.linalg.eig(m.matr)[0])
    print(Q * D * Q.transpose())
    print(m)

sys.setrecursionlimit(10000)
generated()
# own()
