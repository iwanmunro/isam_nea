import pygame, sys, time, random
from common_functions_2 import Button, Player


class Character():
    def __init__ (self,name,img_path):
        pygame.init()
        self.character_name = name 
        self.icon = self.image(img_path)
        self.character_position = (720,50)
        self.cash = 1500
        self.property_button = Button(
                image=None,
                pos= (1068,600),
                text_input="View Owned Properties",
                font= pygame.font.Font("impact.ttf", 35),
                base_color="Black",
                hovering_color="Green"
            )
    def image(self,img_path):
        img_path = f"{self.character_name}.png"
        return pygame.transform.scale(pygame.image.load(img_path), (60,60))


class GameBoard():
    def __init__(self, character_choices):
        self.size = (1280,720)
        self.dice_num = (1,1)
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.characters = character_choices
        self.playerTurn = 0
        self.board_original = pygame.image.load("Monopoly-board-template.png")
        pygame.display.set_caption("Gameboard")  
        self.properties_coordinates = {
            "Go": (1100, 675),
            "Mediterranean Avenue": (995, 675),
            "Community Chest 1": (910, 675),
            "Baltic Avenue": (825, 675),
            "Income Tax": (735, 675),
            "Reading Railroad": (650, 675),
            "Oriental Avenue": (565, 675),
            "Chance 1": (480, 675),
            "Vermont Avenue": (395, 675),
            "Connecticut Avenue": (310, 675),
            "Jail": (225, 675),
            "St. Charles Place": (130, 675),
            "Electric Company": (45, 675),
            "States Avenue": (10, 590),
            "Virginia Avenue": (10, 505),
            "Pennsylvania Railroad": (10, 420),
            "St. James Place": (10, 335),
            "Community Chest 2": (10, 250),
            "Tennessee Avenue": (10, 165),
            "New York Avenue": (10, 80),
            "Free Parking": (10, 10),
            "Kentucky Avenue": (95, 10),
            "Chance 2": (180, 10),
            "Indiana Avenue": (265, 10),
            "Illinois Avenue": (350, 10),
            "B. & O. Railroad": (435, 10),
            "Atlantic Avenue": (520, 10),
            "Ventnor Avenue": (605, 10),
            "Water Works": (690, 10),
            "Marvin Gardens": (775, 10),
            "Go To Jail": (860, 10),
            "Pacific Avenue": (945, 10),
            "North Carolina Avenue": (1030, 10),
            "Community Chest 3": (1115, 10),
            "Pennsylvania Avenue": (1190, 10),
            "Short Line": (1255, 95),
            "Chance 3": (1255, 180),
            "Park Place": (1255, 265),
            "Luxury Tax": (1255, 350),
            "Boardwalk": (1255, 435)
        }
    
    def get_property_name(self,property_coord):
        return self.properties_coordinates.get(property_coord,None)


    def character_info(self):
        # Define the size and position of the rectangle
        window_size = pygame.display.get_surface().get_size()
        rect_width = window_size[0] // 3  # One-third of the window width
        rect_height = window_size[1]
        rect_x = (2 * window_size[0]) // 3  # One-third from the right-hand side
        rect_y = 0

        #create display background
        colour = (152,251,152)
        pygame.draw.rect(self.screen, colour, pygame.Rect(rect_x, rect_y, rect_width, rect_height))
        
        x_coordinate = 875
        y_offset = 20

        # Create objects for each characters
        self.character_objects = [Character(name.piece_name,f'{name.piece_name}.png') for name in self.characters]
        player_num = 1
        for character in self.character_objects:
            if character != self.character_objects[0]:
                y_offset += 130
            self.screen.blit(character.icon, (x_coordinate,y_offset+40))
            
            #Display character cash
            font = pygame.font.Font("impact.ttf", 45)
            cash_text = font.render(f"Player {player_num}: ${character.cash}", True, "Black")
            self.screen.blit(cash_text, (x_coordinate + 60, y_offset + 47))
            player_num += 1
        
            #Drwaiing a button to display player properties
            property_button = character.property_button
            MOUSE_POSITION = pygame.mouse.get_pos()
            property_button.changeColor(MOUSE_POSITION)
            property_button.update(self.screen)

        pygame.display.flip()
        pygame.display.update()


    def dice(self, num, window_size):
        return pygame.transform.scale(pygame.image.load(f"images/dice-{num}.png"), (window_size[0]/20,window_size[0]/20))


    def game_board(self):
        setup = True
        while True:
            self.screen.fill('white')
            window_size = pygame.display.get_surface().get_size()
            # use the original image to avoid resizing an already resized image making it pixelated
            self.board = pygame.transform.scale(self.board_original, (window_size[0]*2/3, window_size[1]))

            board_rect = self.board.get_rect()
            board_rect = board_rect.move((0, 0))
            self.screen.blit(self.board, board_rect)

            #chance card
            chance_card = Button(
                image=pygame.transform.scale(pygame.image.load("chance_card.webp"),(200,140)),
                pos=(270,230),
                text_input='',
                font=pygame.font.Font("impact.ttf", 75),
                base_color= "White",
                hovering_color="Green"
            )

            community_chest_card = Button(
                image=pygame.transform.scale(pygame.image.load("community_chest.png"),(200,140)),
                pos=(570,500),
                text_input='',
                font=pygame.font.Font("impact.ttf", 75),
                base_color= "White",
                hovering_color="Green"
            )

            roll_dice_button_1 = Button(
                image=pygame.transform.scale(pygame.image.load(f"images/dice-{self.dice_num[0]}.png"), (window_size[0]/20,window_size[0]/20)),
                pos=(((window_size[0]-400)/2)-50, (620/2)+50),
                text_input='',
                font=pygame.font.Font("impact.ttf", 75),
                base_color="White",
                hovering_color="Green"
            )

            roll_dice_button_2 = Button(
                image=pygame.transform.scale(pygame.image.load(f"images/dice-{self.dice_num[1]}.png"), (window_size[0]/20,window_size[0]/20)),
                pos=(((window_size[0]-400)/2)+25, (620/2)+50),
                text_input='',
                font=pygame.font.Font("impact.ttf", 75),
                base_color="White",
                hovering_color="Green"
            )

            MOUSE_POSITION = pygame.mouse.get_pos()

            chance_card.changeColor(MOUSE_POSITION), chance_card.update(self.screen)
            community_chest_card.changeColor(MOUSE_POSITION), community_chest_card.update(self.screen)

            roll_dice_button_1.changeColor(MOUSE_POSITION).update(self.screen)
            roll_dice_button_2.changeColor(MOUSE_POSITION).update(self.screen)

            if setup == True:
                # bring characters into the game
                mode = "setup"
                setup = False
            else:
                mode = "update"

            for i in self.characters:
                self.screen = i.move(self.board, self.screen, mode=mode)

            self.character_info()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if roll_dice_button_1.checkForInput(MOUSE_POSITION) or roll_dice_button_2.checkForInput(MOUSE_POSITION):
                        # 15 iterations of randomising ("rolling") the dice
                        for i in range(15):
                            self.dice_num=(random.randint(1,6),random.randint(1,6))
                            roll_dice_button_1.image = self.dice(self.dice_num[0], window_size)
                            roll_dice_button_2.image = self.dice(self.dice_num[1], window_size)
                            roll_dice_button_1.update(self.screen)
                            roll_dice_button_2.update(self.screen)
                            pygame.display.update()
                            time.sleep(0.1)

                        # moving by the dice number
                        for _ in range(sum(self.dice_num)):
                            self.screen = self.characters[self.playerTurn].move(self.board, self.screen)
                            pygame.display.update()
                            time.sleep(0.25)


                        self.playerTurn = (self.playerTurn + 1) % len(self.characters)

                    elif chance_card.checkForInput(MOUSE_POSITION):
                        pass
                    elif community_chest_card.checkForInput(MOUSE_POSITION):
                        pass

            pygame.display.update()

