import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from chess_bot import ChessBot
class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Chess')

        self.game = Game()
        self.ai = ChessBot(self.game, 'black')

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            if game.next_player=='ai':
                ai_move = self.ai.get_best_move()
                board.move(ai_move[0],ai_move[1])
                game.next_turn()
            
            for event in pygame.event.get():
                #click
                if event.type==pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY//SQUARE_SIZE
                    clicked_col = dragger.mouseX//SQUARE_SIZE

                    #if clicked square has piece, move piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        #check if the piece is valid color
                        if piece.color==game.next_player:
                            board.calc_moves(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                #mouse motion/dragging
                elif event.type==pygame.MOUSEMOTION:
                    hovered_row = event.pos[1]//SQUARE_SIZE
                    hovered_col = event.pos[0]//SQUARE_SIZE
                    game.set_hover(hovered_row,hovered_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                #release
                elif event.type==pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY//SQUARE_SIZE
                        released_col = dragger.mouseX//SQUARE_SIZE

                        #create possible move
                        initial = Square(dragger.initial_row,dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        #valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece,move)

                            board.set_true_en_passant(dragger.piece)

                            #play sound
                            game.sound_effect(captured=captured)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            
                            #next turn
                            game.next_turn()

                    dragger.undrag_piece()

                #key press
                elif event.type==pygame.KEYDOWN:
                    #change theme
                    if event.key==pygame.K_t:
                        game.change_theme()

                    if event.key==pygame.K_r:
                        game.reset()
                        game = self.game
                        screen = self.screen
                        dragger = self.game.dragger
                        board = self.game.board
                    
                    if event.key==pygame.K_a:
                        game.next_turn_ai()
                        print('Welcome to AI Mode!')

                    if event.key==pygame.K_p:
                        game.next_turn_pvp()
                        print('Welcome to PVP Mode!')

                #quit
                elif event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()