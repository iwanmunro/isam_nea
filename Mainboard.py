import pygame,sys,random,time, easygui
from common_functions import *
from properties import Property
from card import Card

class Character_display():
    def __init__ (self,name,img_path= None):
        pygame.init()
        self.character_name = name 
        self.icon = self.image(img_path) if img_path else None
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

class Gameboard():
    def	__init__(self,character_choices):
        self.size = (1280,720)
        self.dice_num = (1,1)
        self.characters = character_choices
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.board_original = pygame.image.load("Monopoly-board-template.png")
        pygame.display.set_caption("Gameboard")
        self.colour = (255,0,0)
        self.display = pygame.draw.rect(self.screen, self.colour, pygame.Rect(30, 30, 60, 60))
        self.playerTurn = 0
        self.current_card = None
        self.rollling = False
        

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
        self.character_objects = [Character_display(name.piece_name,f'{name.piece_name}.png') for name in self.characters]
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
                character_display = Character_display(None,None)
                view_properties =  character_display.property_button

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
                            self.current_card = Card()
                            card_event = self.current_card.draw_chance_card()
                            easygui.msgbox(msg=card_event,title="Chance card")
                            self.current_card.chance_events()
                      

                        elif community_chest_card.checkForInput(MOUSE_POSITION):
                            self.current_card = Card()
                            card_event = self.current_card.draw_community_chest_card()
                            easygui.msgbox(msg=card_event, title="Community chest card")

                        
                        elif view_properties.checkForInput(MOUSE_POSITION):
                            view_properties.Mbox("Properties","player 1")
                            print("View Properties button clicked") 

                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            print(f"Mouse clicked at ({mouse_x}, {mouse_y}) on the board.")

      
             
                pygame.display.update()

property_objs = [
    Property("Old Kent Road", 60, "images/old_kent_road.jpg", None, "Brown", None), 
    Property("Whitechapel Road", 60, "images/whitechapel_road.jpg", None, "Brown", None),
    Property("Income Tax", 0, None, None,"action", None),
    Property("Kings Cross Station", 200, "images/kings_cross_station.jpg", "Train", None, None),
    Property("The Angel Islington", 100, "images/the_angel_islington.jpg", "light_blue", None),
    Property("Chance 1", 0, None, None, "sepcial", None),
    Property("Euston Road", 100, "images/euston_road.jpg", None,"light_blue", None),
    Property("Pentonville Road", 120, "images/pentonville_road.jpg", "light_blue", False, None),
    Property("Pall Mall", 140, "images/pall_mall.jpg", "purple", False, None),
    Property("Electric Company", 150, "images/electric_company.jpg", "utilities", None),
    Property("Whitehall", 140, "images/whitehall.jpg", "purple", False, None),
    Property("Northumberland Avenue", 160, "images/northumberland_avenue.jpg", "purple", False, None),
    Property("Marylebone Station", 200, "images/marylebone_station.jpg", "train", None, None),
    Property("Bow Street", 180, "images/bow_street.jpg", "orange", False, None),
    Property("Community Chest 2", 0, None, None, "action", None),
    Property("Marlborough Street", 180, "images/marlborough_street.jpg", "orange", False, None),
    Property("Vine Street", 200, "images/vine_street.jpg", "orange", False, None),
    Property("Free Parking", 0, None, None, "free_parking", None),
    Property("Strand", 220, "images/strand.jpg", "red", False, None),
    Property("Chance 2", 0, None, None, "action", None),
    Property("Fleet Street", 220, "images/fleet_street.jpg", "red", False, None),
    Property("Trafalgar Square", 240, "images/trafalgar_square.jpg", "red", False, None),
    Property("Fenchurch Street Station", 200, "images/fenchurch_street_station.jpg", "train", None, None),
    Property("Leicester Square", 260, "images/leicester_square.jpg", "yellow", False, None),
    Property("Coventry Street", 260, "images/coventry_street.jpg", "yellow", False, None),
    Property("Water Works", 150, "images/water_works.jpg", "utilities", None),
    Property("Piccadilly", 280, "images/piccadilly.jpg", "yellow", False, None),
    Property("Go To Jail", 0, None, None, "action", None),
    Property("Regent Street", 300, "images/regent_street.jpg", "green", False, None),
    Property("Oxford Street", 300, "images/oxford_street.jpg", "green", False, None),
    Property("Community Chest 3", 0, None, None, "action", None),
    Property("Bond Street", 320, "images/bond_street.jpg", "green", False, None),
    Property("Liverpool Street Station", 200, "images/liverpool_street_station.jpg", "train", None, None),
    Property("Chance 3", 0, None, None, "action", None),
    Property("Park Lane", 350, "images/park_lane.jpg", "dark_blue", False, None),
    Property("Super Tax", 0, None, None, "action", None),
    Property("Mayfair", 400, "images/mayfair.jpg", "dark_blue", False, None)
]