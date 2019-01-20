from Matrix import *
import numpy as np
import math
import sys

# eps = 10 ** -1
iter = 15
eps = 0.01
eps_u = 0.01


def equals(a: float, b: float, eps):
    return math.fabs(a - b) <= eps


def step_outside(start, diag, p, u, depth):
    d = diag[0] if p > 0 else diag[len(diag) - 1]

    if depth == iter:
        return start

    if equals(start, d, eps):
        print("EQEQEQEQEQE")
        return start

    def f(l):
        res = 0
        for i in range(len(diag)):
            res += get_u(u, i) ** 2 / (diag[i] - l)
        return 1 + res * p

    def f_der(l):
        res = 0
        for i in range(len(diag)):
            res += get_u(u, i) ** 2 / ((diag[i] - l) ** 2)
        return res * p

    # c1+c2/(d-l) = f
    # c2/(d-l)^2 = f'

    # c2 = f'*(d-l)^2
    # c1 = f - f'*(d-l)
    c2 = f_der(start) * (d - start) ** 2
    c1 = f(start) - c2 / (d - start)

    next = (c2 / c1) + d

    # print("OUTSIDE ",start,next,d,p,c1,c2)
    # print(diag)
    return step_outside(next, diag, p, u, depth + 1)

    # c1 + c2/(d - l) = 0
    # c2/-c1 = d - l
    # l = c2/c1 + d


def step_inside(start, diag, p, u, depth):
    def phi(s, e, l):
        k = s
        res = 0
        while k <= e:
            res += get_u(u, k) ** 2 / (diag[k] - l)
            k += 1
        return res * p

    def phi_der(s, e, l):
        k = s
        res = 0
        while k <= e:
            res += get_u(u, k) ** 2 / ((diag[k] - l) ** 2)
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

        if equals(di, di_1, 2 * eps):
            next.append(l)
            continue
        elif equals(l, di_1, eps) or equals(l, di, eps):
            next.append(l)
            continue

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
        if di_1 < x1 < di:
            next.append(x1)
        elif di_1 < x2 < di:
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
    # u = [u.matr[i, 0] for i in range(u.matr.shape[0])]

    nu = [u.matr[i, 0] for i in range(u.matr.shape[0])]
    norm = sum(map(lambda a: a ** 2, nu))
    start = []
    for i in range(len(diag) - 1):
        start.append((diag[i] + diag[i + 1]) / 2)

    if p > 0:
        return [step_outside(diag[0] + 100, diag, p, u, 0)] + step_inside(start, diag, p, u, 0)
    else:
        return step_inside(start, diag, p, u, 0) + [step_outside(diag[len(diag) - 1] - 100, diag, p, u, 0)]


def get_j(i, lst):
    n = 0
    for j in range(len(lst)):
        for el in lst[j]:
            if n == i:
                return j
            n += 1


def generate_w(alphas, diag, p, l, k, groups_diag):
    length = len(diag)
    w = [None for i in range(length)]

    for i in range(length):
        j = get_j(i, groups_diag)
        kdj = len(groups_diag[j])
        if kdj == 1 and l[j] >= kdj:
            w[i] = 0
        elif l[j] > kdj - 1 > 0:
            w[i] = 0
        elif l[j] == kdj - 1 and kdj - 1 > 0:
            pass
        elif l[j] == 0 and kdj == 1:
            d = diag[i]
            top = 1

            bot = 1
            res = 1

            for n in range(length):
                if n != i:
                    res = res * (alphas[n] - d) / (diag[n] - d)

            res *= alphas[i] - d

            # for n in range(length):
            #     top = top * (alphas[n] - d)
            #
            # for n in range(length):
            #     if n != i:
            #         bot = bot * (diag[n] - d)

            if p < 0:
                # top = -top
                res = -res

            # w[i] = math.sqrt(top / bot)

            w[i] = math.sqrt(res)

    return w