class Transactions:
    pass

class MonopolyGame():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280,720))
        # Initialize the number of players
        self.num_players = 2
        pygame.display.set_caption("Monopoly Menu")

        self.background = pygame.image.load("background.jpg")
        self.character_selections = {1:'Top hat', 2:'Car',3:'Dog',4:'Battleship',5:'WheelBarrow',6:'Iron'}

        self.saved_selections = []

    def load_image(self,img_path):
        return pygame.transform.scale(pygame.image.load(img_path), (250,250))

    def get_font(self, size):
        return pygame.font.Font("impact.ttf", size)

    def get_no_players(self,num_players):
        return num_players

    def character_selection(self):
        #total number of players playing
        TOTAL_NO_PLAYERS = self.num_players

        #player number which changes dynamically after every selection
        player_num = 0
        #player text on screen which changes after every selection
        player_num_char = 1
        #characters selection being stored in a dictionary
        characters = {
            1: self.load_image("Top hat.png"),
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
                pos=(600, 320),
                text_input="Begin game",
                font=self.get_font(60),
                base_color="White",
                hovering_color="Green"
            )

            if len(self.saved_selections) == TOTAL_NO_PLAYERS:
                #creating start game button which will appear once all the characters have been selected
                start_game_button.changeColor(CHARACTER_MOUSE_POS)
                start_game_button.update(self.screen)
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

                self.screen.blit(characters[current_character_index], (520, 270))  # Adjust position as needed
                select_button.update(self.screen)

            #event handler for character selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHARACTER_BACK.checkForInput(CHARACTER_MOUSE_POS):
                        self.play()
                    elif switch_left.checkForInput(CHARACTER_MOUSE_POS):
                        current_character_index = (current_character_index - 1) % (len(characters)+1)
                    elif switch_right.checkForInput(CHARACTER_MOUSE_POS):
                        current_character_index = (current_character_index + 1) % (len(characters)+1)
                    elif select_button.checkForInput(CHARACTER_MOUSE_POS):
                        if player_num < TOTAL_NO_PLAYERS:
                            self.saved_selections.append(Player(
                                                            player_no=len(self.saved_selections)+1,
                                                            game_piece=characters[current_character_index],
                                                            piece_name=self.character_selections[current_character_index]
                                                            )
                                                        )

                            del characters[current_character_index]

                            player_num += 1
                            if player_num_char < TOTAL_NO_PLAYERS:
                                player_num_char += 1
                    elif start_game_button.checkForInput(CHARACTER_MOUSE_POS):
                        game = GameBoard(self.saved_selections)
                        game.game_board()

            pygame.display.flip()
            pygame.display.update()


    def play(self):
        while True:
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.screen.fill("black")

            no_player_text = self.get_font(60).render("Select the number of players:", True, 'White')
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
                        if self.num_players < 6:
                            self.num_players += 1
                            no_player_text = self.get_font(200).render(f'{self.num_players}', True, "White")
                    elif num_decrease.checkForInput(MOUSE_POSITION):
                        if self.num_players > 2:
                            self.num_players -= 1
                            no_player_text = self.get_font(200).render(f'{self.num_players}', True, "White")
                    elif PLAY_BACK_BUTTON.checkForInput(MOUSE_POSITION):
                        self.main_menu()
                    elif START_BUTTON.checkForInput(MOUSE_POSITION):
                        self.character_selection()

                pygame.display.update()


    def options(self):
        while True:
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.screen.fill("white")

            TUTORIAL_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
            TUTORIAL_RECT = TUTORIAL_TEXT.get_rect(center=(640, 260))
            self.screen.blit(TUTORIAL_TEXT, TUTORIAL_RECT)

            TUTORIAL_BACK = Button(
                image=None,
                pos=(640, 460),
                text_input="BACK",
                font=self.get_font(75),
                base_color="Black",
                hovering_color="Green"
            )

            TUTORIAL_BACK.changeColor(MOUSE_POSITION)
            TUTORIAL_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.main_menu()

            pygame.display.update()


    def main_menu(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            MOUSE_POSITION = pygame.mouse.get_pos()

            menu_text = self.get_font(100).render("MONOPOLY", True, "#FF0000")
            menu_rect = menu_text.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(
                image= None,
                pos=(640, 250), 
                text_input="PLAY",
                font=self.get_font(75),
                base_color="#FFFFFF",
                hovering_color="red"
            )

            TUTORIAL_BUTTON = Button(
                image= None,
                pos=(640, 400),
                text_input="TUTORIAL",
                font=self.get_font(75),
                base_color="#FFFFFF",
                hovering_color="red"
            )

            QUIT_BUTTON = Button(
                image= None,
                pos=(640, 550),
                text_input="QUIT",
                font=self.get_font(75),
                base_color="#FFFFFF",
                hovering_color="red"
            )

            self.screen.blit(menu_text, menu_rect)

            for button in [PLAY_BUTTON, TUTORIAL_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE_POSITION)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MOUSE_POSITION):
                        self.play()
                    if TUTORIAL_BUTTON.checkForInput(MOUSE_POSITION):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MOUSE_POSITION):
                        pygame.quit()
                        sys.exit()

                pygame.display.update()

