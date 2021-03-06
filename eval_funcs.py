# file:     eval_funcs.py
# author:   nevitt1@umbc.edu
# date:     02/20/2020
# desc:     Evaluation functions for a chess board, used to drive minimax-ab.

# imports
import chess
import math
import random
from datetime import datetime

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
            score += math.fabs(piece_pts * dist_weight)
        else:
            score -= math.fabs(piece_pts * dist_weight)

    # return the final score
    return score

# gives a score based on the number of pieces placing king in check
def count_checkers(board):
    points_per_checker = 0.6
    checkers = board.checkers()
    if len(checkers) == 0:
        return 0
    #the more pieces we have checking opponent the better
    elif board.piece_at(checkers.pop()).color:
        return (len(checkers) + 1) * points_per_checker
    # the more pieces opponent has checking us the worse
    else:
        return (-(len(checkers) + 1)) * points_per_checker

# gives a score based on the number of friendly pieces in front of king
def protect_king(board):
    point_per_protector = 0.4
    protection = 0
    #it is desirable to have friendly pieces ahead of your king
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        if piece.symbol().lower() == 'k' and piece.color:
            #counts friendly pieces in 3 squares ahead of king in next rank
            squares = [square + 7, square + 8, square + 9]
            for i in range(3):
                #cover out of bounds cases
                try:
                    if board.piece_at(squares[i]) is not None and board.piece_at(squares[i]).color:
                        protection += 1
                except:
                    break
        elif piece.symbol().lower() == 'k' and not piece.color:
            squares = [square - 7, square - 8, square - 9]
            if square/8 == 7 or square/8 == 8:
                protection -= 3
            for i in range(3):
                try:
                    if board.piece_at(squares[i]) is not None and not board.piece_at(squares[i]).color:
                        protection -= 1
                except:
                    break
    return protection * point_per_protector

# gives a score based on whether one side has a pair of bishops and another does not
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
    # if we have a pair of bishops and opponent doesn't, thats good
    if white_bishops == 2 and black_bishops < 2:
        return points_per_pair
    # if opponent has a pair of bishops and we don't, thats bad
    elif black_bishops == 2 and white_bishops > 2:
        return -points_per_pair
    else:
        return 0

# gives a score based on the proximity of pawns to reaching promotion
def pawn_promotion(board):
    promotion_dist_weight = 0.05
    promotion_total = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        #we want our pieces to reach the opposite side
        if piece.symbol().lower() == 'p' and piece.color:
            rank = square / 8
            promotion_total += (1 - ((8 - rank) / 8)) * promotion_dist_weight
        #we dont want enemy pieces to reach our side
        elif piece.symbol().lower() == 'p' and not piece.color:
            rank = square / 8
            promotion_total -= (1 - (rank / 8)) * promotion_dist_weight
    return promotion_total

# gives score based on how free the board is based on available legal moves
def get_possible_moves(board):
    points_per_move = 0.04
    #we want to open up the board with more possible moves
    return points_per_move * board.legal_moves.count()

# gives a bonus score based on whether of not the player has castled
def has_castled(board):
    castling_points = 0.4
    total = 0
    #if white hasn't castled, thats bad, we want to castle
    if bool(board.castling_rights & chess.BB_A1) and bool(board.castling_rights & chess.BB_A8):
        total -= castling_points
    else:
        total += castling_points
    #if black hasn't castled, thats good, we dont want them to castle
    if bool(board.castling_rights & chess.BB_H1) and bool(board.castling_rights & chess.BB_H8):
        total += castling_points
    else:
        total -= castling_points
    return total

# gives a score based on a combination of the above helper functions
def thorough_eval(board):
    score = 0
    score += eval_weightpieces(board)
    score += protect_king(board)
    score += pawn_promotion(board)
    score += get_possible_moves(board)
    score += count_checkers(board)
    score += has_castled(board)
    return score

