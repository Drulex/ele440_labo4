#!/usr/bin/env python

"""
ELE440 Labo4 - Algorithmes genetiques

Usage:
  labo3.py --import <fichier> <iterations> <pb_xover> <pb_mutation>
  labo3.py --generate <N> <iterations> <pb_xover> <pb_mutation>

Options:
  -h --help             Afficher cet ecran d'aide
  --version             Afficher la version.

  <fichier>             Fichier d'entree
  <iterations>          Nombre maximal de generations
  <N>                   Nombre de reines (taille de l'echiquier)
  <pb_xover>            Probabilite de recombinaison
  <pb_mutation>         Probabilite de mutation
"""

from docopt import docopt
import sys
import numpy as np
import matplotlib.pyplot as plt
from Population import Population


def parse_input_data(infile):
    '''
    Function parse data from input file
    Saves the solutions in an array of arrays called sol_array
    Returns N and sol_array
    '''
    with open(infile, 'r') as f:
        nsol = int(f.readline())
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
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
    axes.plot(data.keys(), data.values(), 'r')
    axes.set_xlabel('Generation')
    axes.set_ylabel('Average fitness')
    axes.set_title('Evolution of average fitness over time')
    plt.show()


def check_for_optimal(pop):
    for b in pop.population:
        if b.check_if_optimal() is True:
            print "FOUND OPTIMAL SOLUTION"
            return b


class Printer():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()


if __name__ == '__main__':
    iterations = 0
    infile = 'fichierTest-20-8.txt'
    XOVER_PROB = 0.4
    MUTATION_PROB = 0.5
    N, solutions = parse_input_data(infile)
    Pop = Population(N, solutions, XOVER_PROB, MUTATION_PROB)
    generations = []
    avg_fitness = []
    optimal_solutions = []
    while iterations < 10000:
        print_iterations = 'Iteration=%i' % iterations
        Printer(print_iterations)
        params = Pop.get_graph_params()
        generations.append(params[0])
        avg_fitness.append(params[1])
        optimal_solutions.append(check_for_optimal(Pop))
        next_generation = Pop.build_new_population()
        Pop.regenerate_population(next_generation)
        iterations += 1

    graph_fitness_over_time(generations, avg_fitness)    arguments = docopt(__doc__, version='1.0')
    MAX_ITER = int(arguments['<iterations>'])
    XOVER_PROB = float(arguments['<pb_xover>'])
    MUTATION_PROB = float(arguments['<pb_mutation>'])