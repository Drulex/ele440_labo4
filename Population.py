from random import randint, sample, random, choice, shuffle
import numpy as np


class Population:
    '''
    Class used to manipulation population object
    '''

    def __init__(self, N, solutions, xover_prob, mutation_prob):
        #  number of queens
        self.N = N

        self.baro = 1

        #  probability constants
        self.xover_probability = xover_prob
        self.mutation_probability = mutation_prob

        #  list containing solutions in Board object form
        self.population = []

        #  list containing solutions in list form
        self.solutions = solutions

        #  list of fitness values
        self.fitness_vals = []

        #  list to hold all fitness results
        self.all_fitness_results = []

        #  create board objects with each solution
        self.create_population(N)

        #  attribute representing generation
        self.generation = 1

    def create_population(self, N):
        '''
        Take each solution and create board (if no duplicates in sol)
        Also create fitness_dict: a dictionnary containing {solution: fitness}
        '''
        i = 0
        for s in self.solutions:
            self.baro += 1

            #  we check if the solution contains duplicates (queens on two rows)
            if len(s) == len(set(s)):
                self.baro += 1
                self.population.append(s)

            #  if solution contains duplicate we generate another
            else:
                self.baro += 1
                s = self.generate_random_solution()
                self.population.append(s)
                self.solutions[i] = s

            i += 1

        for s in self.population:
            self.baro += 1
            fit_val, b = calc_fitness(s)
            self.baro += b
            self.fitness_vals.append(fit_val)
            self.all_fitness_results.append(fit_val)

    def generate_random_solution(self):
        '''
        This function generates a random chromosome while making sure
        we don't have two queens on the same row
        '''
        #  generate list with N values in order
        sol = [i for i in range(self.N)]

        #  because of list comprehension we have to increment the barometer
        #  counter here
        for i in range(self.N):
            self.baro += 1

        #  shuffle the list
        shuffle(sol)
        return sol

    def one_point_xover(self, sol1, sol2):
        size = self.N
        pt = randint(0, size - 1)
        child = [None] * self.N
        child[0:pt] = sol1[0:pt]
        child[pt:] = sol2[pt:]

        return child

    def xover(self, sol1, sol2):
        '''
        Crossover function that breeds 2 parents the following way:
            1. If two parents have common board positions they are transferred to child
            2. Rest of positions are randomly generated (with no duplicates)
        '''
        #  if both solutions are the same we randomize one of them
        if sol1 == sol2:
            self.baro += 1
            sol2 = self.generate_random_solution()

        x = random()
        if x < self.xover_probability:
            child = self.one_point_xover(sol1, sol2)
            return child

        #  list with possible values of queens
        possible = [i for i in xrange(self.N)]

        #  child chromosome
        child = [-1 for i in xrange(self.N)]

        #  if a position is common to both solutions we keep it
        for i in range(len(sol1)):
            self.baro += 3  # because of 2 list comprehension above
            if(sol1[i] == sol2[i]):
                self.baro += 1
                child[i] = sol1[i]
                possible.remove(child[i])

        #  we randomize rest of positions
        for i in range(len(sol1)):
            self.baro += 1
            if(child[i] == -1):
                self.baro += 1
                child[i] = choice(possible)
                possible.remove(child[i])

        return child

    def mutate_child(self, sol):
        '''
        This function randomly selects 2 bits in the solutions and swaps them
        '''
        self.baro += 1
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
        alpha_parents = self.get_alpha_parents()
        size = len(alpha_parents) - 1

        for p in alpha_parents:
            self.baro += 1
            new_population.append(p)

        while len(new_population) < len(self.solutions):
            self.baro += 1

            #  random params we will measure probabilites of xover and mutation against
            x = random()
            y = random()

            #  check probability of crossover
            if x <= self.xover_probability:
                self.baro += 1
                child = self.xover(alpha_parents[randint(0, size)], alpha_parents[randint(0, size)])
            #  if no crossover the child will be one of the two parents
            else:
                self.baro += 1
                a = randint(0, size)
                child = alpha_parents[a]
            #  check probability of mutation
            if y <= self.mutation_probability:
                self.baro += 1
                self.mutate_child(child)

            #  add children to new population
            new_population.append(child)

        return new_population

    def get_alpha_parents(self):
        '''
        This function returns 50 percent of most fit parents
        The new generation will be composed of these parents and
        offspring after they are crossed and chidrend are mutate_child
        '''

        #  reorder solutions and fitness_vals lists
        sorted_zip = sorted(zip(self.fitness_vals, self.solutions))
        self.solutions = [x for (y, x) in sorted_zip]
        self.fitness_vals = [y for (y, x) in sorted_zip]

        for i in sorted_zip:
            self.baro += 2

        size = len(self.population)/2

        #  return most fit half
        return self.solutions[size:]

    def regenerate_population(self, new_population):
        '''
        This function mutates the Population object to the new generation.
        This uses less memory than creating new population objects each iteration.
        '''
        self.solutions = new_population
        self.population = []
        self.fitness_vals = []
        self.create_population(self.N)
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
        print 'Temps de calcul:', self.get_barometer_count()
        print '================================================='

    def export_stats(self, outfile):
        '''
        Function to export stats to text file.
        '''
        with open(outfile, 'w') as f:
            f.write('Statistiques:\n')
            f.write('Nombre de reines: %i\n' % self.N)
            f.write('Taille de la population: %i\n' % len(self.population))
            f.write('Nombre de generation: %i\n' % self.generation)
            f.write('Probabilite de recombinaison: %f\n' % self.xover_probability)
            f.write('Probabilite de mutation: %f\n' % self.mutation_probability)
            f.write('Fitness de la meilleure solution: %i\n' % self.get_best_fitness())
            f.write('Temps de calcul: %i' % self.get_barometer_count())

    def get_graph_params(self):
        '''
        Getter method for params used when graphing
        '''
        params = {}
        params.update({self.generation: np.mean(self.fitness_vals)})
        return params

    def get_barometer_count(self):
        return self.baro

    def get_best_fitness(self):
        '''
        Returns best fitness ever calculated
        '''
        return max(self.all_fitness_results)


def calc_conflict(sol, xpos, ypos):
        '''
        Function to calculate number of conflicts AT THE RIGHT SIDE
        of a given queen. This cannot be used to calculate all conflicts
        of a queen, but it is used when iterating queens from left to right
        on a given board
        '''
        baro = 0
        conflict_count = 0
        k = 1
        for j in xrange(xpos + 1, len(sol)):
            baro += 1
            if sol[j] == ypos + k:
                baro += 1
                conflict_count += 1
            if sol[j] == ypos - k:
                baro += 1
                conflict_count += 1
            if sol[j] == ypos:
                baro += 1
                conflict_count += 1
            k += 1
        return conflict_count, baro


def calc_fitness(sol):
        '''
        Function to calculate fitness function of a solution
        '''
        conflicts = 0
        baro = 0

        #  for every queen starting from the first column (most left)
        #  we calculate the number of conflicts and increment it
        for i in xrange(0, len(sol)):
            c, b = calc_conflict(sol, i, sol[i])
            conflicts += c
            baro += b
        return -conflicts, baro


def check_if_optimal(sol):
        '''
        Check if a solution is the optimal solution to the problem
        '''
        res, b = calc_fitness(sol)
        if res == 0:
            return True
        else:
            return False
