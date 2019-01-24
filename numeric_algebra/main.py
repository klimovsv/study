from Matrix import *
import numpy as np
import math
import sys
from statistics import median, mean , pstdev

# eps = 10 ** -1
iter = 10
eps_all = 10 ** -5
eps = eps_all
eps_u = eps_all


def equals(a: float, b: float, eps):
    return math.fabs(a - b) <= eps


def step_outside(start, diag, p, u, depth,group):
    d = diag[0] if p > 0 else diag[len(diag) - 1]

    if depth == iter:
        return start

    if equals(start, d, eps):
        # print("EQEQEQEQEQE")
        return start

    def f(l):
        res = 0
        for i in range(len(diag)):
            j = get_j(i, group)
            d = group[j][0]
            res += get_u(u, i) ** 2 / (d - l)
        return 1 + res * p

    def f_der(l):
        res = 0
        for i in range(len(diag)):
            j = get_j(i, group)
            d = group[j][0]
            res += get_u(u, i) ** 2 / ((d - l) ** 2)
        return res * p

    c2 = f_der(start) * (d - start) ** 2
    c1 = f(start) - c2 / (d - start)

    next = (c2 / c1) + d

    return step_outside(next, diag, p, u, depth + 1,group)


def step_inside(start, diag, p, u, depth,group):
    def phi(s, e, l):
        k = s
        res = 0
        while k <= e:
            j = get_j(k, group)
            d = group[j][0]
            res += get_u(u, k) ** 2 / (d - l)
            k += 1
        return res * p

    def phi_der(s, e, l):
        k = s
        res = 0
        while k <= e:
            j = get_j(k, group)
            d = group[j][0]
            res += get_u(u, k) ** 2 / ((d - l) ** 2)
            k += 1
        return res * p

    if depth == iter:
        return start

    next = []

    for i in range(len(start)):
        l = start[i]
        di = diag[i]
        di_1 = diag[i + 1]

        if equals(di, di_1, 2 * eps):
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
        if di_1 < x1 < di and di_1 < x2 < di:
            # dix1 = math.fabs(x1-di_1)
            # dix2 = math.fabs(x2-di_1)
            if p > 0:
                x = min(x1, x2)
            else:
                x = max(x1, x2)
            next.append(x)
        elif di_1 < x1 < di:
            next.append(x1)
        elif di_1 < x2 < di:
            next.append(x2)
        else:
            next.append(l)

    return step_inside(next, diag, p, u, depth + 1,group)


def century_eq(D, p, u,group):
    diag = [D.matr[i, i] for i in range(D.matr.shape[0])]

    start = []
    for i in range(len(diag) - 1):
        start.append((diag[i] + diag[i + 1]) / 2)

    if p > 0:
        return [step_outside(diag[0] + 100, diag, p, u, 0,group)] + step_inside(start, diag, p, u, 0,group)
    else:
        return step_inside(start, diag, p, u, 0,group) + [step_outside(diag[len(diag) - 1] - 100, diag, p, u, 0,group)]


def get_j(i, lst):
    n = 0
    for j in range(len(lst)):
        for el in lst[j]:
            if n == i:
                return j
            n += 1


def get_is(j, group):
    n = 0
    count = 0
    while n < j:
        count += len(group[n])
        n += 1
    return [(i + count) for i in range(len(group[j]))]


def generate_w_and_eign(alphas, diag, p, l, u, groups_diag):
    length = len(diag)
    w = [None for i in range(length)]
    eign_matr = Matrix.zeros(len(alphas))
    E = Matrix.identity(len(alphas))

    for j in range(len(l)):
        if l[j] == 0:
            i = get_is(j, groups_diag)[0]
            # print(i)
            top = 1
            bot = 1

            for alph in alphas:
                top *= alph - diag[i]

            for j in range(len(diag)):
                if j != i:
                    bot *= diag[j] - diag[i]
            if p < 0:
                bot = -bot
            w[i] = math.sqrt(top / bot)

    i = 0
    while i < length:
        alpha = alphas[i]
        eq_ind = find_equals(alpha, i, diag, p)

        if len(eq_ind) == 0:
            i+=1
        else:
            eq_ind = eq_ind[0]
            j = get_j(eq_ind, groups_diag)
            if l[j] == len(groups_diag[j]) - 1:
                i_s = get_is(j, groups_diag)
                ij = i_s[0] if p > 0 else i_s[len(i_s) - 1]
                for it in i_s:
                    if it != ij:
                        w[it] = 0
                        eign_matr.set_vector(E.getCol(it), i)
                    else:
                        dij = diag[ij]
                        top = 1
                        bot = 1
                        for alph in alphas:
                            if not equals(alph, dij, eps):
                                top *= alph - dij
                        for d in diag:
                            if not equals(d, dij, 2 * eps):
                                bot *= d - dij
                        if p < 0:
                            top = -top
                        w[ij] = math.sqrt(top / bot)
            if l[j] == len(groups_diag[j]):
                i_s = get_is(j, groups_diag)
                count = 0
                for it in i_s:
                    w[it] = 0
                    eign_matr.set_vector(E.getCol(it), i + count)
                    count += 1

            if l[j] == len(groups_diag[j]) + 1:
                i_s = get_is(j, groups_diag)
                for it in i_s:
                    w[it] = 0
                    eign_matr.set_vector(E.getCol(it), it)
                    # i += 1
            i += l[j]
        # i += 1

    # print("w ", w)
    # print(eign_matr)
    for i in range(len(w)):
        sign_u = 1 if u.matr[i, 0] > 0 else -1
        sign_w = 1 if w[i] > 0 else -1
        if sign_u != sign_w:
            w[i] = -1 * w[i]

    i = 0

    while i < length:
        alpha = alphas[i]
        eq_ind = find_equals(alpha, i, diag, p)

        if len(eq_ind) == 0:
            vec = []
            for j in range(len(diag)):
                vec.append(w[j] / (diag[j] - alpha))
            eign_matr.set_vector_eign(vec, i)
        else:
            eq_ind = eq_ind[0]
            j = get_j(eq_ind, groups_diag)
            if l[j] == len(groups_diag[j]) + 1:
                i_s = get_is(j, groups_diag)
                vec_ind = i + len(i_s) if p > 0 else i
                i += len(i_s)
                z = [0 for i in range(length)]
                ij = i_s[0] if p > 0 else i_s[len(i_s) - 1]
                dij = diag[ij]
                for n in range(length):
                    if not (n in i_s):
                        z[n] = w[n] / (diag[n] - dij)
                eign_matr.set_vector_eign(z, vec_ind)
        i += 1

    return Matrix.vector(w), eign_matr


