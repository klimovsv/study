import numpy as np
import math
import operator
from itertools import product


def f(x):
    return sum(map(lambda v: v ** 2 - 10 * math.cos(2 * v * math.pi) + 10, x))


def cross(ind1, ind2):
    c = np.random.rand()
    ch1 = c * ind1 + (1 - c) * ind2
    ch2 = c * ind2 + (1 - c) * ind1
    return ch1, ch2


def selection(population, cropsize):
    return population[:cropsize//4]


def mutate_function(alpha, beta):
    def f(individual):
        new_ind = np.copy(individual)
        for i in range(len(individual)):
            factor = np.random.rand()
            if np.random.randint(0, 2) == 0:
                new_ind[i] -= (new_ind[i] - alpha) * factor ** 15
            else:
                new_ind[i] += (beta - new_ind[i]) * factor ** 15
        return new_ind

    return f


def ga(fit, crossover, mutation, selection, n=3, crop=100, epoch=1000, alpha=0, beta=20):
    initial_individuals = np.random.uniform(low=alpha, high=beta, size=(crop, n))
    population = [(x, fit(x)) for x in initial_individuals]
    population.sort(key=operator.itemgetter(1))

    pcross = 0.5
    pmut = 0.2

    iter = 0
    while iter < epoch:
        iter += 1
        # selection
        if len(population) >= crop:
            population = selection(population, crop)

        pop_len = len(population)
        # cross
        parents = list(filter(lambda individual: np.random.rand() < pcross, population[:int(pop_len * pcross)]))
        parent_pairs = []
        for i, p in enumerate(parents):
            parent_pairs += list(product([p], parents[:i] + parents[i + 1:]))

        childs = []
        for pair in parent_pairs:
            p1, p2 = pair
            ch1, ch2 = crossover(p1[0], p2[0])
            childs.append((ch1, f(ch1)))
            childs.append((ch2, f(ch2)))

        # mutation
        mutation_list = list(filter(lambda individual: np.random.rand() < pmut, population[:int(pop_len * pmut)]))
        for i, individual in enumerate(mutation_list):
            mutated = mutation(individual[0])
            mutation_list[i] = (mutated, f(mutated))

        population += mutation_list + childs
        population.sort(key=operator.itemgetter(1))

    return population[0]





def main():
    x = ga(f, cross, mutate_function(0, 20), selection)
    print(x)


if __name__ == '__main__':
    main()
