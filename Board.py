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
        if self.calc_fitness() == 0:
            return True
        else:
            return False