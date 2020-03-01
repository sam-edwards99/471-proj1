# file:     eval_funcs.py
# author:   <your_umbc_email_here>
# date:     02/20/2020
# desc:     Evaluation functions for a chess board, used to drive minimax-ab.

# imports
import chess
import math
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

# linear_dist() returns the linear distance between two vectors
# @param a  a 2-tuple containing the x and y components of a vector
# @param b  a 2-tuple containing the x and y components of another vector
# @return   the magnitude of the difference between those vectors
def linear_dist(a, b):
    return math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2))

# eval_weightpieces()   returns a board-state evaluation based on piece values
#                       and their positions relative to the center of the board
# @param board  a python-chess board object containing the board state to be
#               evaluated.
# @return       the evaluation of the board state, with positive values good
#               for white and negative values good for black.
def eval_weightpieces(board):
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
        # get the distance between that piece and the center of the board
        # NOTE: 1-dist because pieces closer to the center are better
        # NOTE: the values for square are integers. They go accross from the
        #       bottom-right at A1 and wrap up a row at the end. Therefore,
        #       (square % 8) is the x-coord of a square and (square / 8) is the
        #       y-coord of a square.
        # NOTE: we divide by 5 because that's the max distance from the middle
        dist_weight = 1 - linear_dist((square % 8, square / 8), (4.5, 4.5)) / 5
        dist_weight *= 2
        # if the piece is a white piece, add its value. Otherwise, subtract it.
        if piece.color:
            score += piece_pts * dist_weight
        else:
            score -= piece_pts * dist_weight
    # return the final score
    return score

def count_checkers(board):
    points_per_checker = 3
    board.checkers()

def protect_king(board):
    point_per_protector = 1
    protectors = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        if piece.symbol().lower() == 'k' and piece.color:
            squares = [square + 7, square + 8, square + 9]
            for i in range(3):
                #try:
                if board.piece_at(squares[i]) is not None and board.piece_at(squares[i]).color:
                    protectors += 1
                #except:
                    #break
        elif piece.symbol().lower() == 'k' and not piece.color:
            squares = [square - 7, square - 8, square - 9]
            for i in range(3):
                # try:
                if board.piece_at(squares[i]) is not None and not board.piece_at(squares[i]).color:
                    protectors -= 1
                #except:
                    #break
    return protectors * point_per_protector

def bishop_pair(board):
    points_per_pair = 1
    white_bishops = 0
    black_bishops = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        if piece.symbol().lower() == 'b' and piece.color:
            white_bishops += 1
        elif piece.symbol().lower() == 'b' and not piece.color:
            black_bishops += 1
    if white_bishops == 2 and black_bishops < 2:
        return points_per_pair
    elif black_bishops == 2 and white_bishops > 2:
        return -points_per_pair
    else:
        return 0

def pawn_promotion(board):
    promotion_dist_weight = 1
    promotion_total = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        if piece.symbol().lower() == 'p' and piece.color:
            rank = square / 8
            promotion_total += (1 - ((8 - rank) / 8)) * promotion_dist_weight
        elif piece.symbol().lower() == 'p' and not piece.color:
            rank = square / 8
            promotion_total -= -(1 - (rank / 8)) * promotion_dist_weight
    return promotion_total

def get_possible_moves(board):
    points_per_move = 0.02
    return points_per_move * board.legal_moves.count()


def thorough_eval(board):
    score = 0
    score += eval_weightpieces(board)
    score += protect_king(board)
    score += pawn_promotion(board)
    score += get_possible_moves(board)
    score += count_checkers(board)
    return score


# TODO(y'all):  implement one more evaluation function, more-thorough than just
#               counting pieces and/or weighting their positions like in the
#               above examples.