def find_equals(alph, i,diag,p):
    lst = []
    if equals(alph, diag[i], eps):
        lst.append(i)
    if p > 0:
        if i > 0 and equals(alph, diag[i - 1], eps):
            lst.append(i - 1)
    else:
        if i < len(diag) - 1 and equals(alph, diag[i + 1], eps):
            lst.append(i + 1)
    return lst

def get_u(u, i):
    if equals(u.matr[i, 0], 0, eps_u):
        return 0
    else:
        return u.matr[i, 0]


def spectral(m: Matrix) -> [Matrix, Matrix]:
    if m.matr.shape[0] == m.matr.shape[1] == 1:
        return Matrix.from_const(1), m

    t1, t2, b, v = m.cut()
    q1, l1 = spectral(t1)
    q2, l2 = spectral(t2)

    D = Matrix.diagonaled(l1, l2)
    Q = Matrix.diagonaled(q1, q2)
    perm = D.sort()
    u = Q.transpose() * v

    # print(D)
    diag = perm * D * perm.transpose()
    # print(diag)
    u = perm * u

    n_diag = [diag.matr[i, i] for i in range(diag.matr.shape[0])]
    groups_diag = []
    i = 0
    while i < len(n_diag):
        el = n_diag[i]
        eq = [el]
        while i + 1 < len(n_diag) and equals(el, n_diag[i + 1], 2 * eps):
            eq.append(n_diag[i + 1])
            i += 1
        groups_diag.append(eq)
        i += 1

    # print(n_diag)
    # print(groups_diag)

    k = []
    i = 0
    for group in groups_diag:
        res = 0
        for d in group:
            res += get_u(u, i) ** 2
            i += 1
        k.append(res)

    # print(k)

    alphas = century_eq(diag, b, u)

    l = []

    def f(l):
        res = 0
        for i in range(len(n_diag)):
            res += get_u(u, i) ** 2 / (n_diag[i] - l)
        return 1 + res * b

    for i in range(len(groups_diag)):
        count = 0
        for alph in alphas:
            if equals(groups_diag[i][0], alph, eps):
                count += 1

        l.append(count)
        # if k[i] != 0:
        #     l.append(len(groups_diag[i]) - 1)
        # else:
        #     if equals(f(groups_diag[i][0]), 0, eps):
        #         l.append(len(groups_diag[i]) + 1)
        #     else:
        #         l.append(len(groups_diag[i]))

    diag = [diag.matr[i, i] for i in range(diag.matr.shape[0])]

    print("u ", u)
    print("k ", k)
    print("l ", l)
    print("d ", diag)
    print("alph ", alphas)
    print("perm ", perm)

    w = Matrix.vector(generate_w(alphas, diag, b, l, k, groups_diag))
    # print(l)
    # print(w)
    eign_matr = Matrix.zeros(len(alphas))
    E = Matrix.identity(len(alphas))

    for i in range(len(w.matr.reshape(-1))):
        sign_u = 1 if u.matr[i, 0] > 0 else -1
        sign_w = 1 if w.matr[i, 0] > 0 else -1
        if sign_u != sign_w:
            w.matr[i, 0] = -1 * w.matr[i, 0]


    p = b
    D = perm * D * perm.transpose()
    for i in range(len(alphas)):
        # j = get_j(i, groups_diag)
        # kij = len(groups_diag[j])
        alpha = alphas[i]
        eq_ind = find_equals(alpha, i,diag,p)

        if len(eq_ind) == 0:
            vec = []
            for j in range(D.matr.shape[0]):
                vec.append(w.matr[j, 0] / (D.matr[j, j] - alphas[i]))

            eign_matr.set_vector_eign(vec, i)
        else:
            j = get_j(eq_ind[0], groups_diag)
            kij = len(groups_diag[j])
            if l[j] == kij:
                n = eq_ind[0]
                eign_matr.set_vector(E.getCol(n), i)
            elif l[j] == kij + 1:
                dij = groups_diag[j][0]
                if equals(diag[i], dij, 2 * eps):

                    eign_matr.set_vector(E.getCol(i), i)
                else:
                    z = [None for i in range(alphas)]
                    for n in range(len(z)):
                        if equals(diag[n], dij, 2 * eps):
                            z[n] = 0
                        else:
                            z[n] = w.matr[n, 0] / (D.matr[n, n] - dij)
                    eign_matr.set_vector_eign(z, i)
            # elif l[j] == kij - 1:
            #     local_w = [None for i in range(alphas)]
            #     dij = groups_diag[j][0]
            #     for i in range(len(diag)):
            #         n_j = get_j(i,groups_diag)


        # if equals(alphas[i], diag[i], eps) and l[j] == kij:
        #     eign_matr.set_vector(E.getCol(i), i)
        # else:
        #     vec = []
        #     for j in range(D.matr.shape[0]):
        #         vec.append(w.matr[j, 0] / (D.matr[j, j] - alphas[i]))
        #
        #     eign_matr.set_vector_eign(vec, i)

    # for i in range(len(alphas)):
    #     print("norm ",np.linalg.norm(eign_matr.getCol(i)))

    # if equals(u.matr[i, 0], 0, eps):
    #     eign_matr.set_vector(E.getCol(i), i)

    L = Matrix.diag_from_vector(alphas)

    # print()
    #

    print(eign_matr)
    print(eign_matr * eign_matr.transpose())
    print(np.linalg.det((eign_matr * eign_matr.transpose()).matr))
    # print()

    # print("back ", Q * perm.transpose()*(perm * D * perm.transpose() + b*u*u.transpose()) * (Q*perm.transpose()).transpose())
    # print("back with eign ", Q * (eign_matr * perm) * (perm.transpose() * L * perm) * (Q * (eign_matr * perm)).transpose() )
    # print("L ",L)
    # print("QLQt ", (eign_matr * L * eign_matr.transpose()))
    # if m.matr.shape[0] == m.matr.shape[1] == 2:
    #     return Q * eign_matr, L
    return Q * perm.transpose() * eign_matr, L


