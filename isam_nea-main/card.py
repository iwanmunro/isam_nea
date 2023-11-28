import random
from common_functions import *

class Card():
    def __init__(self,total_no_players,screen,board,properties_list):
        self.num_players = total_no_players
        self.screen = screen
        self.board = board
        self.property_objs = properties_list
        self.chance_cards = [
            # "Advance to Go. Collect $200.",
            #    "Take a trip to Mayfair. If you pass Go, collect $200.",
            # "You have won a crossword competition. \n Collect $100.",
            # "Pay a $50 fine for speeding.",
            # #   "Bank error in your favor. Collect $75.",
              "Go directly to Jail. Do not pass Go. \n Do not collect $200.",]
        #     "Advance to the nearest utility. \n If unowned, you may buy it from the bank.\n If owned, throw the dice and pay the owner\n ten times the amount thrown.",
        #     "Advance to the nearest station \n and pay double the rent.",
        #     "It's your birthday! Collect $10 from each player.",
        #     "Go back three spaces.",
        #     "Pay each player $20 \n for a charity donation.",
        #     "Take a trip to King's Cross Station. \n If you pass Go, collect $200.",
        #     "Pay a $50 doctor's fee.",
        #     "You inherit $100 from a relative.",
        #     "Advance to Mayfair.\n If you pass Go, collect $200.",
        #     "Your building loan matures. Collect $150.",
        #     "You've been elected Chairman of the Board. \n Pay each player $50.",
        #     "You've won second prize in a beauty contest.\n Collect $10.",
        #     "Get caught in a property tax audit.\n Pay $25 for each house \n and $100 for each hotel you own.",
        #     "Receive a Get Out of Jail Free card.",
        #     "Pay a $100 luxury tax."
        # ]


        self.community_chest_cards = [
            "Advance to Go. Collect $200",
            "Bank error in your favor. Collect $75",
            "Doctor's fees. Pay $50",
            "Get out of Jail Free. This card may be kept until needed or sold.",
            "Grand Opera Night. Collect $50 from every player for opening night seats",
            "Holiday Fund matures. Receive $100",
            "Income tax refund. Collect $20",
            "It's your birthday. Collect $10 from every player",
            "Life insurance matures. Collect $100",
            "Pay hospital fees of $100",
            "Pay school fees of $150",
            "Receive $25 consultancy fee",
            "You are assessed for street repairs. Pay $40 per house and $115 per hotel you own",
            "You have won second prize in a beauty contest. Collect $10",
            "You inherit $100",
            "From sale of stock, you get $45",
            "Go to Jail. Go directly to Jail. Do not pass Go. Do not collect $200",
            "You have been elected chairman of the board. Pay each player $50",
            "Your building loan matures. Receive $150",
            "You have won a crossword competition. Collect $100"
        ]

        random.shuffle(self.chance_cards)
        random.shuffle(self.community_chest_cards)

        


    def draw_chance_card(self):
        drawn_card = self.chance_cards.pop(0)
        self.chance_cards.append(drawn_card)
        return drawn_card



    def draw_community_chest_card(self):
        drawn_card = self.community_chest_cards.pop(0)
        self.community_chest_cards.append(drawn_card)
        return drawn_card

    def chance_events(self, card_event, player, other_players):
        if card_event == "Advance to Go. Collect $200.":
            player.cash += 200

        elif card_event == "Take a trip to Mayfair. If you pass Go, collect $200.":
            property_pos = 39
            move_num = property_pos - player.position_int
            for i in range(move_num):
                player.move(self.board,self.screen)
                pygame.display.update()  # Ensure the display updates in each step
                pygame.time.delay(100)
            # Update the player's position after the move
    
            buy_property = Buy_property(root)
            buy_property.property_popup(self.property_objs[property_pos],player,other_players)
            player.position_int = property_pos
   

        elif card_event == "You have won a crossword competition. \n Collect $100.":
            player.cash += 100

        elif card_event == "Pay a $50 fine for speeding.":
            player.cash -= 50

        elif card_event == "Bank error in your favor. Collect $75.":
            player.cash += 75

        elif card_event ==  "Go directly to Jail. Do not pass Go. \n Do not collect $200.":
            # player.in_jail = True  
            property_pos = 10
            move_num = property_pos - player.position_int
            for i in range(move_num):
                player.move(self.board,self.screen)
                pygame.display.update()
            player.position_int = property_pos
            
        elif card_event == "Advance to the nearest utility. \n If unowned, you may buy it from the bank.\n If owned, throw the dice and pay the owner\n ten times the amount thrown.":
            utility_positions = [12,28]
            # Find the nearest utility
            nearest_utility = min(utility_positions, key=lambda x: abs(x - player.position_int)) 

            move_num = nearest_utility - player.position_int
            for i in range(move_num):
                player.move(self.board, self.screen)
                pygame.display.update()  # Ensure the display updates in each step
                pygame.time.delay(100)
            player.position_int = nearest_utility
          
            utility = self.get_current_propety(player)
            if utility.owner is None:
                pass

        elif card_event == "Advance to the nearest station \n and pay double the rent.":
            pass  #movement

        elif card_event == "It's your birthday! Collect $10 from each player.":
            player.cash += 10 * (self.num_players-1)
                
            for player in other_players:
                player.cash -= 10

        elif card_event == "Go back three spaces.":
            pass

        elif card_event ==  "Pay each player $20 \n for a charity donation.":
            player.cash -= 20 * (self.num_players-1)
            # Distribute $20 to each other player
            for player in other_players:
                player.cash += 20

        elif card_event == "Take a trip to King's Cross Station. \n If you pass Go, collect $200.":
            move_num = 5 - player.position_int
            for i in range(move_num):
                player.move(self.board,self.screen)
            player.position_int = move_num

        elif card_event == "Pay a $50 doctor's fee.":
            player.cash -= 50

        elif card_event == "You inherit $100 from a relative.":
            player.cash += 100

        elif card_event == "Advance to Mayfair.\n If you pass Go, collect $200.":
            pass #movement

        elif card_event == "Your building loan matures. Collect $150.":
            player.cash += 150

        elif card_event == "You've been elected Chairman of the Board. \n Pay each player $50.":
            player.cash -= 50 * (self.num_players-1)
            # Distribute $50 to each other player
            for player in other_players:
                player.cash += 50

        elif card_event == "You've won second prize in a beauty contest.\n Collect $10.":
            player.cash += 10

        elif card_event == "Get caught in a property tax audit.\n Pay $25 for each house \n and $100 for each hotel you own.":
            for property in player.properties:
                player.cash += (property.houses*25) + (property.hotels * 100)

        elif card_event == "Receive a Get Out of Jail Free card.":
            pass  #append jail free card to player properties

        elif card_event == "Pay a $100 luxury tax.":
            player.cash -= 100


    def community_chest_events(self,card_event, player,other_players):
        
        if card_event == "Advance to Go. Collect $200":
            player.cash += 200

        elif card_event == "Bank error in your favor. Collect $75":
            player.cash += 75

        elif card_event == "Doctor's fees. Pay $50":
            player.cash -= 50

        elif card_event == "Get out of Jail Free. This card may be kept until needed or sold":
            pass #append jail free card to player properties

        elif card_event == "Grand Opera Night. Collect $50 from every player for opening night seats":
            player.cash += (self.num_players-1)*50

        elif card_event == "Holiday Fund matures. Receive $100":
            player.cash += 100

        elif card_event == "Income tax refund. Collect $20":
            player.cash += 20

        elif card_event == "It's your birthday. Collect $10 from every player":
            player.cash += (self.num_players-1)*10
            for player in other_players:
                player.cash -= 10

        elif card_event == "Life insurance matures. Collect $100":
            player.cash += 100

        elif card_event == "Pay hospital fees of $100":
            player.cash -= 100

        elif card_event == "Pay school fees of $150":
            player.cash -= 150

        elif card_event == "Receive $25 consultancy fee":
            player.cash += 25

        elif card_event == "You are assessed for street repairs. Pay $40 per house and $115 per hotel you own":
            for property in player.properties:
                player.cash += (property.houses*40) + (property.hotels * 115)

        elif card_event == "You have won second prize in a beauty contest. Collect $10":
            player.cash += 10

        elif card_event == "You inherit $100":
            player.cash += 100

        elif card_event == "From sale of stock, you get $45":
            player.cash += 45

        elif card_event == "Go to Jail. Go directly to Jail. Do not pass Go. Do not collect $200":
            pass #mpmvement

        elif card_event == "You have been elected chairman of the board. Pay each player $50":
            player.cash -= (self.num_players-1)*50
            for player in other_players:
                player.cash += 50


        elif card_event == "Your building loan matures. Receive $150":
            player.cash += 150