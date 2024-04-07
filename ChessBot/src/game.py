import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
class Game:
    def __init__(self) -> None:
        self.next_player = 'white'
        self.hovered_sqr = None
        self.ai_mode = False
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    #show methods
    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                #color
                color = theme.bg.light if (row+col)%2==0 else theme.bg.dark
                #rect
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                #render
                pygame.draw.rect(surface, color, rect)

                #row coordinates
                if col==0:
                    #color
                    color = theme.bg.dark if row%2==0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(str(ROWS-row),1,color)
                    lbl_pos = (5,5+row*SQUARE_SIZE)
                    surface.blit(lbl,lbl_pos)
                if row==7:
                    color = theme.bg.dark if (row+col)%2==0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(Square.get_alphacol(col),1,color)
                    lbl_pos = (col*SQUARE_SIZE+SQUARE_SIZE-20,HEIGHT-20)
                    surface.blit(lbl,lbl_pos)

    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                #check if piece on that square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    #all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture()
                        img = pygame.image.load(piece.texture)
                        img_center = col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img,piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            #loop through all possible moves
            for move in piece.moves:
                #create a color for valid squares
                color = theme.moves.light if (move.final.row+move.final.col)%2==0 else theme.moves.dark
                #create rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                #draw
                pygame.draw.rect(surface,color,rect)
    
    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]:
                #color
                color = theme.trace.light if (pos.row+pos.col)%2==0 else theme.trace.dark
                #rect
                rect = (pos.col*SQUARE_SIZE, pos.row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                #render
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            #color
            color = (120, 120, 120)
            #rect
            rect = (self.hovered_sqr.col*SQUARE_SIZE, self.hovered_sqr.row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            #render
            pygame.draw.rect(surface, color, rect, width=3)

    #other methods
    def next_turn(self):
        if self.ai_mode:
            self.next_player = 'white' if self.next_player=='ai' else 'ai'
        else:
            self.next_player = 'white' if self.next_player=='black' else 'black'
    
    def next_turn_ai(self):
        self.ai_mode = True
    
    def next_turn_pvp(self):
        self.ai_mode = False
    
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
    
    def sound_effect(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()