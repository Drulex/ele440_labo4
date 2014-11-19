class Board:
	'''
	Board class represents the chessboard and methods available to manipulate it.
	'''

	def __init__(self, N):
		'''
		We create a 2d array (list of lists) of size N x N
		'''
		self.board = [[' ' for x in range(N)] for y in range(N)]


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



def build_board_from_solution(N, sol):
	'''
	Function to build board from solution array
	'''
	#  We create board object
	board = Board(N)

	#  We add the queens on the board
	for i in xrange(len(sol)):
		board.add_queen(sol[i], i)

	#  We print the board
	board.print_board()
	return board


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


def calc_conflict(sol, xpos, ypos):
	'''
	Function to calculate number of conflicts AT THE RIGHT SIDE
	of a given queen. This cannot be used to calculate all conflicts
	of a queen, but it is used when iteraing queens from left to right
	on a given board
	'''
	conflict_count = 0
	k = 1
	for j in xrange(xpos + 1, len(sol)):
		if sol[j] == ypos + k:
			print
			conflict_count += 1
		if sol[j] == ypos - k:
			conflict_count += 1
		if sol[j] == ypos:
			conflict_count += 1
		k += 1
	return conflict_count


def calc_fitness(sol):
	'''
	Function to calculate fitness function of a solution
	'''
	conflicts = 0

	#  for every queen starting from the first column (most left)
	#  we calculate the number of conflicts and increment
	for i in xrange(0, len(sol)):
		conflicts += calc_conflict(sol, i, sol[i])
	return conflicts


if __name__ == '__main__':
	infile = 'fichierTest-20-8.txt'
	#N, solutions = parse_input_data(infile)
	#build_board_from_solution(N, solutions[0])
	#print solutions[0]
	sol = [1, 3, 4, 2, 1, 7, 5, 0]
	sol2 = [6, 4, 2, 0, 5, 7, 1, 3]
	build_board_from_solution(8, sol2)
	print 'fitness: ', calc_fitness(sol2)
