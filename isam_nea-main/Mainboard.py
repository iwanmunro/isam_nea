import pygame,sys,random,time
from common_functions import *
from properties import Property
from card import Card

class Gameboard():
    def	__init__(self, character_choices, mode):
        self.player_mode = mode
        self.size = (1280,720)
        self.dice_num = (1,1)
        self.characters = character_choices
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.board_original = pygame.image.load("Monopoly-board-template.png")
        pygame.display.set_caption("Gameboard")
        self.colour = (255,0,0)
        self.display = pygame.draw.rect(self.screen, self.colour, pygame.Rect(30, 30, 60, 60))
        self.playerTurn = 0
 
        self.property_button = Button(
                    image=None,
                    pos= (1070,630),
                    text_input="View Owned Properties",
                    font= pygame.font.Font("impact.ttf", 30),
                    base_color="Black",
                    hovering_color="Green"
                )
    
        self.trade_button = Button(
                image=None,
                pos= (1070,580),
                text_input="Trade",
                font= pygame.font.Font("impact.ttf", 30),
                base_color="Black",
                hovering_color="Green"
            )

        
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

        player_num = 1
        for character in self.characters:
            if character != self.characters[0]:
                y_offset += 130
            self.screen.blit(character.game_piece, (x_coordinate,y_offset+40))
            
            #Display character cash
            font = pygame.font.Font("impact.ttf", 45)
            cash_text = font.render(f"Player {player_num}: ${character.cash}", True, "Black")
            self.screen.blit(cash_text, (x_coordinate + 60, y_offset + 47))
            player_num += 1
        
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.property_button.changeColor(MOUSE_POSITION), self.property_button.update(self.screen)
            self.trade_button.changeColor(MOUSE_POSITION), self.trade_button.update(self.screen)

        pygame.display.flip()
        pygame.display.update()


    def dice(self, num, window_size):
        return pygame.transform.scale(pygame.image.load(f"images/dice-{num}.png"), (window_size[0]/20,window_size[0]/20))


    def roll_dice(self, roll_dice_button_1, roll_dice_button_2,window_size):
        # 15 iterations of randomising ("rolling") the dice
        for i in range(15):
            self.dice_num=(random.randint(1,6),random.randint(1,6))
            roll_dice_button_1.image = self.dice(self.dice_num[0], window_size)
            roll_dice_button_2.image = self.dice(self.dice_num[1], window_size)
            roll_dice_button_1.update(self.screen)
            roll_dice_button_2.update(self.screen)
            pygame.display.update()
            time.sleep(0.1)

        self.characters[self.playerTurn].position_int = (self.characters[self.playerTurn].position_int + sum(self.dice_num)) % 40

        # moving by the dice number
        for _ in range(sum(self.dice_num)):
            self.screen = self.characters[self.playerTurn].move(self.board, self.screen)
            pygame.display.update()
            time.sleep(0.05)

    def go_to_jail(self,player):
        property_pos = 10
        move_num = property_pos - player.position_int
        for i in range(move_num):
            player.move(self.board,self.screen)
            pygame.display.update()  # Ensure the display updates in each step
            pygame.time.delay(100)
        player.position_int = property_pos
    
    def jail(self,player):
        pass

    def land_on_property(self,current_player,other_players,mode):
        curr_property = property_objs[(self.characters[self.playerTurn].position_int)]

        if mode == 'singleplayer' and self.playerTurn != 0:
            if random.random() > 0.01:
                buy_property = Buy_property(root)
                buy_property.property_popup(curr_property,current_player,other_players,singleplayer_option='buy')
            else:
                buy_property = Buy_property(root)
                buy_property.property_popup(curr_property,current_player,other_players,singleplayer_option='auction')

        else:
            if curr_property.property_group != "action" and curr_property.owner == None:
                buy_property = Buy_property(root)
                buy_property.property_popup(curr_property,current_player,other_players)

            elif curr_property.property_name == "Chance":
                card_event = self.current_card.draw_chance_card()
                chance = Card_Popup(root)
                chance.card_popup("Card chance",card_event)
                self.current_card.chance_events(card_event,current_player,other_players)

            elif curr_property.property_name == "Community Chest":
                community_chest = Card_Popup(root)
                card_event = self.current_card.draw_chance_card()
                community_chest.card_popup("Community chest",card_event)
                self.current_card.community_chest_events(card_event,current_player,other_players)

            elif curr_property.property_name == "Go To Jail":
                self.go_to_jail(player=current_player)
                current_player.in_jail = True


        #check for doubles    
        if self.dice_num[0] == self.dice_num[1]:
            self.playerTurn = self.playerTurn
        else:
            self.playerTurn = (self.playerTurn + 1) % len(self.characters)
            print(curr_property.property_name)
            print()

    def game_board(self):
            setup = True
            roll = False
            while True:
                self.screen.fill('white')
                window_size = pygame.display.get_surface().get_size()
                # use the original image to avoid resizing an already resized image making it pixelated
                self.board = pygame.transform.scale(self.board_original, (window_size[0]*2/3, window_size[1]))
                self.current_card = Card(total_no_players=len(self.characters),screen=self.screen, board=self.board,properties_list=property_objs)

                board_rect = self.board.get_rect()
                board_rect = board_rect.move((0, 0))
                self.screen.blit(self.board, board_rect)

                chance_card = Button(
                    image=pygame.transform.scale(pygame.image.load("chance_card.webp").convert_alpha(),(180,120)),
                    pos=(580,445),
                    text_input='',
                    font=pygame.font.Font("impact.ttf", 75),
                    base_color= "White",
                    hovering_color="Green"
                )

                chance_card.image = pygame.transform.rotate(chance_card.image, 45)

                community_chest_card = Button(
                    image=pygame.transform.scale(pygame.image.load("community_chest.png"),(180,120)),
                    pos=(245,190),
                    text_input='',
                    font=pygame.font.Font("impact.ttf", 75),
                    base_color= "White",
                    hovering_color="Green"
                )
                community_chest_card.image = pygame.transform.rotate(community_chest_card.image, 225)

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
                chance_card.update(self.screen),community_chest_card.update(self.screen)

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

                other_players = [i for i in self.characters if i != self.characters]
                current_player = self.characters[self.playerTurn]
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if roll_dice_button_1.checkForInput(MOUSE_POSITION) or roll_dice_button_2.checkForInput(MOUSE_POSITION):
                            roll = True

                        # #check if player is in jail
                        # elif current_player.in_jail == True:
                        #     jail = JailManager(root)
                        #     jail.jail_popup(player=current_player,dice_number=self.dice_num)


                        elif chance_card.checkForInput(MOUSE_POSITION):
                            card_event = self.current_card.draw_chance_card()
                            chance = Card_Popup(root)
                            chance.card_popup("Card chance",card_event)
                            self.current_card.chance_events(card_event,current_player,other_players)

                        elif community_chest_card.checkForInput(MOUSE_POSITION):
                            community_chest = Card_Popup(root)
                            card_event = self.current_card.draw_chance_card()
                            community_chest.card_popup("Community chest",card_event)
                            self.current_card.community_chest_events(card_event,current_player,other_players)
                
                if roll or (self.player_mode == "singleplayer" and self.playerTurn != 0):
                    self.roll_dice(roll_dice_button_1,roll_dice_button_2,window_size)
                    self.land_on_property(current_player,other_players,self.player_mode)   
                               
                roll = False
                pygame.display.update()


