import random as rand
from game import Game
from board import Board
from square import Square
from const import *
class ChessBot:
    def __init__(self, game, color) -> None:
        self.game = game
        self.color=color
    
    def get_best_move(self):
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
        
        piece = rand.choice(list(all_possible_moves.items()))[0]
        while all_possible_moves[piece] == []:
            piece = rand.choice(list(all_possible_moves.items()))[0]
        move = rand.choice(all_possible_moves[piece])
        return [piece,move]