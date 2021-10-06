import math
from main import *    #this is just for writing solve separately, delete when merging main and solver

class State:
    def __init__(self, board, player, score, depth):
        self.board = board.copy()
        self.player = player    #1 is player1, -1 is player2
        self.score = score
        self.depth = depth

#placeholder
def check_win(board):
    pass
def is_full(board):
    pass

def isTerminated(state):
    return len(check_win(state.board)) > 0 or is_full(state.board())

def minimax(state):




if __name__ == "__main__":
    print(board)

