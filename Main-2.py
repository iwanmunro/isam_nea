from typing import Self
import pygame, sys, time, random
from button import Button


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
	def	__init__(self,saved_selections):
		self.size = (1280,720)
		self.saved_selections = saved_selections
		self.dice_num = (1,1)
		self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.board_original = pygame.image.load("Monopoly-board-template.png")
		pygame.display.set_caption("Gameboard")
		self.colour = (255,0,0)
		self.display = pygame.draw.rect(self.screen, self.colour, pygame.Rect(30, 30, 60, 60))
		
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
		self.character_objects = [Character(name,f'{name}.png') for name in self.saved_selections]
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
	

	def display_popup(self,card_info):
		popup_width = 400
		popup_height = 200
		popup_x = (self.screen.get_width() - popup_width) // 2
		popup_y = (self.screen.get_height() - popup_height) // 2

		pygame.draw.rect(self.screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height))
		
		# Display card event information (customize this part)
		font = pygame.font.Font(None, 36)
		text_surface = font.render(card_info, True, (0, 0, 0))
		text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
		self.screen.blit(text_surface, text_rect)

	def game_board(self):
		setup = True
		while True:
			self.screen.fill('white')
			window_size = pygame.display.get_surface().get_size()
			# use the original image to avoid resizing an already resized image making it pixelated
			self.board = pygame.transform.scale(self.board_original, (window_size[0]*2/3, window_size[1]))
			rect = self.board.get_rect()
			rect = rect.move((0, 0))
			self.screen.blit(self.board, rect)
			
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
			
			MOUSE_POSITION = pygame.mouse.get_pos()
			chance_card.changeColor(MOUSE_POSITION), chance_card.update(self.screen)
			community_chest_card.changeColor(MOUSE_POSITION), community_chest_card.update(self.screen)
			
		   

			# game dice
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
			roll_dice_button_1.changeColor(MOUSE_POSITION), roll_dice_button_1.update(self.screen)
			roll_dice_button_2.changeColor(MOUSE_POSITION), roll_dice_button_2.update(self.screen)
		   

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if roll_dice_button_1.checkForInput(MOUSE_POSITION) or roll_dice_button_2.checkForInput(MOUSE_POSITION):
						for i in range(15):
							self.dice_num=(random.randint(1,6),random.randint(1,6))
							roll_dice_button_1.image = self.dice(self.dice_num[0], window_size)
							roll_dice_button_2.image = self.dice(self.dice_num[1], window_size)
							roll_dice_button_1.update(self.screen)
							self.character_info()
							roll_dice_button_2.update(self.screen)
							self.character_info()
							pygame.display.update()
							time.sleep(0.1)
					elif chance_card.checkForInput(MOUSE_POSITION):
						self.display_popup('Card info')
						chance_card.update(self.screen)
					elif community_chest_card.checkForInput(MOUSE_POSITION):
						pass
			self.character_info()
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
		self.character_selections = {1:'Top hat', 2:'Car',3:'dog',4:'Battleship',5:'WheelBarrow',6:'Iron'}
		
		self.saved_selections = []

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

	def character_selection(self):
		#total number of players playing
		TOTAL_NO_PLAYERS = self.num_players

		selected_characters = []

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
				pos=(640, 380),
				text_input="Start game",
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
						self.saved_selections = []
						print(selected_characters)
						self.play()
					elif switch_left.checkForInput(CHARACTER_MOUSE_POS):
						current_character_index = (current_character_index - 1) % (len(characters)+1)
					elif switch_right.checkForInput(CHARACTER_MOUSE_POS):
						current_character_index = (current_character_index + 1) % (len(characters)+1)
					elif select_button.checkForInput(CHARACTER_MOUSE_POS):
						if player_num < TOTAL_NO_PLAYERS:
							self.saved_selections.append(self.character_selections[current_character_index])

							del characters[current_character_index]

							player_num += 1
							if player_num_char < TOTAL_NO_PLAYERS:
								player_num_char += 1
							if len(self.saved_selections) >= TOTAL_NO_PLAYERS:
								select_button.update(self.screen)
	
							character_text = self.get_font(200).render(f'{player_num}', True, "White")                  

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
			# monopoly_man = pygame.transform.scale(pygame.image.load('monopoly_man.png'),(300,370))

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
			# self.screen.blit(monopoly_man,(120,220))
			
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


if __name__ == "__main__":
	game = MonopolyGame()
	game.main_menu()