class Property():
    def __init__(self, name,price,coord, owner, mortgage_status):
        self.property_name = name
        self.price = price
        self.owner = owner
        self.properties = []
        self.mortgage_status = mortgage_status
        self.coord = coord
    
    def image(self,img_path):
        img_path = f"{self.property_name}.png"
        return pygame.transform.scale(pygame.image.load(img_path), (250,250))
    
    def calculate_rent(self):
        pass
        
    def add_houses(self):
        pass

    def add_hotel(self):
        pass 


chance_cards = [
    "Advance to Go. Collect $200.",
    "Go directly to Jail. Do not pass Go. Do not collect $200.",
    "Receive a Get Out of Jail Free card.",
    "Pay a $50 fine for speeding.",
    "Bank error in your favor. Collect $75.",
    "Pay a $100 luxury tax.",
    "You have won a crossword competition. Collect $100.",
    "Advance to the nearest railroad and pay double the rent.",
    "It's your birthday! Collect $10 from each player.",
    "Go back three spaces.",
    "Pay each player $20 for a charity donation.",
    "Take a trip on the Reading Railroad. If you pass Go, collect $200.",
    "Pay a $50 doctor's fee.",
    "You inherit $100 from a relative.",
    "Advance to Boardwalk. If you pass Go, collect $200.",
    "Your building loan matures. Collect $150.",
    "You've been elected Chairman of the Board. Pay each player $50.",
    "You've won second prize in a beauty contest. Collect $10.",
    "Advance to the nearest utility. If unowned, you may buy it from the bank. If owned, throw the dice and pay owner ten times the amount thrown.",
    "Get caught in a property tax audit. Pay $25 for each house and $100 for each hotel you own."
]

