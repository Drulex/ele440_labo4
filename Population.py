from random import randint, sample, random, choice, shuffle
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

        #  list to hold all fitness results
        self.all_fitness_results = []

        #  create board objects with each solution
        self.create_population(N)

        #  list of relative fitness values
        self.probabilities = self.get_probability_list()

        #  attribute representing generation
        self.generation = 0

    def create_population(self, N):
        '''
        Take each solution and create board (if no duplicates in sol)
        Also create fitness_dict: a dictionnary containing {solution: fitness}
        '''
        i = 0
        for s in self.solutions:

            #  we check if the solution contains duplicates (queens on two rows)
            if len(s) == len(set(s)):
                self.population.append(Board(N, s))

            #  if solution contains duplicate we generate another
            else:
                s = self.generate_random_solution()
                self.population.append(Board(N, s))
                self.solutions[i] = s

            i += 1

        for s in self.population:
            self.fitness_dict.update({s: s.calc_fitness()})
            self.all_fitness_results.append(s.calc_fitness())

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

    def xover(self, sol1, sol2):
        '''
        Crossover function that breeds 2 parents the following way:
            1. If two parents have common board positions they are transferred to child
            2. Rest of positions are randomly generated (with no duplicates)
        '''
        #  if both solutions are the same we randomize one of them
        if sol1 == sol2:
            sol2 = self.generate_random_solution()

        #  list with possible values of queens
        possible = [i for i in range(len(sol1))]

        #  child chromosome
        child = [-1 for i in range(len(sol1))]

        #  if a position is common to both solutions we keep it
        for i in range(len(sol1)):
            if(sol1[i] == sol2[i]):
                child[i] = sol1[i]
                possible.remove(child[i])

        #  we randomize rest of positions
        for i in range(len(sol1)):
            if(child[i] == -1):
                child[i] = choice(possible)
                possible.remove(child[i])

        return child

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
            2. Crossover (recombine them to create a child)
            3. Mutation (mutate children)
            4. Repeat until new population is same size as previous generation
        '''
        new_population = []
        while len(new_population) < len(self.solutions):

            #  random params we will measure probabilites of xover and mutation against
            x = random()
            y = random()

            #  we select parents for recombination using roulette wheel method
            parents = self.roulette_wheel_select()

            #  check probability of crossover
            if x <= self.xover_probability:
                child = self.xover(parents[0], parents[1])
            #  if no crossover the child will be one of the two parents
            else:
                a = choice([0, 1])
                child = parents[a]
            #  check probability of mutation
            if y <= self.mutation_probability:
                self.mutate_child(child)

            #  add children to new population
            new_population.append(child)

        return new_population

    def regenerate_population(self, new_population):
        '''
        This function mutates the Population object to the new generation.
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
        print
        print '================================================='
        print 'Statistiques:'
        print 'Nombre de reines:', self.N
        print 'Taille de la population:', len(self.population)
        print 'Nombre de generations:', self.generation
        print 'Probabilite de recombinaison:', self.xover_probability
        print 'Probabilite de mutation:', self.mutation_probability
        print 'Fitness de la meilleure solution:', self.get_best_fitness()
        print 'Temps de calcul: TODO'
        print '================================================='


    def get_graph_params(self):
        '''
        Getter method for params used when graphing
        '''
        params = {}
        params.update({self.generation: np.mean(self.fitness_dict.values())})
        return params

    def get_best_fitness(self):
        '''
        Returns best fitness ever calculated
        '''
        return max(self.all_fitness_results)
