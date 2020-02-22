# file:     eval_funcs.py
# author:   <your_umbc_email_here>
# date:     02/20/2020
# desc:     Evaluation functions for a chess board, used to drive minimax-ab.

# imports
import chess
import random
from datetime import datetime
import consts

# test_eval() returns a random board evaluation in [-10, 10]
# @param board  a python-chess board object containing the current board state
# @return       a number representing the evaluation of the current board state.
#               NOTE: negative evaluations are good for the minimizing player
#               and vice versa. the scale of your evaluations is up to you.
#               NOTE: the player who goes first is always the maximizing player,
#               and when playing chess, white goes first.
def test_eval(board):
    return random.seed(datetime.now()).uniform(-100, 100)

def count_pieces(board):
    total = 0
    points = {1: 1,  #pawn = 1 point
              2: 3,  #knight = 3 points
              3: 3,  #bishop = 3 points
              4: 5,  #rook = 4 points
              5: 9,  #queen = 9 points
              6: 100 #king = priceless
              }
    for square in chess.SQUARES:
        if board.piece_at(square) is not None:
            value = points.get(board.piece_at(square).piece_type)
            # if piece = white
            if board.piece_at(square).color is True:
                total += value
            # if piece = black
            if board.piece_at(square).color is False:
                total -= value
    #print(total)
    return total

# TODO(y'all):  implement two more evaluation functions, one more thorough than
#               the other. Use the function test_eval() as shown above as a
#               template.
