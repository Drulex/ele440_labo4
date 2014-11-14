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


def build_board_from_file(infile):
	'''
	Function to import text file and build chess board based on params
	'''



if __name__ == '__main__':
	b = Board(10)
	b.add_queen(3, 8)
	b.print_board()