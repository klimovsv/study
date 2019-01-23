from Matrix import *
import numpy as np
import math
import sys
from scipy.linalg import hessenberg

# eps = 10 ** -1
iter = 10
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
        # elif equals(l, di_1, eps) or equals(l, di, eps):
        #     next.append(l)
        #     continue

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
        if di_1 < x1 < di and di_1 < x2 < di:
            x = min(x1, x2)
            next.append(x)
        elif di_1 < x1 < di:
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

    # print(diag)
    # print(alphas)
    for j in range(len(l)):
        if l[j] == 0:
            i = get_is(j, groups_diag)[0]
            print(i)
            top = 1
            bot = 1

            for alph in alphas:
                top *= alph - diag[i]

            for j in range(len(diag)):
                if j != i:
                    bot *= diag[j] - diag[i]

            # for d in diag:
            #     if not equals(d,diag[i],eps):
            #         bot *= d - diag[i]

            # print(top)
            # print(bot)
            if p < 0:
                bot = -bot
            w[i] = math.sqrt(top / bot)

    i = 0
    while i < length:
        # print(i)
        # j = get_j(i, groups_diag)
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
                # i -= 1
            if l[j] == len(groups_diag[j]):
                i_s = get_is(j, groups_diag)
                # print(i_s)
                count = 0
                for it in i_s:
                    w[it] = 0
                    eign_matr.set_vector(E.getCol(it), i + count)
                    count += 1
                # i -= 1

            if l[j] == len(groups_diag[j]) + 1:
                i_s = get_is(j, groups_diag)
                for it in i_s:
                    w[it] = 0
                    eign_matr.set_vector(E.getCol(it), it)
                    # i += 1
            i += l[j]
        # i += 1

    print("w ", w)
    print(eign_matr)
    for i in range(len(w)):
        sign_u = 1 if u.matr[i, 0] > 0 else -1
        sign_w = 1 if w[i] > 0 else -1
        if sign_u != sign_w:
            w[i] = -1 * w[i]

    i = 0
    # print(w)

    while i < length:
        alpha = alphas[i]
        eq_ind = find_equals(alpha, i, diag, p)

        # print("index ",i)
        # print(eq_ind)
        if len(eq_ind) == 0:
            vec = []
            # print("index ",i)
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

    # if b < 0:
    #     n_diag = list(reversed(n_diag))

    i = 0
    while i < len(n_diag):
        el = n_diag[i]
        eq = [el]
        while i + 1 < len(n_diag) and equals(el, n_diag[i + 1], 2 * eps):
            eq.append(n_diag[i + 1])
            i += 1
        groups_diag.append(eq)
        i += 1

    # if b < 0:
    #     n_diag = list(reversed(n_diag))
    #     groups_diag = list(reversed(groups_diag))

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
    print("p ",b)
    print("k ", k)
    print("l ", l)
    print("d ", diag)
    print("alph ", alphas)
    # print("perm ", perm)

    w, eign_matr = generate_w_and_eign(alphas, diag, b, l, u, groups_diag)

    # print("w",w.matr.reshape(-1))
    # w = Matrix.vector(w)
    # print(l)
    # print(w)
    # eign_matr = Matrix.zeros(len(alphas))
    # E = Matrix.identity(len(alphas))

    # for i in range(len(w.matr.reshape(-1))):
    #     sign_u = 1 if u.matr[i, 0] > 0 else -1
    #     sign_w = 1 if w.matr[i, 0] > 0 else -1
    #     if sign_u != sign_w:
    #         w.matr[i, 0] = -1 * w.matr[i, 0]

    # p = b
    # D = perm * D * perm.transpose()
    # for i in range(len(alphas)):
    #     # j = get_j(i, groups_diag)
    #     # kij = len(groups_diag[j])
    #     alpha = alphas[i]
    #     eq_ind = find_equals(alpha, i, diag, p)
    #
    #     if len(eq_ind) == 0:
    #         vec = []
    #         for j in range(D.matr.shape[0]):
    #             vec.append(w.matr[j, 0] / (D.matr[j, j] - alphas[i]))
    #
    #         eign_matr.set_vector_eign(vec, i)
    #     else:
    #         j = get_j(eq_ind[0], groups_diag)
    #         kij = len(groups_diag[j])
    #         if l[j] == kij:
    #             n = eq_ind[0]
    #             eign_matr.set_vector(E.getCol(n), i)
    #         elif l[j] == kij + 1:
    #             dij = groups_diag[j][0]
    #             if equals(diag[i], dij, 2 * eps):
    #
    #                 eign_matr.set_vector(E.getCol(i), i)
    #             else:
    #                 z = [None for i in range(alphas)]
    #                 for n in range(len(z)):
    #                     if equals(diag[n], dij, 2 * eps):
    #                         z[n] = 0
    #                     else:
    #                         z[n] = w.matr[n, 0] / (D.matr[n, n] - dij)
    #                 eign_matr.set_vector_eign(z, i)
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


def vector_diff(a,b):
    n = []
    for i in range(len(a)):
        n.append(math.fabs(a[i]-b[i]))
    return max(n) , min(n) , sum(n)/len(n)

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
    n=10
    m = Matrix.generate(n)
    # m = Matrix.generate_hilbert(5)
    # m = Matrix.generate_wilk(n)
    print(np.linalg.eig(m.matr)[0])
    print(m)
    Q, D = spectral(m)
    # print(list(reversed(sorted(D.matr.reshape(-1)))))
    # print(list(reversed(sorted(np.linalg.eig(m.matr)[0]))))
    print(Q * D * Q.transpose())
    print(m)

    diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    diag = list(reversed(sorted(diag)))
    np_diag = list(reversed(sorted(np.linalg.eig(m.matr)[0])))


    m.change(0.001)
    Q, D = spectral(m)
    new_diag = [D.matr[i, i] for i in range(D.matr.shape[0])]
    new_diag = list(reversed(sorted(new_diag)))
    print(diag)
    print(np_diag)
    print(new_diag)
    print(vector_diff(diag,new_diag))
    # print(vector_diff(diag,np_diag))
    # print(np.linalg.det((Q * Q.transpose() - Matrix.identity(n)).matr))


sys.setrecursionlimit(10000)
generated()
# owns()

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
