import numpy as np
import operator


def simplex(A, c, b, b_idx, eps=10 ** -3):
    if b_idx is None:
        return None, None
    k = 0
    max_iters = A.shape[0] * 5
    n_idx = [i for i in range(A.shape[1]) if i not in b_idx]

    def get_cb():
        return c[:, b_idx]

    def get_cn():
        return c[:, n_idx]

    def get_B():
        return A[:, b_idx]

    def get_N():
        return A[:, n_idx]

    while k <= max_iters:
        k += 1
        Binv = np.linalg.inv(get_B())
        N = get_N()

        xb = np.matmul(Binv, b).reshape(-1)

        cb = get_cb()
        cn = get_cn()

        gamma = cb @ Binv
        z = gamma @ N
        d = z - cn
        mind = min([(i, v) for i, v in enumerate(d[0].tolist())], key=operator.itemgetter(1))
        q_ind = mind[0]
        q = n_idx[q_ind]
        mind = mind[1]

        if mind >= eps and np.min(xb) >= 0:
            x = np.zeros(A.shape[1])
            x[b_idx] = xb.reshape(-1)
            return x, k

        alphq = (Binv @ A[:, q]).reshape(-1)
        beta = xb.reshape(-1)
        filtered = list(filter(lambda x: x[1][1] > 0, [(i, v) for i, v in enumerate(zip(beta, alphq))]))

        if len(filtered) == 0:
            return None, None

        p_ind = min(filtered, key=lambda v: v[1][0] / v[1][1])[0]
        p = b_idx[p_ind]

        b_idx[p_ind] = q
        n_idx[q_ind] = p
    return None, None


def get_basis(A, c, b):
    m = A.shape[0]
    n = A.shape[1]
    A = A.tolist()
    c = c.tolist()
    M = 1000
    for i in range(m):
        added = [0] * m
        added[i] = 1
        A[i] += added

    c[0] += [-M] * m
    A = np.array(A)
    c = np.array(c)
    basis = simplex(A, c, b, [i + n for i in range(m)])[0]

    if basis is None:
        return basis

    return list(map(operator.itemgetter(0), filter(lambda x: x[1] != 0, enumerate(basis))))


def two_step_simplex(A, b, c):
    basis = get_basis(A, c, b)
    return simplex(A, c, b, basis)


def main():
    A = np.array([
        [2, 1, 3, 0],
        [3, 1, 0, 1]
    ])
    c = np.array([[3, 4, -10, 0]])
    b = np.array([
        [24],
        [12]
    ])

    res = two_step_simplex(A, b, c)
    print(res)
    import scipy.optimize
    res = scipy.optimize.linprog(-c.reshape(-1), A_eq=A, b_eq=b.reshape(-1)).x
    print(res)



def is_int(x):
    return np.allclose(x - np.round(x), np.zeros(x.shape[0]))


def branching(A, b, idx, x):
    import math
    newA1 = np.copy(A)
    newb1 = np.copy(b)
    newcons = np.zeros((1, newA1.shape[1]))
    newcons[0][idx] = 1
    newA1 = np.concatenate((newA1, newcons))
    newb1 = np.concatenate((newb1, np.array([[math.floor(x[idx])]])))

    newA2 = np.copy(A)
    newb2 = np.copy(b)
    newcons = np.zeros((1, newA2.shape[1]))
    newcons[0][idx] = -1
    newA2 = np.concatenate((newA2, newcons))
    newb2 = np.concatenate((newb2, np.array([[-(math.floor(x[idx]) + 1)]])))

    return newA1, newb1, newA2, newb2



def lab62():
    import scipy.optimize
    two_step_simplex = lambda A, b, c: scipy.optimize.linprog(-c.reshape(-1), A_eq=A, b_eq=b.reshape(-1)).x

    A = np.array([
        [2, 1, 3, 0],
        [3, 1, 0, 1]
    ])
    c = np.array([[3, 4, -10, 0]])
    b = np.array([
        [24],
        [12]
    ])

    k = 0
    f = lambda x: (x @ c.transpose())[0]
    x = two_step_simplex(A, b, c)

    if np.isnan(x).any():
        return None, None, None

    f_val = f(x)

    if is_int(x):
        return x, f_val, 1

    q = [(f_val, x, A, b)]
    xs = []
    max_iters = 30
    while q:
        fs = [x[0] for x in q]
        maxind = max(enumerate(fs))[0]

        new_f, new_x, new_a, new_b = q.pop(maxind)

        filtered = list(filter(lambda v: not abs(v[1] - round(v[1])) <= 10 ** -8, enumerate(new_x)))
        if not filtered:
            continue
        idx = max(filtered, key=operator.itemgetter(0))[0]
        A1, b1, A2, b2 = branching(new_a, new_b, idx, new_x)

        x = two_step_simplex(A1, b1, c)
        if not np.isnan(x).any():
            if is_int(x):
                xs.append(x)
            q.append((f(x), x, A, b))

        x = two_step_simplex(A2, b2, c)
        if not np.isnan(x).any():
            if is_int(x):
                xs.append(x)
            q.append((f(x), x, A, b))

        if k > max_iters:
            break

        k += 1

    if len(xs) == 0:
        return None, None, k
    maxx = max(xs, key=f)
    return maxx, f(maxx), k


if __name__ == "__main__":
    main()
    print(lab62())
