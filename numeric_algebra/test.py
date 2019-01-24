from main import *
from Matrix import *
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from statistics import *

def testing_diff(iters_inside,iters, size, diff_size):
    max_ = []
    min_ = []
    avg_ = []
    median_ = []
    x = [size + i for i in range(iters)]
    for i in range(iters):
        lmax_ = []
        lmin_ = []
        lavg_ = []
        lmedian_ = []
        for j in range(iters_inside):
            m = Matrix.generate(size)
            Q, D = spectral(m)
            diag = list(sorted([D.matr[i,i] for i in range(size)]))
            m.change(diff_size)
            Q, D = spectral(m)
            diff_diag = list(sorted([D.matr[i, i] for i in range(size)]))
            d = vector_diff(diag,diff_diag)
            print(i,j,d)
            lmax_.append(d["max"])
            lmin_.append(d["min"])
            lavg_.append(d["avg"])
            lmedian_.append(d["median"])
        max_.append(mean(lmax_))
        min_.append(mean(lmin_))
        avg_.append(mean(lavg_))
        median_.append(mean(lmedian_))
        size += 1

    plt.plot(x, max_, label='max')
    plt.plot(x, avg_, label='avg')
    plt.plot(x, median_, label='median')
    plt.xticks(x)
    plt.xlabel('size')
    plt.ylabel('abs diff')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()


def testing(iters_inside,iters, size):
    max_ = []
    min_ = []
    avg_ = []
    median_ = []
    x = [size + i for i in range(iters)]
    for i in range(iters):
        lmax_ = []
        lmin_ = []
        lavg_ = []
        lmedian_ = []
        for j in range(iters_inside):
            m = Matrix.generate(size)
            Q, D = spectral(m)
            diag = list(sorted([D.matr[i, i] for i in range(size)]))
            diff_diag = list(sorted(linalg.eig(m.matr)[0]))
            d = vector_diff(diag, diff_diag)
            print(i, j, d)
            lmax_.append(d["max"])
            lmin_.append(d["min"])
            lavg_.append(d["avg"])
            lmedian_.append(d["median"])
        max_.append(mean(lmax_))
        min_.append(mean(lmin_))
        avg_.append(mean(lavg_))
        median_.append(mean(lmedian_))
        size += 1

    plt.plot(x, max_, label='max')
    plt.plot(x, avg_, label='avg')
    plt.plot(x, median_, label='median')
    plt.xticks(x)
    plt.xlabel('size')
    plt.ylabel('abs diff')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

def testing_wilk(iters,start):
    max = []
    min = []
    avg = []
    median = []
    ind = start
    for i in range(iters):
        m = Matrix.generate_wilk(ind)
        Q, D = spectral(m)
        diag = list(sorted([D.matr[i, i] for i in range(ind)]))
        numpy_diag = list(sorted(linalg.eig(m.matr)[0]))
        d = vector_diff(diag,numpy_diag)
        print(i, d)
        max.append(d["max"])
        min.append(d["min"])
        avg.append(d["avg"])
        median.append(d["median"])
        ind += 2

    x = [start + i*2 for i in range(iters)]
    print(x)
    # plt.xticks(x)
    plt.plot(x, max, label='max')
    plt.plot(x, avg, label='avg')
    plt.plot(x, median, label='median')

    plt.xlabel('size')
    plt.ylabel('abs diff')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)

    plt.show()

def testing_wilk_first(iters,start):
    ind = start
    diff = []
    for i in range(iters):
        locdiff = []
        m = Matrix.generate_wilk(ind)
        Q, D = spectral(m)
        diag = list(sorted([D.matr[i, i] for i in range(ind)],reverse=True))
        numpy_diag = list(sorted(linalg.eig(m.matr)[0],reverse=True))
        d = vector_diff(diag, numpy_diag)
        print(i, d)
        # print(diag)
        # print(numpy_diag)
        ind += 2
        for i in range(10):
            locdiff.append(math.fabs(diag[i]-numpy_diag[i]))
        diff.append(mean(locdiff))

    x = [start + i * 2 for i in range(iters)]
    plt.plot(x, diff, label='avg')

    plt.xlabel('size')
    plt.ylabel('abs diff')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)

    plt.show()


def testing_eign(iters_inside, iters, size):
    max_ = []
    avg_ = []
    median_ = []
    x = [size + i for i in range(iters)]
    for i in range(iters):
        lmax_ = []
        lavg_ = []
        lmedian_ = []

        for j in range(iters_inside):
            m = Matrix.generate(size)
            Q, D = spectral(m)
            diag = [D.matr[i, i] for i in range(size)]
            E = Matrix.identity(size)

            _max_ = []
            _avg_ = []
            _med_ = []

            for i in range(size):
                w = Matrix.vector(Q.getCol(i))
                l = diag[i]
                vec_diff = ((m - l * E) * w).matr.reshape(-1)
                vec_diff = map(math.fabs,vec_diff)
                _max_.append(max(vec_diff))
                # _avg_.append(mean(vec_diff))
                # _med_.append(median(vec_diff))

            lmax_.append(mean(_max_))
            # lavg_.append(mean(_avg_))
            # lmedian_.append(mean(_med_))

        max_.append(mean(lmax_))
        # avg_.append(mean(lavg_))
        # median_.append(mean(lmedian_))
        size += 1


    plt.plot(x, max_, label='max')
    # plt.plot(x, avg_, label='avg')
    # plt.plot(x, median_, label='median')
    plt.xticks(x)
    plt.xlabel('size')
    plt.ylabel('abs diff')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

# testing_diff(5,20, 5, 0.001)
# testing(5,20,5)
# testing_wilk(50, 5)
# testing_wilk_first(42, 21)
# def testing_eign(size):
#     m = Matrix.generate(size)
#     E = Matrix.identity(size)
#     Q, D = spectral(m)
#     diag = [D.matr[i, i] for i in range(size)]
#     for i in range(size):
#         w = Matrix.vector(Q.getCol(i))
#         l = diag[i]
#         print("own ",((m - l * E)*w).matr.reshape(-1))
testing_eign(1,20,5)

