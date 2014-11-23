from random import randint, sample, random
from Board import Board
import numpy as np

class Population:
    '''
    Class used to manipulation population object
    '''

    def __init__(self, N, solutions, xover_prob, mutation_prob):
        #  number of queens
        self.N = N

        #  probability constants
        self.xover_probability = xover_prob
        self.mutation_probability = mutation_prob

        #  list containing solution in Board object form
        self.population = []

        #  list containing solutions in list form
        self.solutions = solutions

        #  dictionnary containing solutions and their corresponding fitness value
        self.fitness_dict = {}

        #  create board objects with each solution
        self.create_population(N)

        #  list of relative fitness values
        self.probabilities = self.get_probability_list()

        #  attribute representing generation
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

    def generate_random_solution(self):
        '''
        This function generates a random chromosome while making sure
        we don't have two queens on the same row
        '''
        #  generate list with N values in order
        sol = [i for i in range(self.N)]

        #  shuffle the list
        shuffle(sol)

        return sol

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
        params = {}
        params.update({self.generation: np.mean(self.fitness_dict.values())})
        return params