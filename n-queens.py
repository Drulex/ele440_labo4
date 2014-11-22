from random import randint, sample
import sys

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

    def __init__(self, N, solutions):
        self.N = N
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

    def recombine(self):
        '''
        Recombination algorithm. Selects 2 solutions at random and recombines them
        We may choose the crossover function we want
        '''
        #  we select 2 solutions at random
        randi = sample(xrange(len(self.population)), 2)

        #  we recombine them using 2 points crossover
        self.two_points_crossover(self.solutions[randi[0]], self.solutions[randi[1]])




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


def check_for_optimal(pop):
    for b in pop.population:
        print b.calc_fitness()
        if b.check_if_optimal() is True:
            print "FOUND OPTIMAL SOLUTION"
            sys.exit(1)


if __name__ == '__main__':
    infile = 'fichierTest-20-8.txt'
    N, solutions = parse_input_data(infile)
    Pop = Population(N, solutions)
    iterations = 0
    while iterations < 10000:
        print 'iteration=', iterations
        check_for_optimal(Pop)
        Pop.recombine()
        iterations += 1
