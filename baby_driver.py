#! /usr/bin/env python3
# file:     baby_driver.py
# author:   nevitt1@umbc.edu
# date:     02/02/2020
# desc:     python3 minmax-ab implementation for use with chess eval functions,
#           CMSC471 project 1.

# imports
import chess
import random
from eval_funcs import *
# minimax() runs an iteration of minimax-ab with the specified max depth
# @param depth          set to the maximum depth we want to evaluate, decreases
#                       over recursions until it reaches 0 at the bottom of the
#                       tree.
# @param board          the python-chess board object at the root node.
# @param alpha          the alpha value we're using. You can play with this.
# @param beta           the beta value we're using. You can play with this too.
# @param is_maximizing  is the current iteration the maximizing player?
# @param eval_func      the evaluation function used to evaluate the current
#                       position.
# @return               A 2-tuple containing the score of the subtree and its
#                       respective move.
def minimax(depth, board, alpha, beta, is_maximizing, eval_func):
    # end the recursion if this is the maximum depth we want to reach
    if depth == 0:
        if board.result() == "1-0":
            return (float("inf"), board.peek())
        if board.result() == "0-1":
            return (float("-inf"), board.peek)
        return (-eval_func(board), board.peek())

    # populate the possible moves that can be made from the current board state
    possible_moves = []
    # iterate through the generator because we can only shuffle a list
    for move in board.legal_moves:
        possible_moves.append(move)
    # shuffle the order of the moves
    random.shuffle(possible_moves)

    # if we're the maximizing player
    if is_maximizing:
        # track the current best move. start with the worst move imaginable.
        best_score = float("-inf")
        best_move = None

        # iterate over all available moves
        for x in possible_moves:
            # commit the move to the board state
            move = chess.Move.from_uci(str(x))
            board.push(move)

            # recurse to find the best move
            pair = minimax(depth - 1, board, alpha, beta, not is_maximizing, eval_func)
            best_score = max(best_score, pair[0])
            if pair[0] == best_score:
                best_move = board.peek()
            board.pop()
            alpha = max(alpha, best_score)

            # prune the sub-tree via alpha-beta
            if beta <= alpha:
                return (best_score, best_move)

        # return the best move we found
        return (best_score, best_move)

    # if we're the minimizing player
    else:
        # track the current best move. start with the worst move imaginable.
        best_score = float("inf")
        best_move = None

        # iterate over all available moves
        for x in possible_moves:
            # commit the move to the board state
            move = chess.Move.from_uci(str(x))
            board.push(move)

            # recurse to find the best move
            pair = minimax(depth - 1, board, alpha, beta, not is_maximizing, eval_func)
            best_score = min(best_score, pair[0])
            if pair[0] == best_score:
                best_move = board.peek()
            board.pop()
            beta = min(beta, best_score)

            # prune the sub-tree via alpha-beta
            if(beta <= alpha):
                return (best_score, best_move)

        # return the best move we found
        return (best_score, best_move)

# play_game() pits two ai's against each other in a game of chess
# @param white_eval     The evaluation function to be used by the white team.
# @param white_depth    The search depth to be used by the white team.
# @param black_eval     The evaluation function to be used by the black team.
# @param black_depth    The search depth to be used by the white team.
# @return               A string containing the result of the game, in points.
def play_game(white_eval, white_depth, black_eval, black_depth):
    board = chess.Board()

    # while the game is still going, play it
    while not board.is_game_over():
        # if it's white's turn
        if board.turn == chess.WHITE:
            # determine the best move to make via minimax-ab
            best_pair = minimax(white_depth, board, float("inf"), float("-inf"), True, white_eval)
            # make that move and pass the turn
            board.push(best_pair[1])
        # if it's black's turn
        else:
            # determine the best move to make via minimax-ab
            best_pair = minimax(black_depth, board, float("-inf"), float("inf"), False, black_eval)
            # make that move and pass the turn
            board.push(best_pair[1])
        # print the board at the end of each turn
        # print(board)
        # print("----------------")
    # print the final board state and return the result of the game
    # print(board)
    return board.result()

# main() is the entry point
def main():
    #code for generating all variations
    output = open('output.csv', 'w')
    depths = [2,4,6]
    functs = [eval_countpieces, eval_weightpieces, thorough_eval]
    combos = []
    # generate all 9 combinations
    for i in range(3):
        for j in range(3):
            pair = (depths[i], functs[j])
            combos.append(pair)

    for k in range(len(combos)):
        #generate all matchups
        for l in range(1,len(combos)):
            print(str('combination: ' + str(k) + ' vs combination: '
                 + str((k + l) % len(combos)) + '\n' + 'results: '))

            output.write(str('combination: '+ str(k) + ' vs combination: '
                        + str((k+l)%len(combos)) + '\n' + 'results: '))
            # each matchup plays 2 games twice (4 total)
            results = []
            for m in range(2):
                results.append(play_game(combos[k][1], combos[k][0],
                combos[(k+l) % len(combos)][1], combos[(k+l) % len(combos)][0]))
            output.write(tally_score(results) + ',\n')
            print(tally_score(results) + ',\n')

#gives result string based on a series of games
def tally_score(results):
    white_wins = 0
    black_wins = 0
    for i in range(len(results)):
        try:
            white_score = int(results[i].split('-')[0], 10)
            black_score = int(results[i].split('-')[1], 10)
        except:
            white_score = 0.5
            black_score = 0.5
        white_wins += white_score
        black_wins += black_score
    return str(white_wins) + ' - ' + str(black_wins)

# python is a dirty language and this is necessary
if __name__ == "__main__":
        main()
