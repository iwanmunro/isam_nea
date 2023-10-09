import time
import pygame

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.visible = True # Add a 'visible' attribute and set it to True
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
   

    def update(self, screen):
        if self.visible:  # Check if the button is not disabled
            if self.image is not None:
                screen.blit(self.image, self.rect)
                screen.blit(self.text, self.text_rect)
        return self
                
    def checkForInput(self, position):
        if self.visible and position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        return self

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True


class Player():
    def __init__(self, player_no=None, game_piece=None, piece_name=None):
        self.player_no = player_no
        self.game_piece = game_piece
        self.piece_name = piece_name
        self.position = (0, 0)

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
            if (self.position[1] > board.get_size()[1]*10.5/12 and self.position[1] < board.get_size()[1]) and self.position[0] > 0:
                self.position = ((self.position[0] - board.get_size()[0]*1/12), self.position[1]) # go left and update position
            elif self.position[1] > 0 and (self.position[0] >= 0 and self.position[0] < board.get_size()[0]*0.5/12):
                self.position = (self.position[0], (self.position[1] - board.get_size()[1]*1/12)) # go up and update position
            elif (self.position[0] >= 0 and self.position[0] < board.get_size()[0]*0.5/12) and self.position[0] < board.get_size()[0]:
                self.position = ((self.position[0] + board.get_size()[0]*1/12), self.position[1]) # go right and update position
            elif self.position[1] < board.get_size()[1] and (self.position[0] >= 0 and self.position[0] < board.get_size()[0]*0.5/12):
                self.position = (self.position[0], (self.position[1] + board.get_size()[1]*1/12)) # go down and update position

            if self.position[0] < 0:
                self.position = (0, self.position[1])
            if self.position[1] < 0:
                self.position = (self.position[0], 0)

            rect = self.game_piece.get_rect()
            # TODO: get_rect() of the character and just adjust coords rather than re-writing
            rect = rect.move(self.position)
            # blit the board to "remove" the previous instance of the piece
            # TODO: may need to reblit all characters unless I work out a better way to do this
            screen.blit(board, board.get_rect())
            # blit the image in its new location
            screen.blit(self.game_piece, rect)

        return screen