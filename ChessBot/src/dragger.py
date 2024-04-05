import pygame
from const import *
class Dragger:
    def __init__(self) -> None:
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    #update image
    def update_blit(self, surface):
        #update texture
        self.piece.set_texture(size=128)

        #create image
        img = pygame.image.load(self.piece.texture)

        #image center
        img_center = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)

        #draw image
        surface.blit(img,self.piece.texture_rect)
    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos #pos is a tuple (xcor, ycor)
    
    def save_initial(self,pos):
        self.initial_row = pos[1]//SQUARE_SIZE
        self.initial_col = pos[0]//SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        self.piece = None
        self.dragging = False
