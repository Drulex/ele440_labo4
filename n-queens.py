#!/usr/bin/env python

"""
ELE440 Labo4 - Algorithmes genetiques

Usage:
  labo3.py --import <fichier> <iterations> <pb_xover> <pb_mutation>
  labo3.py --generate <N> <pop_size> <iterations> <pb_xover> <pb_mutation>

Options:
  -h --help             Afficher cet ecran d'aide
  --version             Afficher la version.

  <fichier>             Fichier d'entree
  <iterations>          Nombre maximal de generations
  <N>                   Nombre de reines (taille de l'echiquier)
  <pb_xover>            Probabilite de recombinaison
  <pb_mutation>         Probabilite de mutation
  <pop_size>            Taille de la population
"""

from docopt import docopt
import sys
import matplotlib.pyplot as plt
from random import shuffle
from Population import Population, check_if_optimal


def parse_input_data(infile):
    '''
    Function parse data from input file
    Saves the solutions in an array of arrays called sol_array
    Returns N and sol_array
    '''
    with open(infile, 'r') as f:
        f.readline()
        N = int(f.readline())
        sol_array = []
        for line in f.readlines():

            #  For each line we split and convert values to int before adding to array
            sol = [int(x) for x in line.split()]

            #  If array is not empty we append it to array of solutions
            if sol:
                sol_array.append(sol)
        return N, sol_array


def graph_fitness_over_time(data):
    '''
    Print evolution of average fitness over time
    '''
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot(data.keys(), data.values(), 'r')
    axes.set_xlabel('Generation')
    axes.set_ylabel('Average fitness')
    axes.set_title('Evolution of average fitness over time')
    plt.show()


def generate_population(N, pop_size):
    '''
    Generates a random population based on user input
    '''
    population = []
    for i in xrange(pop_size):
        solution = [x for x in range(N)]
        shuffle(solution)
        population.append(solution)

    return population


class Printer():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self, data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    MAX_ITER = int(arguments['<iterations>'])
    XOVER_PROB = float(arguments['<pb_xover>'])
    MUTATION_PROB = float(arguments['<pb_mutation>'])

    if arguments['--import'] is True:
        INFILE = arguments['<fichier>']
        N, solutions = parse_input_data(INFILE)
        Pop = Population(N, solutions, XOVER_PROB, MUTATION_PROB)
        data = {}
        optimal_solutions = []
        iterations = 1

        #  Genetic algorithm loop starts here
        while iterations < MAX_ITER:
            print_iterations = 'Iteration=%i' % iterations
            Printer(print_iterations)
            params = Pop.get_graph_params()
            data.update(params)

            #  create the next generation
            next_generation = Pop.build_new_population()

            #  modify the current population to the new one
            Pop.regenerate_population(next_generation)

            #  increment generations
            iterations += 1


    elif arguments['--generate'] is True:
        N = int(arguments['<N>'])
        pop_size = int(arguments['<pop_size>'])
        solutions = generate_population(N, pop_size)
        Pop = Population(N, solutions, XOVER_PROB, MUTATION_PROB)
        data = {}
        optimal_solutions = []
        iterations = 0

        #  Genetic algorithm loop starts here
        while iterations < MAX_ITER:
            print_iterations = 'Iteration=%i' % iterations
            Printer(print_iterations)
            params = Pop.get_graph_params()
            data.update(params)

            #  create the next generation
            next_generation = Pop.build_new_population()

            #  modify the current population to the new one
            Pop.regenerate_population(next_generation)

            #  increment generations
            iterations += 1

    Pop.print_stats()
    if Pop.optimal_solutions:
        print 'Found %i solutions' %len(Pop.optimal_solutions)
        for s in Pop.optimal_solutions:
            print s
    Pop.export_stats('results.txt')
    Pop.export_optimal_solutions('solutions.txt')
    graph_fitness_over_time(data)