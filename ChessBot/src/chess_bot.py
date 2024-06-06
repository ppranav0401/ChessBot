import random as rand
from game import Game
from board import Board
from square import Square
import copy
from const import *
class ChessBot:
    def __init__(self, game, color) -> None:
        self.game = game
        self.color=color
    
    def get_random_move(self):
        all_possible_moves = {}
        board = self.game.board
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    p = board.squares[row][col].piece
                    if p.color==self.color:
                        all_possible_moves[p]=[]
                        board.calc_moves(p, row, col, bool=True)
                        for move in p.moves:
                            all_possible_moves[p].append(move)
                    p.clear_moves()
        piece = rand.choice(list(all_possible_moves.items()))[0]
        while all_possible_moves[piece] == []:
            piece = rand.choice(list(all_possible_moves.items()))[0]
        move = rand.choice(all_possible_moves[piece])
        all_possible_moves={}
        return [piece,move]

    def get_best_move(self):
        maxScore = 10000
        bestMove = []
        board = copy.deepcopy(self.game.board)
        #print(board.scoreBoardMaterial())
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    p = copy.deepcopy(board.squares[row][col].piece)
                    print(p,p.color)
                    if p.color==self.color:
                        board.calc_moves(p, row, col, bool=True)
                        for move in p.moves:
                            board.move(p,move,testing=True)
                            score = board.scoreBoardMaterial()
                            #print(score)
                            if score <= maxScore:
                                maxScore = score
                                bestMove.append(p)
                                bestMove.append(move)
                    p.clear_moves()
        return bestMove
    