t = np.array([
    [500, 200, 0, 0],
    [200, 400, 3, 0],
    [0, 3, 1000, 6],
    [0, 0, 6, 100]
], np.float)

x = np.array([[-34. , 43. ,  0. ,  0.  , 0. ,  0.],
 [ 43. , -4., -50. ,  0. ,  0. ,  0.],
 [  0., -50. , 20.  , 6.,   0.,   0.],
 [  0.  , 0. ,  6. ,-18.,  12. ,  0.],
 [  0. ,  0.  , 0. , 12.  ,-2.,  26.],
 [  0. ,  0. ,  0.  , 0.  ,26. , 38.]], np.float)


def own():
    tm = Matrix(x)
    Q, D = spectral(tm)

    print(tm)
    print(Q * D * Q.transpose())
    print()

    print(D)
    print(np.linalg.eig(t)[0])

    print(Q)
    print(np.linalg.eig(t)[1])


def generated():
    m = Matrix.generate(6)
    print(np.linalg.eig(m.matr)[0])
    Q, D = spectral(m)
    print(D)
    print(np.linalg.eig(m.matr)[0])
    print(Q * D * Q.transpose())
    print(m)

    diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    print(diag)
    print(np.linalg.eig(m.matr)[0])


sys.setrecursionlimit(10000)
generated()
# own()

x = [1, 20, 30, 10]
m = Matrix.diag_from_vector(x)

# perm = m.sort()
# d = perm * m * perm.transpose()
# l = perm.transpose() * d * perm
# print(d,l)
# print(d * perm)

# t = np.array([
#     [500, 200, 0, 0],
#     [200, 400, 3, 0],
#     [0, 3, 1000, 6],
#     [0, 0, 6, 100]
# ], np.float)
# tm = Matrix(t)
# perm = tm.sort()
# print(tm * perm)
