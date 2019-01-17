import math

import numpy as np
from numpy.linalg import inv
import functools
import random


class Matrix:

    @staticmethod
    def generate(n):
        matrix = np.zeros((n, n))
        for i in range(n):
            matrix[i, i] = random.uniform(10, 100)
        for i in range(n - 1):
            matrix[i, i + 1] = matrix[i + 1, i] = random.uniform(10, 100)
        return Matrix(matrix)

    @staticmethod
    def is_numeric(var):
        tp = type(var)
        return tp is int or tp is float

    def transpose(self):
        return Matrix(self.matr.transpose())

    @staticmethod
    def from_const(number):
        return Matrix(np.array([[number]]))

    @staticmethod
    def zeros(n):
        return Matrix(np.zeros((n, n), np.float))

    @staticmethod
    def diag_from_vector(diag):
        m = Matrix.zeros(len(diag))
        for i in range(len(diag)):
            m.matr[i, i] = diag[i]
        return m

    def set_vector(self, vec, n):
        for i in range(len(vec)):
            self.matr[i, n] = vec[i]

    def set_vector_eign(self, vec, n):
        vec_len = math.sqrt(functools.reduce(lambda a, b: a + b, map(lambda v: v ** 2, vec)))
        # vec_len=1
        for i in range(len(vec)):
            self.matr[i, n] = vec[i] / vec_len

    @staticmethod
    def vector(vec):
        m = np.zeros((len(vec), 1), np.float)
        for i in range(len(vec)):
            m[i, 0] = vec[i]
        return Matrix(m)

    @staticmethod
    def identity(n):
        return Matrix(np.eye(n))

    def getCol(self, n):
        return self.matr[:, n].reshape(-1)

    @staticmethod
    def diagonaled(m1, m2):
        pos = m1.matr.shape[0]
        length = m1.matr.shape[0] + m2.matr.shape[0]
        matr = np.zeros((length, length))
        matr[:pos, :pos] = m1.matr
        matr[pos:, pos:] = m2.matr
        return Matrix(matr)

    def cut(self):
        if self.matr.shape[1] != self.matr.shape[0]:
            raise Exception("sorting supported only in square matrices")

        if self.matr.shape[0] >= 3:
            position = self.matr.shape[0] - 3
        else:
            position = self.matr.shape[0] - 2
        # print(position)

        matr = self.matr.copy()

        b = matr[position, position + 1]

        v = np.zeros((matr.shape[0], 1))
        v[position, 0] = 1
        v[position + 1, 0] = 1

        matr[position, position] -= b
        matr[position + 1, position + 1] -= b
        matr[position, position + 1] = 0
        matr[position + 1, position] = 0

        t1 = Matrix(matr[:position + 1, :position + 1])
        t2 = Matrix(matr[position + 1:, position + 1:])

        return self.diagonaled(t1, t2), t1, t2, b, Matrix(v)

        # print(self.matr[:position+1,:position+1])

    def sort(self):
        if self.matr.shape[1] != self.matr.shape[0]:
            raise Exception("sorting supported only in square matrices")

        matr = self.matr.copy()
        permutation = self.identity(self.matr.shape[0])

        left = self.identity(self.matr.shape[0])
        right = self.identity(self.matr.shape[0])
        length = self.matr.shape[0]

        for i in range(length - 1, 0, -1):
            for j in range(i):
                if matr[j, j] < matr[j + 1, j + 1]:
                    permutation = self.swap_rows_matr(j, j + 1) * permutation
                    left = self.swap_rows_matr(j, j + 1) * left
                    right = right * self.swap_cols_matr(j, j + 1)
                    matr[j, j], matr[j + 1, j + 1] = matr[j + 1, j + 1], matr[j, j]

        return permutation, left, right

    def swap_cols_matr(self, i, j):
        id = self.identity(self.matr.shape[1]).matr
        id[i, i] = 0
        id[j, j] = 0
        id[i, j] = 1
        id[j, i] = 1
        return Matrix(id)

    def swap_rows_matr(self, i, j):
        id = self.identity(self.matr.shape[0]).matr
        id[i, i] = 0
        id[j, j] = 0
        id[i, j] = 1
        id[j, i] = 1
        return Matrix(id)

    def inv(self):
        return Matrix(inv(self.matr))

    def __init__(self, matr):
        # print(matr.shape)
        if matr.shape[0] == 0 or matr.shape[1] == 0:
            raise Exception("please insert not empty matrix")

        self.matr = matr

    def __sub__(self, other):
        if type(other) is Matrix:
            return Matrix(self.matr - other.matr)
        else:
            raise Exception("unsupported type for operation : {}".format(type(other)))

    def __add__(self, other):
        if type(other) is Matrix:
            return Matrix(self.matr + other.matr)
        else:
            raise Exception("unsupported type for operation : {}".format(type(other)))

    __radd__ = __add__

    def __mul__(self, other):
        if self.is_numeric(other):
            return Matrix(self.matr * other)
        elif type(other) is Matrix:
            return Matrix(np.matmul(self.matr, other.matr))
        else:
            raise Exception("unsupported type for operation : {}".format(type(other)))

    def __rmul__(self, other):
        if self.is_numeric(other):
            return self * other
        else:
            raise Exception("unsupported type for operation : {}".format(type(other)))

    def __str__(self):
        return str(self.matr)
