#!/usr/bin/env python2
import random

# suggestion: BSTATES and GSTATES moved into TicTacToeGame class or to
# their own class? or something?
BSTATES = {'EMPTY':0, 'P1':1, 'P2':-1}
# suggestion: use tuple of strings instead of dict
GSTATES = {'INPROGRESS':4, 'NOTSTARTED':3, 'P2WON':BSTATES['P2'],
                        'P1WON':BSTATES['P1'], 'DRAW':2}

class TicTacToeGame:

    def __init__(self, size=3, initial_state=None):
        self.SIZE = size
        self.board = [[BSTATES['EMPTY']] * self.SIZE for _ in range(self.SIZE)]

        self.current_player = BSTATES['P1']
        self.mode = GSTATES['NOTSTARTED']

        # TODO: feature addition: full game stats: draws, num games
        self.wins = {BSTATES['P1']:0, BSTATES['P2']:0}
        self.losses = {BSTATES['P1']:0, BSTATES['P2']:0}

        self.lastwincoords = set()

        # for testing
        if initial_state:
            self.board = initial_state

    def make_random_move(self, player):
        ''' player is 1 or -1 (for X or O)
            returns the location that was changed
        '''
        if self.is_over():
            raise Exception("No game in progress. Game over.")

        location = random.choice(self.get_locations(BSTATES['EMPTY']))
        return self.make_move(player, location)

    def assign_value(self, player):
        
        def eval(player, lines):
            empty_weight = 0.5
            winning_weight = 999
            opponent_win_weight = 99
            value = 0
            for line in lines:
                bstates = self.get_bstates(line)
                num_zeros = bstates.count(bstates.EMPTY)

                s = sum(bstates) * player
                # our winning spot
                if s == 2:
                    value += winning_weight
                elif s == -2: # opponent's winning spot
                    value += opponent_win_weight
                else:
                    value += num_zeros*empty_weight + s

        
        values = [[0] * self.SIZE for _ in range(self.SIZE)]
        for row_i, row in enumerate(values):
            for col_i, item in enumerate(row):
                lines = []
                if row_i == col_i || row_i+col_i == self.SIZE - 1:
                    lines.append(self.get_diagonal_left())
                    lines.append(assign_diagonal_right(player))
                lines.append(assign_vertical(player))
                lines.append(assign_horizontal(player))

                values[row_i][col_i] = eval(player, lines)

    def get_bstates(self, line):
        return [self.board[row][col] for (row, col) in line]

    def get_diagonal_left_coords(self):
        return [(i,i) for i in range(self.SIZE)]
            
    def get_diagonal_right_coords(self):
        return [(self.SIZE-1-i, i) for i in range(self.SIZE)]

    def get_vertical_coords(self, col_i):
        return [(i, col_i) for i in range(self.SIZE)]

    def get_horizontal_coords(self, row_i):
        return [(row_i, i) for i in range(self.SIZE)]

    def optimal_move(self, weights):
        #TODO:

    def make_smart_move(self, player):
        
        weights = self.assign_value(player)
        location = optimal_move(weights)

        self.make_move(player, location)

    def get_locations(self, bstate):
        ''' returns list of (row, col) tuples '''
        board = self.board
        return [(ri,ci) for ri,row in
                enumerate(board) for ci,spot in
                enumerate(row) if spot == bstate]

    def is_over(self):
        return self.mode <= 2


    def reset(self, player):
        if self.mode == GSTATES['INPROGRESS']:
            self.losses[player] += 1
            self.wins[player * -1] += 1
        self.board = [[BSTATES['EMPTY'] for i in range(self.SIZE)] \
                   for i in range(self.SIZE)]
        self.current_player = BSTATES['P1']
        self.mode = GSTATES['NOTSTARTED']

    def make_move(self, player, (row,col)):
        ''' player is 1 or -1 (for X or O)
            location is tuple of row,col coords
            returns location that was changed
        '''
        if self.is_over():
            raise Exception("No game in progress. Game over.")

        # validate
        size = self.SIZE
        if player != self.current_player:
            msg = ("Invalid player " + str(player) + ". Should be " +
                    str(self.current_player))
            raise ValueError(msg)
        if row not in range(size) or col not in range(size):
            raise ValueError("Invalid location value " + str((row, col)))

        # update state
        if self.board[row][col] == BSTATES['EMPTY']:
            self.board[row][col] = player
            self.update_mode()
            if self.mode == GSTATES['INPROGRESS']:
                # only switch turns if most recent move did not end the game
                self.current_player *= -1
        else:
            raise ValueError("Location already full " + str((row, col)))

        return (row, col)

    def update_points(self):
        if self.mode == GSTATES['P1WON']:
            self.wins[BSTATES['P1']] += 1
            self.losses[BSTATES['P2']] += 1
        elif self.mode == GSTATES['P2WON']:
            self.wins[BSTATES['P2']] += 1
            self.losses[BSTATES['P1']] += 1

    @property
    def board_1d(self):
        return [i for row in self.board for i in row]

        #rewrite to fix the repeated return statements
    def update_mode(self):
        ''' determines whether game is over '''
        s = self.SIZE

        # don't check until one player has made > size moves
        if self.board_1d.count(BSTATES['EMPTY']) > s ** 2 - (s * 2 - 1):
            self.mode = GSTATES['INPROGRESS']
            return

        def update_mode_helper(line):
            self.mode = self.board[line[0][0]][line[0][1]]
            self.lastwincoords = set(line)
            self.update_points()

        for ri,row in enumerate(self.board):
            if TicTacToeGame.is_winning_line(row):
                update_mode_helper([(ri,i) for i in range(s)])
                return
        for ci,col in enumerate(zip(*self.board)):
            if TicTacToeGame.is_winning_line(col):
                update_mode_helper([(i,ci) for i in range(s)])
                return

        diagonal_coords = [[(i,i) for i in range(s)],
            [(s-1-i, i) for i in range(s)]]
        diagonals = [[self.board[i][i] for i in range(s)],
            [self.board[s-1-i][i] for i in range(s)]]

        for i,l in enumerate(diagonals):
            if TicTacToeGame.is_winning_line(l):
                update_mode_helper(diagonal_coords[i])
                return

        #it's a draw
        if BSTATES['EMPTY'] not in self.board_1d:
            self.mode = GSTATES['DRAW']
            self.lastwincoords = set()
            return

        #otherwise
        self.mode = GSTATES['INPROGRESS']

    @staticmethod
    def is_winning_line(line):
        ''' return true if line consists of all 'X' or 'O';
        line is a list of board spaces, like a row or a diagonal'''
        return BSTATES['EMPTY'] not in line and all(line[0] == i for i in \
                                                      line)


    # assuming game loop is implemented by UI
    def play(self):
        while self.mode == GSTATES['INPROGRESS']:
            break
            #TODO

    # for testing
    def __str__(self):
        boardstr = ''
        for row in self.board:
            for i in row:
                if i == BSTATES['P1']:
                    boardstr += 'X'
                elif i == BSTATES['P2']:
                    boardstr += 'O'
                else:
                    boardstr += '_'
            boardstr += '\n'
        return boardstr
