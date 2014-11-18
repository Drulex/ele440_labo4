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
		for row in self.board:
			print row


	def add_queen(self, x, y):
		'''
		Add a queen on the board at position x, y
		'''
		self.board[x][y] = 'Q'


def build_board_from_solution(sol):
	'''
	Function to build board from solution array
	'''



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
			#  for each line we split and convert values to int before adding to array
			sol = [int(x) for x in line.split()]
			#  if array is not empty we append it to array of solutions
			if sol:
				sol_array.append(sol)
		return N, sol_array



if __name__ == '__main__':
	#b = Board(10)
	#b.add_queen(3, 8)
	#b.print_board()
	infile = 'fichierTest-20-8.txt'
	N, solutions = parse_input_data(infile)
	print N
	print solutions