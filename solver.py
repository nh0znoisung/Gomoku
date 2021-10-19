import math
from copy import deepcopy
import random
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
        '''winList = check_win(self.board)
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
            return 0'''

        halfCoeff = [0, 0, 10, 200, 500, 6000]
        openCoeff = [0, 0, 50, 500, 4800, 6000]
        totalScore = 0

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if (self.board[i][j] != 0):
                    cur = self.board[i][j]
                    #Unit vector for directions: Vertical, Horizontal and Diagonal
                    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
                    visitedLines = []
                    for vector in directions:
                        lineLen = 1
                        head = (i + vector[0], j + vector[1])
                        tail = (i - vector[0], j - vector[1])
                        headBlock = False
                        taiBlock = False

                        #Move the head in the direction of vector
                        if (not self.isOutOfRange(head)):
                            while (self.board[head[0]][head[1]] == cur):
                                lineLen += 1
                                head = (head[0] + vector[0], head[1] + vector[1])
                                if (self.isOutOfRange(head)):
                                    break

                        if (self.isOutOfRange(head)):
                            headBlock = True    #boundary block
                        elif (self.board[head[0]][head[1]] == -cur):
                            headBlock = True    #blocked by the other player

                        #Do the same thing with the tail
                        if (not self.isOutOfRange(tail)):
                            while (self.board[tail[0]][tail[1]] == cur):
                                lineLen += 1
                                tail = (tail[0] - vector[0], tail[1] - vector[1])
                                if (self.isOutOfRange(tail)):
                                    break
                        if (self.isOutOfRange(tail)):
                            taiBlock = True
                        elif (self.board[tail[0]][tail[1]] == -cur):
                            taiBlock = True

                        headTail = {head, tail}
                        if headTail not in visitedLines:
                            visitedLines.append(headTail)
                            if (lineLen > 5):
                                lineLen = 5


                            if (lineLen == 5):
                                totalScore += cur * openCoeff[lineLen]
                            elif (headBlock and taiBlock):
                                pass
                            elif (headBlock or taiBlock):
                                totalScore += cur * halfCoeff[lineLen]
                            else:
                                totalScore += cur * openCoeff[lineLen]

        return totalScore



    def isOutOfRange(self, cell):
        (x,y) = cell
        horizontal = (x < 0) or (x >= len(self.board))
        vertical = (y < 0) or (y >= len(self.board))
        return horizontal or vertical



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

    #The init bound is at the center of the board
    leftBound = 9
    rightBound = 9
    topBound = 9
    downBound = 9

    foundOccupiedCell = False

    for i in range(len(currentBoard)):
        for j in range(len(currentBoard[i])):
            if currentBoard[i][j] == 0:
                moves.append((i,j))
            else:
                #If this is the first we find occupied cells the bound will be relative to that cell.
                if (not foundOccupiedCell):
                    foundOccupiedCell = True
                    leftBound = j
                    rightBound = j
                    topBound = i
                    downBound = i

                if (j < leftBound):
                    leftBound = j
                if (j > rightBound):
                    rightBound = j
                if (i < topBound):
                    topBound = i
                if (i > downBound):
                    downBound = i

    topBound -= 2
    downBound += 2
    rightBound += 2
    leftBound -= 2

    unfilteredMoves = moves.copy()
    moves = [(i,j) for (i,j) in moves if leftBound <= j and j <= rightBound and topBound <= i and i <= downBound]
    if (len(moves) == 0):
        moves = unfilteredMoves

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
    random.shuffle(possibleMoves)   #include some randomness to the moves
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
            if (result.score < state.score or len(state.bestMove) == 0):
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
    state = State(currentBoard, turn, 0)
    bestState = minimaxCore(state, maxDepth, -math.inf, math.inf)
    if (bestState != None):
        return bestState.bestMove
    else:
        return None

if __name__ == "__main__":
    #print(board)

    print(minimaxSearch(board, turn, 1))

