import pygame, sys, random
from common_functions import Button
from player import Player
from Mainboard import Gameboard
from card import Card
from network import Network

class Transactions:
    pass

class MonopolyGame():
    def __init__(self):
        pygame.init()
        n = Network()
        self.screen = pygame.display.set_mode((1280,720))
        # Initialize the number of players
        pygame.display.set_caption("Monopoly Menu")

        self.background = pygame.image.load("background.jpg")
        self.character_selections = {1:'Top hat', 2:'Car',3:'dog',4:'Battleship',5:'WheelBarrow',6:'Iron'}
        self.num_players = None
        self.saved_selections = []
        self.num_online_players = 2
        self.num_local_players = 2
        self.isOnlineMode = False

    def load_image(self, img_path, desired_size=(250, 250)):
        # Load the original image
        original_image = pygame.image.load(img_path)
        # Scale the original image to the desired size using smoothscale
        scaled_image = pygame.transform.smoothscale(original_image, desired_size)
        return scaled_image
    
    def get_font(self, size):
        return pygame.font.Font("impact.ttf", size)
    
    def get_no_players(self,num_players):
        return num_players

    def character_selection(self, mode='multiplayer'):
        #total number of players playing
        if self.isOnlineMode:
            total_no_players = self.num_players
        else:
            total_no_players = self.num_players


        #player number which changes dynamically after every selection
        player_num = 0
        #player text on screen which changes after every selection
        player_num_char = 1
        #characters selection being stored in a dictionary
        characters = {
            1: self.load_image("top hat.png"),
            2: self.load_image("car.png"),
            3: self.load_image("dog.png"),
            4: self.load_image("battleship.png"),
            5: self.load_image("wheelbarrow.png"),
            6: self.load_image("iron.png")
        }

        # Initialize character selection index
        current_character_index = 1
        
        while True:
            CHARACTER_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.fill("black")

            start_game_button = Button(
                image=None,
                pos=(640, 380),
                text_input="Start game",
                font=self.get_font(60),
                base_color="White",
                hovering_color="Green"
                )

            if (len(self.saved_selections) == total_no_players and mode=='multiplayer') or \
                (len(self.saved_selections) == total_no_players+1 and mode=='singleplayer'):
                #creating start game button which will appear once all the characters have been selected
                start_game_button.changeColor(CHARACTER_MOUSE_POS)
                start_game_button.update(self.screen)

            elif len(self.saved_selections) == 1 and mode=='singleplayer':
                for _ in range(total_no_players):
                    current_character_index = random.choice(list(characters.keys()))

                    self.saved_selections.append(
                        Player(
                            player_no=len(self.saved_selections)+1,
                            game_piece=characters[current_character_index],
                            piece_name=self.character_selections[current_character_index]
                        )
                    )
                    del characters[current_character_index]
            else:
                character_text = self.get_font(60).render(f'Player {player_num_char} choose your character:', True, 'White')
                CHARACTER_RECT = character_text.get_rect(center=(640, 150))
                self.screen.blit(character_text, CHARACTER_RECT)

                CHARACTER_BACK = Button(
                    image=None,
                    pos=(530, 620), 
                    text_input="Back", 
                    font=self.get_font(30), 
                    base_color="White", 
                    hovering_color="Green"
                )

                CHARACTER_BACK.changeColor(CHARACTER_MOUSE_POS).update(self.screen)
                
                #select button that will dissapear once all players have selected their character
                select_button = Button(
                    image=None,
                    pos=(725, 620),
                    text_input="Select",
                    font=self.get_font(30),
                    base_color="White",
                    hovering_color="Green"
                    )
                select_button.changeColor(CHARACTER_MOUSE_POS)
                select_button.update(self.screen)

                # Buttons to switch characters
                switch_right = Button(
                    image=None,
                    pos=(800, 410), 
                    text_input=">",
                    font=self.get_font(100),
                    base_color="White",
                    hovering_color="Green"
                    )

                switch_left = Button(
                    image=None,
                    pos=(480, 410), 
                    text_input="<",
                    font=self.get_font(100),
                    base_color="White",
                    hovering_color="Green"
                    )
            
                switch_right.changeColor(CHARACTER_MOUSE_POS).update(self.screen)
                switch_left.changeColor(CHARACTER_MOUSE_POS).update(self.screen)

                while current_character_index not in characters.keys():
                    current_character_index = (current_character_index + 1) % (len(characters)+1)

                self.screen.blit(characters[current_character_index], (520, 270)) 
                select_button.update(self.screen)
        
            #event handler for character selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHARACTER_BACK.checkForInput(CHARACTER_MOUSE_POS):
                        self.saved_selections = []
                        self.multi_player()
                    elif switch_left.checkForInput(CHARACTER_MOUSE_POS):           
                        current_character_index = (current_character_index - 1) % (len(characters)+1)
                    elif switch_right.checkForInput(CHARACTER_MOUSE_POS):
                        current_character_index = (current_character_index + 1) % (len(characters)+1)
                    elif select_button.checkForInput(CHARACTER_MOUSE_POS):
                        if player_num <= total_no_players:
                            self.saved_selections.append(Player(
                                                            player_no=len(self.saved_selections)+1,
                                                            game_piece=characters[current_character_index],
                                                            piece_name=self.character_selections[current_character_index]
                                                        ))
            
                            
                            del characters[current_character_index]
                            player_num += 1
                            
                            if player_num_char < total_no_players:
                                player_num_char += 1
                        
    
                            character_text = self.get_font(200).render(f'{player_num}', True, "White")                  

                    elif start_game_button.checkForInput(CHARACTER_MOUSE_POS):
                        game = Gameboard(self.saved_selections, mode)
                        game.game_board()
                        total_players = Card(total_no_players)
                        total_players.chance_events()
        
            pygame.display.update()


    def play(self, mode="multiplayer"):
        if mode == 'singleplayer':
            self.num_players = 1
        else:
            self.num_players = self.num_local_players
        while True:
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.screen.fill("black") 

            if mode == 'multiplayer':
                no_player_text = self.get_font(60).render("Select the number of players:", True, 'White')
            elif mode == 'singleplayer':
                no_player_text = self.get_font(60).render("Select the number of NPCs:", True, 'White')

            NO_OF_PLAYERS_RECT = no_player_text.get_rect(center=(640, 150))

            self.screen.blit(no_player_text, NO_OF_PLAYERS_RECT)

            no_player_text = self.get_font(200).render(f'{self.num_players}', True, "White")
            NO_OF_PLAYERS_RECT = no_player_text.get_rect(center=(640, 400))

            self.screen.blit(no_player_text, NO_OF_PLAYERS_RECT)

            # Buttons to increase/decrease the number of players to begin the game
            num_increase = Button(
                image=None,
                pos=(800, 410),
                text_input="+",
                font=self.get_font(150),
                base_color="White",
                hovering_color="Green"
            )
            num_increase.changeColor(MOUSE_POSITION)
            num_increase.update(self.screen)

            num_decrease = Button(
                image=None,
                pos=(480, 410),
                text_input="-",
                font=self.get_font(150),
                base_color="White",
                hovering_color="Green"
                
            )
            num_decrease.changeColor(MOUSE_POSITION)
            num_decrease.update(self.screen)
    
            #back_button
            PLAY_BACK_BUTTON = Button(
                image=None,
                pos=(530, 620),
                text_input='Back',
                font=self.get_font(30),
                base_color="White",
                hovering_color="Green"
            )
            PLAY_BACK_BUTTON.changeColor(MOUSE_POSITION)
            PLAY_BACK_BUTTON.update(self.screen)

            #Advance button
            START_BUTTON = Button(
                image=None,
                pos=(725, 620),
                text_input='Advance',
                font=self.get_font(30),
                base_color="White",
                hovering_color="Green"
            )
            START_BUTTON.changeColor(MOUSE_POSITION)
            START_BUTTON.update(self.screen)

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if num_increase.checkForInput(MOUSE_POSITION):
                        if (self.num_players < 5 and mode=='multiplayer') or (self.num_players < 4 and mode=='singleplayer'):
                            self.num_players += 1
                            no_player_text = self.get_font(200).render(f'{self.num_players}', True, "White")
                    elif num_decrease.checkForInput(MOUSE_POSITION):
                        if (self.num_players > 2 and mode=='multiplayer') or (self.num_players > 1 and mode=='singleplayer'):
                            self.num_players -= 1
                            no_player_text = self.get_font(200).render(f'{self.num_players}', True, "White")
                    elif PLAY_BACK_BUTTON.checkForInput(MOUSE_POSITION):
                        self.isOnlineMode = False
                        self.main_menu()
                    elif START_BUTTON.checkForInput(MOUSE_POSITION):
                        if not self.isOnlineMode:
                            self.character_selection(mode)
                        else:
                            self.waiting_room()

            pygame.display.update()

        
    def waiting_room(self):
        while True:
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.screen.fill("white")

            online_text = self.get_font(45).render("Waiting for other players...", True, "Black")
            TUTORIAL_RECT = online_text.get_rect(center=(640, 130))
            self.screen.blit(online_text, TUTORIAL_RECT)

            BACK_BUTTON = Button(
                image=None,
                pos=(640, 660),
                text_input="BACK",
                font=self.get_font(50),
                base_color="Black",
                hovering_color="Green"
            )

            BACK_BUTTON.changeColor(MOUSE_POSITION)
            BACK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.isOnlineMode = False
                    self.main_menu()

            pygame.display.update()


    def main_menu(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            MOUSE_POSITION = pygame.mouse.get_pos()

            menu_text = self.get_font(100).render("MONOPOLY", True, "#FF0000")
            menu_rect = menu_text.get_rect(center=(640, 100))
            monopoly_man = pygame.transform.scale(pygame.image.load('monopoly_man.png'),(300,370))

            SINGLEPLAYER_BUTTON = Button(
                image= None,
                pos=(640, 250),
                text_input="SINGLEPLAYER",
                font=self.get_font(75),
                base_color="#FFFFFF",
                hovering_color="red"
            )

            MULTIPLAYER_BUTTON = Button(
                image= None,
                pos=(640, 400), 
                text_input="MULTIPLAYER",
                font=self.get_font(75),
                base_color="#FFFFFF",
                hovering_color="red"
            )
    
            QUIT_BUTTON = Button(
                image= self.load_image("images/button_rect.png",(300,80)),
                pos=(640, 550),
                text_input="QUIT",
                font=self.get_font(60),
                base_color="#FFFFFF",
                hovering_color="red"
            )

            self.screen.blit(menu_text, menu_rect)	
            self.screen.blit(monopoly_man,(120,220))
            
            for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE_POSITION)
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(MOUSE_POSITION):
                        self.play("singleplayer")
                    if MULTIPLAYER_BUTTON.checkForInput(MOUSE_POSITION):
                        self.play("multiplayer")
                    if QUIT_BUTTON.checkForInput(MOUSE_POSITION):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


if __name__ == "__main__":
    game = MonopolyGame()
    game.main_menu()


