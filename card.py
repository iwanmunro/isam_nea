import random,pygame
from player import Player
from .Mainboard import Character_display

class Card():
    def __init__(self):
        self.chance_card_visible = False  # Add a visibility flag
        self.chance_cards = [
            "Advance to Go. Collect $200.",
            "Take a trip to Mayfair. If you pass Go, collect $200.",
            "You have won a crossword competition. Collect $100.",
            "Pay a $50 fine for speeding.",
            "Bank error in your favor. Collect $75.",
            "Go directly to Jail. Do not pass Go. Do not collect $200.",
            "Advance to the nearest utility. If unowned, you may buy it from the bank. If owned, throw the dice and pay the owner ten times the amount thrown.",
            "Advance to the nearest station and pay double the rent.",
            "It's your birthday! Collect $10 from each player.",
            "Go back three spaces.",
            "Pay each player $20 for a charity donation.",
            "Take a trip to King's Cross Station. If you pass Go, collect $200.",
            "Pay a $50 doctor's fee.",
            "You inherit $100 from a relative.",
            "Advance to Mayfair. If you pass Go, collect $200.",
            "Your building loan matures. Collect $150.",
            "You've been elected Chairman of the Board. Pay each player $50.",
            "You've won second prize in a beauty contest. Collect $10.",
            "Get caught in a property tax audit. Pay $25 for each house and $100 for each hotel you own.",
            "Receive a Get Out of Jail Free card.",
            "Pay a $100 luxury tax."
        ]


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
        if len(self.chance_cards) == 0:
            random.shuffle(self.chance_cards)
        return self.chance_cards.pop()

    def draw_community_chest_card(self):
        if len(self.community_chest_cards) == 0:
            random.shuffle(self.community_chest_cards)
        return self.community_chest_cards.pop()



    def chance_events(self,card_event, player):
        character_display = Character_display(None,None)
        if card_event == "Advance to Go. Collect $200.":
            character_display.cash += 200
            

        elif card_event ==  "Go directly to Jail. Do not pass Go. Do not collect $200.":
            player.position = None
            
        elif card_event ==  "Receive a Get Out of Jail Free card.":
            Player.properties_owned.append()


        elif card_event ==  "Pay a $50 fine for speeding.":
            Player.cash -= 50
            character_display.cash -= 50

        elif card_event ==  "Bank error in your favor. Collect $75.":
            Player.cash += 75
            character_display.cash += 75

        pygame.display.update()