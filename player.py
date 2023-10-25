import pygame

class Player():
    def __init__(self, player_no=None, game_piece=None, piece_name=None):
        self.player_no = player_no
        self.game_piece = game_piece
        self.piece_name = piece_name
        self.position = (0, 0)
        self.cash = 1500
        self.properties_owned = []
        self.in_jail = False
        self.player_hitbox = (self.position[0], self.position[1], 75, 55)
        self.playerTurn = 0


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
            print(self.position)
            print(board.get_size())
            if (self.position[1] > board.get_size()[1]*10.5/12 and self.position[1] < board.get_size()[1]) and self.position[0] > 0:
                self.position = ((self.position[0] - board.get_size()[0]*1/12), self.position[1]) # go left and update position
            elif self.position[1] > 0 and (self.position[0] >= 0 and self.position[0] < board.get_size()[0]*0.7/12):
                self.position = (self.position[0], (self.position[1] - board.get_size()[1]*1/12)) # go up and update position
            elif (self.position[1] >= 0 and self.position[1] < board.get_size()[0]*0.5/12) and self.position[0] < board.get_size()[0]*11/12:
                self.position = ((self.position[0] + board.get_size()[0]*1/12), self.position[1]) # go right and update position
            elif self.position[1] < board.get_size()[1] and (self.position[0] >= board.get_size()[0]*11/12 and self.position[0] < board.get_size()[0]):
                self.position = (self.position[0], (self.position[1] + board.get_size()[1]*1/12)) # go down and update position
                print(self.position)

            if self.position[0] < 0:
                self.position = (0, self.position[1])
            if self.position[1] < 0:
                self.position = (self.position[0], 0)
            if self.position[0] >= board.get_size()[0]:
                self.position = (board.get_size()[0]*11/12, 0)
            if self.position[1] >= board.get_size()[1]:
                self.position = (board.get_size()[0]*11/12, board.get_size()[1]*11/12)

            rect = self.game_piece.get_rect()
            # TODO: get_rect() of the character and just adjust coords rather than re-writing
            rect = rect.move(self.position)
            # blit the board to "remove" the previous instance of the piece
            # TODO: may need to reblit all characters unless I work out a better way to do this
            screen.blit(board, board.get_rect())
            # blit the image in its new location
            screen.blit(self.game_piece, rect)

        return screen