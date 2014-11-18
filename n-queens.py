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
		board.add_queen(i, sol[i])

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



if __name__ == '__main__':
	infile = 'fichierTest-20-8.txt'
	N, solutions = parse_input_data(infile)
	for i in xrange(len(solutions)):
		build_board_from_solution(N, solutions[i])