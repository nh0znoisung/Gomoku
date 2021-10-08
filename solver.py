import math
from copy import deepcopy
#from main import *    #this is just for writing solve separately, delete when merging main and solver
from queue import LifoQueue

# Set board 19x19
board = [[0 for j in range(19)] for i in range(19)] # 0 is empty, 1 is Player 1, -1 is Player 2
turn = 1


class State:
    def __init__(self, board, player, depth):
        self.board = deepcopy(board)
        self.player = player    #The player that makes the next move. 1 is player1, -1 is player2
        self.depth = depth

        self.score = self.calScore()
        self.bestMove = ()


    def calScore(self):
        '''Calculate the point value for the current state'''
        winList = check_win(self.board)
        if len(winList) > 0:
            # just to make sure the player just made the move is the winning one
            winPlayer = self.board[winList[0][0]][winList[0][1]]
            assert winPlayer == -self.player
            if (winPlayer == 1):
                return 100
            elif (winPlayer == -1):
                return -100
            else:
                return None
        else:
            return 0


def check_win(curr_board):
    for x in [-1, 1]:
        # Horizontal with straight 5 points -> 1
        for i in range(19):
            cnt = 0
            for j in range(19):
                if curr_board[i][j] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(i, j - 4), (i, j), 1, x]
                else:
                    cnt = 0

        # Vertical with straight 5 points -> 2
        for i in range(19):
            cnt = 0
            for j in range(19):
                if curr_board[j][i] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(j - 4, i), (j, i), 2, x]
                else:
                    cnt = 0

        # Diagonal top-left to bottom-right -> 3
        cnt = 0
        for i in range(19):
            if curr_board[i][i] == x:
                cnt += 1
                if cnt == 5:
                    return [(i - 4, i - 4), (i, i), 3, x]
            else:
                cnt = 0
        for i in range(1, 19):
            # (i,0)
            cnt = 0
            for j in range(19 - i):
                if curr_board[i + j][j] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(i + j - 4, j - 4), (i + j, j), 3, x]
                else:
                    cnt = 0
        for i in range(1, 19):
            # (i,0)
            cnt = 0
            for j in range(19 - i):
                if curr_board[18 - (i + j)][18 - j] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(18 - i - j, 18 - j), (18 - (i + j) + 4, 18 - j + 4), 3, x]
                else:
                    cnt = 0

        # Diagonal top-right to bottom-left -> 4
        cnt = 0
        for i in range(19):
            if curr_board[18 - i][i] == x:
                cnt += 1
                if cnt == 5:
                    return [(18 - i, i), (18 - i + 4, i - 4), 4, x]
            else:
                cnt = 0
        for i in range(18):
            # (i,0)
            cnt = 0
            for j in range(i + 1):
                if curr_board[i - j][j] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(i - j, j), (i - j + 4, j - 4), 4, x]
                else:
                    cnt = 0
        for i in range(18):
            # (i,0)
            cnt = 0
            for j in range(i + 1):
                if curr_board[18 - (i - j)][18 - j] == x:
                    cnt += 1
                    if cnt == 5:
                        return [(18 - (i - j) - 4, 18 - j + 4), (18 - (i - j), 18 - j), 4, x]
                else:
                    cnt = 0
    return []

def is_full(curr_board):  # check draw or not
    for i in range(19):
        for j in range(19):
            if curr_board[i][j] == 0:
                return False
    return True

def isTerminated(state):
    return len(check_win(state.board)) > 0 or is_full(state.board)

def makeMove(oldState, move):
    '''Transition between 2 states'''
    #The new board after the player make a move
    newBoard = deepcopy(oldState.board)
    newBoard[move[0]][move[1]] = oldState.player
    player = -oldState.player   #switch player
    return State(newBoard, player, oldState.depth + 1)


def getPossibleMoves(currentBoard):
    '''get all the moves that a player can make in the current board'''
    moves = []
    for i in range(len(currentBoard)):
        for j in range(len(currentBoard[i])):
            if currentBoard[i][j] == 0:
                moves.append((i,j))
    return moves

def minimaxCore(state, maxDepth, alpha, beta):
    '''The core logic of minimax algorithm
    Return the current state object, with the best possible move and score updated'''

    #Stop if we found a winner or if there is no more moves to make
    if (isTerminated(state)):
        return state

    if (state.depth >= maxDepth):
        return state

    possibleMoves = getPossibleMoves(state.board)
    for move in possibleMoves:
        newState = makeMove(state, move)
        result = minimaxCore(newState, maxDepth, alpha, beta)

        if result == None:
            continue

        if state.player == 1:
            #Maximizing player
            if (result.score > state.score or len(state.bestMove) == 0):
                state.bestMove = move
                state.score = result.score
                if (result.score > alpha):
                    alpha = result.score
        elif state.player == -1:
            #Minimizing player
            #if (move == (0,4)):
            #    print(state.score)
            #    print(result.score)
            #    print(result.score < state.score)
            if (result.score < state.score or len(state.bestMove) == 0):
                print("MOVE: " + str(move))
                state.bestMove = move
                state.score = result.score
                if (result.score < beta):
                    beta = result.score

        if (alpha >= beta):
            break

    return state


def minimaxSearch(currentBoard, turn, maxDepth):
    '''Return the best move using minimax algorithm
    We assume that player with code 1 is the maximizing player
    and the -1 player is the minimizing one.
    '''
    #global board, turn
    state = State(currentBoard, turn, 0)
    bestState = minimaxCore(state, maxDepth, -math.inf, math.inf)
    if (bestState != None):
        return bestState.bestMove
    else:
        return None

if __name__ == "__main__":
    #print(board)

    print(minimaxSearch(board, turn, 1))

