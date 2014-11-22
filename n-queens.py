from random import randint, sample, random
import numpy as np
import sys
import matplotlib.pyplot as plt

class Board:
    '''
    Board class represents the chessboard and methods available to manipulate it.
    '''

    def __init__(self, N, sol):
        '''
        We create a 2d array (list of lists) of size N x N
        We create an array to hold the solution in proper encoding format
        '''
        self.board = [[' ' for x in range(N)] for y in range(N)]
        self.sol = sol
        self.populate_board(N)

    def print_board(self):
        '''
        Print the current board
        '''
        print '----------------------------------------'
        for row in self.board:
            print row
        print '----------------------------------------'

    def add_queen(self, x, y):
        '''
        Add a queen on the board at position x, y
        '''
        self.board[x][y] = 'Q'

    def populate_board(self, N):
        '''
        Function to populate board based on sol_array
        '''
        #  We add the queens on the board
        for i in xrange(N):
            self.add_queen(self.sol[i], i)

    def calc_conflict(self, xpos, ypos):
        '''
        Function to calculate number of conflicts AT THE RIGHT SIDE
        of a given queen. This cannot be used to calculate all conflicts
        of a queen, but it is used when iterating queens from left to right
        on a given board
        '''
        conflict_count = 0
        k = 1
        for j in xrange(xpos + 1, len(self.sol)):
            if self.sol[j] == ypos + k:
                conflict_count += 1
            if self.sol[j] == ypos - k:
                conflict_count += 1
            if self.sol[j] == ypos:
                conflict_count += 1
            k += 1
        return conflict_count

    def calc_fitness(self):
        '''
        Function to calculate fitness function of a solution
        '''
        conflicts = 0

        #  for every queen starting from the first column (most left)
        #  we calculate the number of conflicts and increment it
        for i in xrange(0, len(self.sol)):
            conflicts += self.calc_conflict(i, self.sol[i])
        return -conflicts

    def check_if_optimal(self):
        '''
        Check if current chessboard is a optimal solution to the problem
        '''
        if self.calc_fitness == 0:
            return True
        else:
            return False


class Population:
    '''
    Class used to manipulation population object
    '''

    def __init__(self, N, solutions, xover_prob, mutation_prob):
        self.N = N
        self.xover_probability = xover_prob
        self.mutation_probability = mutation_prob
        self.population = []
        self.solutions = solutions
        self.fitness_dict = {}
        self.create_population(N)
        self.probabilities = self.get_probability_list()
        self.generation = 1

    def create_population(self, N):
        '''
        Take each solution and create board
        Also create fitness_dict: a dictionnary containing {solution: fitness}
        '''
        for s in self.solutions:
            self.population.append(Board(N, s))
        for s in self.population:
            self.fitness_dict.update({s: s.calc_fitness()})

    def get_probability_list(self):
        '''
        Create a list that with probability for a solution to be selected depending
        on its fitness.
        ---------------------------------------------
        Formula used:

        Pi = probability of a solution to be selected
        Fi = fitness of a solution
        Tfit = sum of fitness value of all solutions

        Pi = Fi / Tfit
        =---------------------------------------------
        '''
        fitness = self.fitness_dict.values()
        total_fitness = float(sum(fitness))
        relative_fitness = [f/total_fitness for f in fitness]
        probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
        return probabilities

    def roulette_wheel_select(self):
        '''
        Implementation of roulette wheel selection algorithm
        '''
        selected = []
        for n in xrange(2):
            r = random()
            for (i, individual) in enumerate(self.solutions):
                if r <= self.probabilities[i]:
                    selected.append(list(individual))
                    break
        return selected

    def two_points_crossover(self, sol1, sol2):
        '''
        Function to execute 2 points crossover on 2 chromosomes
        '''
        size = min(len(sol1), len(sol2))
        pt1 = randint(1, size)
        pt2 = randint(1, size - 1)
        if pt2 >= pt1:
            pt2 += 1
        else: # Swap the two cx points
            pt1, pt2 = pt2, pt1

        sol1[pt1:pt2], sol2[pt1:pt2] = sol2[pt1:pt2], sol1[pt1:pt2]
        return sol1, sol2

    def mutate_child(self, sol):
        '''
        This function randomly selects 2 bits in the solutions and swaps them
        '''
        r = sample(sol, 2)
        sol[r[0]], sol[r[1]] = sol[r[1]], sol[r[0]]

    def build_new_population(self):
        '''
        Creates a new population by doing:
            1. Selection (select 2 parents)
            2. Crossover (recombine them to create children)
            3. Mutation (mutate children)
            4. Repeat until new population is same size as previous generation
        '''
        new_population = []
        while len(new_population) < len(self.solutions):
            x = random()
            y = random()

            #  we select parents for recombination using roulette wheel method
            parents = self.roulette_wheel_select()

            #  check probability of crossover
            if x <= self.xover_probability:
                children = list(self.two_points_crossover(parents[0], parents[1]))
            else:
                children = parents

            #  check probability of mutation
            if y <= self.mutation_probability:
                self.mutate_child(children[0])
                self.mutate_child(children[1])

            #  add children to new population
            if len(set(children[0])) == len(children[0]):
                new_population.append(children[0])

            if len(set(children[1])) == len(children[1]):
                new_population.append(children[1])
        return new_population

    def regenerate_population(self, new_population):
        '''
        This function mutates the current Population object to the new generation.
        This uses less memory than creating new population objects each iteration.
        '''
        self.solutions = new_population
        self.population = []
        self.fitness_dict = {}
        self.create_population(self.N)
        self.probabilities = self.get_probability_list()
        self.generation += 1

    def print_stats(self):
        '''
        Print relevant stats
        '''
        print "Generation:", self.generation
        print 'Average fitness:', np.mean(self.fitness_dict.values())
        print "Population:"
        for key in self.fitness_dict:
            print key.sol, self.fitness_dict[key]

    def get_graph_params(self):
        params = []
        params.append(self.generation)
        params.append(np.mean(self.fitness_dict.values()))
        return params


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


def graph_fitness_over_time(gen, fit):
    '''
    Print evolution of average fitness over time
    '''
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
    axes.plot(gen, fit, 'r')
    axes.set_xlabel('Generation')
    axes.set_ylabel('Average fitness')
    axes.set_title('Evolution of average fitness over time')
    plt.show()


def check_for_optimal(pop):
    for b in pop.population:
        if b.check_if_optimal() is True:
            print "FOUND OPTIMAL SOLUTION"
            sys.exit(1)



if __name__ == '__main__':
    iterations = 0
    infile = 'fichierTest-20-8.txt'
    XOVER_PROB = 0.6
    MUTATION_PROB = 0.8
    N, solutions = parse_input_data(infile)
    Pop = Population(N, solutions, XOVER_PROB, MUTATION_PROB)
    generations = []
    avg_fitness = []
    Pop.print_stats()
    while iterations < 2000:
        params = Pop.get_graph_params()
        generations.append(params[0])
        avg_fitness.append(params[1])
        check_for_optimal(Pop)
        next_generation = Pop.build_new_population()
        Pop.regenerate_population(next_generation)
        Pop.print_stats()
        iterations += 1

    graph_fitness_over_time(generations, avg_fitness)