community_chest_cards = [
    "Advance to Go. Collect $200.",
    "Bank error in your favor. Collect $75.",
    "Doctor's fees. Pay $50.",
    "Get out of Jail Free. This card may be kept until needed or sold.",
    "Grand Opera Night. Collect $50 from every player for opening night seats.",
    "Holiday Fund matures. Receive $100.",
    "Income tax refund. Collect $20.",
    "It's your birthday. Collect $10 from every player.",
    "Life insurance matures. Collect $100.",
    "Pay hospital fees of $100.",
    "Pay school fees of $150.",
    "Receive $25 consultancy fee.",
    "You are assessed for street repairs. Pay $40 per house and $115 per hotel you own.",
    "You have won second prize in a beauty contest. Collect $10.",
    "You inherit $100.",
    "From sale of stock, you get $45.",
    "Go to Jail. Go directly to Jail. Do not pass Go. Do not collect $200.",
    "You have been elected chairman of the board. Pay each player $50.",
    "Your building loan matures. Receive $150.",
    "You have won a crossword competition. Collect $100."
]

property_objects = [
    Property("Go", 0, (1100, 675), None, False),
    Property("Mediterranean Avenue", 60, (995, 675), None, False),
    Property("Community Chest 1", 0, (910, 675), None, False),
    Property("Baltic Avenue", 60, (825, 675), None, False),
    Property("Income Tax", 0, (735, 675), None, False),
    Property("Reading Railroad", 200, (650, 675), None, False),
    Property("Oriental Avenue", 100, (565, 675), None, False),
    Property("Chance 1", 0, (480, 675), None, False),
    Property("Vermont Avenue", 100, (395, 675), None, False),
    Property("Connecticut Avenue", 120, (310, 675), None, False),
    Property("Jail", 0, (225, 675), None, False),
    Property("St. Charles Place", 140, (130, 675), None, False),
    Property("Electric Company", 150, (45, 675), None, False),
    Property("States Avenue", 140, (10, 590), None, False),
    Property("Virginia Avenue", 160, (10, 505), None, False),
    Property("Pennsylvania Railroad", 200, (10, 420), None, False),
    Property("St. James Place", 180, (10, 335), None, False),
    Property("Community Chest 2", 0, (10, 250), None, False),
    Property("Tennessee Avenue", 180, (10, 165), None, False),
    Property("New York Avenue", 200, (10, 80), None, False),
    Property("Free Parking", 0, (10, 10), None, False),
    Property("Kentucky Avenue", 220, (95, 10), None, False),
    Property("Chance 2", 0, (180, 10), None, False),
    Property("Indiana Avenue", 220, (265, 10), None, False),
    Property("Illinois Avenue", 240, (350, 10), None, False),
    Property("B. & O. Railroad", 200, (435, 10), None, False),
    Property("Atlantic Avenue", 260, (520, 10), None, False),
    Property("Ventnor Avenue", 260, (605, 10), None, False),
    Property("Water Works", 150, (690, 10), None, False),
    Property("Marvin Gardens", 280, (775, 10), None, False),
    Property("Go To Jail", 0, (860, 10), None, False),
    Property("Pacific Avenue", 300, (945, 10), None, False),
    Property("North Carolina Avenue", 300, (1030, 10), None, False),
    Property("Community Chest 3", 0, (1115, 10), None, False),
    Property("Pennsylvania Avenue", 320, (1190, 10), None, False),
    Property("Short Line", 200, (1255, 95), None, False),
    Property("Chance 3", 0, (1255, 180), None, False),
    Property("Park Place", 350, (1255, 265), None, False),
    Property("Luxury Tax", 0, (1255, 350), None, False),
    Property("Boardwalk", 400, (1255, 435), None, False),
]



if __name__ == "__main__":
    game = MonopolyGame()
    game.main_menu()