property_objs = [
    Property("Go", 0, None, None, "action"),
    Property("Old Kent Road", 60, "images/old_kent_road.jpg", None, "Brown"),
    Property("Community Chest", 0, None, None, "action"),
    Property("Whitechapel Road", 60, "images/whitechapel_road.jpg", None, "Brown"),
    Property("Income Tax", 0, None, None, "Tax"),
    Property("Kings Cross Station", 200, "images/kings_cross_station.jpg", None, "Train"),
    Property("The Angel Islington", 100, "images/the_angel_islington.jpg", None, "light_blue"),
    Property("Chance", 0, None, None, "action"),
    Property("Euston Road", 100, "images/euston_road.jpg", None, "light_blue"),
    Property("Pentonville Road", 120, "images/pentonville_road.jpg", None, "light_blue"),
    Property("Jail", 0, None, None, "action"),
    Property("Pall Mall", 140, "images/pall_mall.jpg", None, "pink"),
    Property("Electric Company", 150, "images/electric_company.jpg", None, "utilities"),
    Property("Whitehall", 140, "images/whitehall.jpg", None, "pink"),
    Property("Northumberland Avenue", 160, "images/northumberland_avenue.jpg", None, "pink"),
    Property("Marylebone Station", 200, "images/marylebone_station.jpg",None, "train"),
    Property("Bow Street", 180, "images/bow_street.jpg",None, "orange"),
    Property("Community Chest", 0, None, None, "action"),
    Property("Marlborough Street", 180, "images/marlborough_street.jpg",None, "orange"),
    Property("Vine Street", 200, "images/vine_street.jpg", None, "orange"),
    Property("Free Parking", 0, None, None, "action"),
    Property("Strand", 220, "images/strand.jpg", None, "red"),
    Property("Chance", 0, None, None, "action"),
    Property("Fleet Street", 220, "images/fleet_street.jpg", None, "red"),
    Property("Trafalgar Square", 240, "images/trafalgar_square.jpg", None, "red"),
    Property("Fenchurch Street Station", 200, "images/fenchurch_station.jpg", None, "train"),
    Property("Leicester Square", 260, "images/leicester_square.jpg", None, "yellow"),
    Property("Coventry Street", 260, "images/coventry_street.jpg", None, "yellow"),
    Property("Water Works", 150, "images/water_works.jpg", None, "utilities"),
    Property("Piccadilly", 280, "images/piccadilly.jpg", None, "yellow"),
    Property("Go To Jail", 0, None, None, "action"),
    Property("Regent Street", 300, "images/regent_street.jpg", None, "green"),
    Property("Oxford Street", 300, "images/oxford_street.jpg", None, "green"),
    Property("Community Chest", 0, None, None, "action"),
    Property("Bond Street", 320, "images/bond_street.jpg", None, "green"),
    Property("Liverpool Street Station", 200, "images/liverpool_station.jpg", None, "train"),
    Property("Chance", 0, None, None, "action"),
    Property("Park Lane", 350, "images/park_lane.jpg", None, "dark_blue"),
    Property("Super Tax", 0, None, None, "Tax"),
    Property("Mayfair", 400, "images/mayfair.jpg", None, "dark_blue")
]
