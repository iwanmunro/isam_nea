import pygame
from properties import Property

class Player():
    def __init__(self, player_no=None, game_piece=None, piece_name=None,):
        self.player_no = player_no
        self.game_piece = game_piece
        self.piece_name = piece_name
        self.position = (0, 0)
        self.properties = []
        self.in_jail = False
        self.position_int = 0
        self.cash = 1500
        self.houses = 0
        self.hotels = 0

    def image(self,img_path):
        img_path = f"{self.game_piece}.png"
        return pygame.transform.scale(pygame.image.load(img_path), (60,60))
    
    def move(self, board, screen, mode="move"):
        if mode == "setup":
            self.game_piece = pygame.transform.scale(self.game_piece, (board.get_size()[0]/1/12, board.get_size()[1]/12))
            rect = self.game_piece.get_rect()
            rect = rect.move((board.get_size()[0]*11/12, board.get_size()[1]*11/12))
            self.position = (board.get_size()[0]*11/12, board.get_size()[1]*11/12)
            screen.blit(self.game_piece, rect)

        elif mode == "update":
            rect = self.game_piece.get_rect()
            rect = rect.move(self.position)
            screen.blit(self.game_piece, rect)

        else:
            if ((board.get_size()[0]-self.position[0])/board.get_size()[0])*100 < 10 and ((board.get_size()[1]-self.position[1])/board.get_size()[1])*100 < 10 or \
                ((board.get_size()[0]-self.position[0])/board.get_size()[0])*100 == 100 and ((board.get_size()[1]-self.position[1])/board.get_size()[1])*100 < 10:
                multiplier = 8
            elif ((board.get_size()[0]-self.position[0])/board.get_size()[0])*100 == 100 and ((board.get_size()[1]-self.position[1])/board.get_size()[1])*100 == 100 or \
                ((board.get_size()[0]-self.position[0])/board.get_size()[0])*100 < 10 and ((board.get_size()[1]-self.position[1])/board.get_size()[1])*100 == 100:
                multiplier = 7.5
            else:
                multiplier = 12

            if (self.position[1] >= board.get_size()[1]*11/12 and self.position[1] < board.get_size()[1]) and self.position[0] > 0:
                self.position = ((self.position[0] - board.get_size()[0]*1/multiplier), self.position[1]) # go left and update position
            elif self.position[1] > 0 and (self.position[0] >= 0 and self.position[0] < board.get_size()[0]*0.5/12):
                self.position = (self.position[0], (self.position[1] - board.get_size()[1]*1/multiplier)) # go up and update position
            elif (self.position[1] >= 0 and self.position[1] < board.get_size()[0]*0.5/12) and self.position[0] < board.get_size()[0]*11/12:
                self.position = ((self.position[0] + board.get_size()[0]*1/multiplier), self.position[1]) # go right and update position
            elif self.position[1] < board.get_size()[1] and (self.position[0] >= board.get_size()[0]*10.5/12 and self.position[0] < board.get_size()[0]):
                self.position = (self.position[0], (self.position[1] + board.get_size()[1]*1/multiplier)) # go down and update position

            if self.position[0] < 0:
                self.position = (0, self.position[1])
                self.move(board, screen)
            if self.position[1] < 0:
                self.position = (self.position[0], 0)
                self.move(board, screen)
            if self.position[0] > board.get_size()[0]*11/12:
                self.position = (board.get_size()[0]*11/12, 0)
                self.move(board, screen)
            if self.position[1] > board.get_size()[1]*11/12:
                self.position = (board.get_size()[0]*11/12, board.get_size()[1]*11/12)
                self.move(board, screen)

            rect = self.game_piece.get_rect()
            rect = rect.move(self.position)
            screen.blit(board, board.get_rect())
            # blit the image in its new location
            screen.blit(self.game_piece, rect)

        return screen
    

