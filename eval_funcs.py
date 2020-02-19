# file:     eval_funcs.py
# author:   <your_umbc_email_here>
# date:     02/20/2020
# desc:     Evaluation functions for a chess board, used to drive minimax-ab.

# imports
import chess
import random

# test_eval() returns a random board evaluation in [-10, 10]
# @param board  a python-chess board object containing the current board state
# @return       a number representing the evaluation of the current board state.
#               NOTE: negative evaluations are good for the minimizing player
#               and vice versa. the scale of your evaluations is up to you.
#               NOTE: the player who goes first is always the maximizing player,
#               and when playing chess, white goes first.
def test_eval(board):
    return random.uniform(-100, 100)

# TODO(y'all):  implement two more evaluation functions, one more thorough than
#               the other. Use the function test_eval() as shown above as a
#               template.

# piece_to_pts() returns a point evaluation for a given python-chess piece.
# @param piece  a python-chess piece object of the piece to be evaluated.
#               NOTE: Cannot be None or it'll break. Catch those elsewhere.
# @return       the number of points that piece is worth, according to standard
#               valuations dating back to the 18th century.
def piece_to_pts(piece):
    # fetch the symbol for the piece
    charcode = piece.symbol().lower()
    # giant if-else block to handle all the pieces
    if charcode == 'p':
        return 1
    if charcode == 'b':
        return 3
    if charcode == 'n':
        return 3
    if charcode == 'r':
        return 5
    if charcode == 'q':
        return 9
    if charcode == 'k':
        return 1
    return 0

# eval_countpieces() returns a board-state evaluation based only on piece values
# @param board  a python-chess board object containing the board state to be
#               evaluated.
# @return       the evaluation of the board state, with positive values good
#               for white and negative values good for black.
def eval_countpieces(board):
    # running total of our evaluation of this board state
    score = 0

    # Iterate over every square on the board
    for square in chess.SQUARES:
        # Get the piece that resides there
        piece = board.piece_at(square)
        # If the square is empty, ignore it
        if piece == None:
            continue
        # Get the point value of that piece
        piece_pts = piece_to_pts(piece)
        # if the piece is a white piece, add its value. Otherwise, subtract it.
        if piece.color:
            score += piece_pts
        else:
            score -= piece_pts
    # return the final score
    return score