def find_equals(alph, i, diag, p):
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

    diag = perm * D * perm.transpose()
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

    k = []
    i = 0
    for group in groups_diag:
        res = 0
        for d in group:
            res += get_u(u, i) ** 2
            i += 1
        k.append(res)

    alphas = century_eq(diag, b, u, groups_diag)

    l = []

    for i in range(len(groups_diag)):
        count = 0
        for alph in alphas:
            if equals(groups_diag[i][0], alph, eps):
                count += 1

        l.append(count)

    diag = [diag.matr[i, i] for i in range(diag.matr.shape[0])]
    w, eign_matr = generate_w_and_eign(alphas, diag, b, l, u, groups_diag)
    L = Matrix.diag_from_vector(alphas)

    return Q * perm.transpose() * eign_matr, L


def vector_diff(a,b):
    n = []
    for i in range(len(a)):
        n.append(math.fabs(a[i]-b[i]))
    return {"max":max(n) ,"min": min(n) , "avg":mean(n) , "median" : median(n) , "deviation" : pstdev(n)}

t = np.array([
    [500, 200, 0, 0],
    [200, 400, 3, 0],
    [0, 3, 1000, 6],
    [0, 0, 6, 100]
], np.float)

x = np.array([[-14., 9., 0.],
              [9., -34., -45.],
              [0., -45., 30.]], np.float)


def own():
    tm = Matrix(x)
    Q, D = spectral(tm)

    print(tm)
    print(Q * D * Q.transpose())
    print()

    print(D)
    print(np.linalg.eig(t)[0])

    # print(Q)
    # print(np.linalg.eig(t)[1])


def generated():
    n = 21
    # m = Matrix.generate(n)
    # m = Matrix.generate_hilbert(5)
    m = Matrix.generate_wilk(n)
    x = Matrix.generate_wilk(n)
    # x.change(0.01)
    print(np.linalg.eig(m.matr)[0])
    print(m)
    Q, D = spectral(x)
    # print(list(reversed(sorted(D.matr.reshape(-1)))))
    # print(list(reversed(sorted(np.linalg.eig(m.matr)[0]))))
    print(Q * D * Q.transpose())
    print(m)

    diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    diag = list(reversed(sorted(diag)))
    np_diag = list(reversed(sorted(np.linalg.eig(m.matr)[0])))


    # m.change(0.001)
    # Q, D = spectral(m)
    # new_diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    # new_diag = list(reversed(sorted(new_diag)))
    print(diag)
    print(np_diag)
    # print(new_diag)
    # print(vector_diff(diag,new_diag))
    print(vector_diff(diag, np_diag))
    # print(np.linalg.det((Q * Q.transpose() - Matrix.identity(n)).matr))


sys.setrecursionlimit(10000)
# generated()
# own()

x = [1, 20, 30, 10]
m = Matrix.diag_from_vector(x)

def test():
    diag = [46.72498073958795, 45.84971769034255, 14.275019260412048, -33.84971769034256]
    l = [0, 1, 2, 1]
    p = -1
    group = [[46.72498073958795], [45.84971769034255], [14.275019260412048], [-33.84971769034256]]
    u = Matrix(np.array([[-0.95709203],
                         [0.80657652],
                         [0.28978415],
                         [0.59112969]]))
    alphas = [45.84971769034322, 14.275019260412051, 14.275019260412046, -33.84971769034256]
    # generate_w(alphas, diag, p, l, None, group)

    w, eign = generate_w_and_eign(alphas, diag, p, l, u, group)
    # w = Matrix.vector(w)
    print(eign)
    print(eign * eign.transpose())
    print(w)

    # w = np.array([[30,40,50],
    #               [2,99,77],
    #               [3,45,38]])
    # print(hessenberg(hessenberg(w).transpose()))

# test()