import tkinter as tk
import pygame
from tkinter import *
from tkinter import messagebox as m_box
from PIL import ImageTk, Image

root = tk.Tk()  

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
   

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)
        return self
                
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

        return self 

 
class Popup():
    def __init__(self,root):
        self.root = root

    def create_popup(self, title, width, height):
        popup = tk.Toplevel()
        popup.title(title)
        self.root.withdraw()
        popup.geometry(f"{width}x{height}")
        return popup
    
    def exit_popup(self, popup):
        popup.destroy()


class Card_Popup(Popup):
    def __init__(self,root):
        super().__init__(root)

    def card_popup(self,title,text):
        pop = self.create_popup(title,400,200)

        pop_label = tk.Label(pop, text=text, font= ("Courier 22 bold",12,"bold"))
        pop_label.pack(pady = 50)
        
        def exit_btn():
            self.exit_popup(pop)

        ok_button = tk.Button(pop, text = "Ok", font = ("Helvetica",12), command=exit_btn)
        ok_button.pack()
        pop.wait_window()


class Buy_property(Popup):
    def __init__(self,root):
        super().__init__(root)
        
        self.highest_bidder = None
        self.current_bid = 0
        self.remaining_time = 5
        self.timer_id = None

     # Create a pop-up window for auction setup
    def property_popup(self,property,player,total_no_players,singleplayer_option=None):
        pop = self.create_popup("Property purchase",700,500)
    
        def buy_property():
            if player.cash > property.price:
                player.cash -= property.price
                player.properties.append(property)
                property.owner = player
                self.exit_popup(pop)
             
        if singleplayer_option == 'buy' and player.cash > property.price:
            buy_property()
        elif singleplayer_option == 'auction' or (singleplayer_option == 'buy' and player.cash < property.price):
            self.auction_setup(player,total_no_players,property,pop)
        else:
            #display the property image on the screen
            property_image = Image.open(property.image)
            resized_image = property_image.resize((200, 350))
            # Create a PhotoImage object from the resized image
            property_image = ImageTk.PhotoImage(resized_image)


            label = tk.Label(pop, image = property_image)
            label.pack()

            #create the buttons to buy and auction the propety if unowned
            buy_button = tk.Button(pop,text="Buy", font="bold", command= buy_property)
            buy_button.pack(side="top", padx=30)
            auction_button = tk.Button(pop, text="Auction", font="bold", command=lambda: [self.auction_setup(player,total_no_players,property,pop),self.exit_popup(pop)])
            auction_button.pack(side="top",padx=60 )
            pop.wait_window()


    def auction_setup(self,player,total_no_players,property,property_popup):
        # Close the property popup
        self.exit_popup(property_popup)
        # Create a pop-up window for auction setup
        pop = self.create_popup("Auction setup",500,200)

        # Label for bidding instructions
        bidding_label = tk.Label(pop, text=f"Player {player.player_no}, enter your starting bidding price:", font=("helvetica", 12, "bold"))
        bidding_label.pack(pady=10)

        # Entry boxes for starting price
        bid_var = tk.StringVar()
        entry = tk.Entry(pop, width=20, textvariable=bid_var)
        entry.pack(pady=20)
    

        def submit():
            # Handle input validation before starting the auction
            starting_price = bid_var.get()
            if starting_price == '':
                m_box.showerror('Error', 'Please enter a value')
            else:
                try:
                    starting_price = int(starting_price)
                    if starting_price > player.cash:
                        m_box.showerror('Error', "You don't have enough cash")
                    else:
                        pop.grab_release()
                        # Call the auction function
                        self.auction(entry, total_no_players, property, player, property_popup)
                        # Destroy the widgets after the auction function call
                        entry.destroy()
                        submit_button.destroy()
                        pop.destroy()
                except ValueError:
                    m_box.showerror('Error', 'You can only enter digits')


        # Create a "Submit" button to initiate the auction setup
        submit_button = tk.Button(pop, text="Submit", command= submit)
        submit_button.pack(pady=30)

        # Display the auction setup pop-up and wait for it to close
        pop.wait_window()




    def auction(self,entry,total_no_players,property,player,property_popup):
        # Create the main auction window

        pop2 = self.create_popup("Auction",700,500)
        # Get the starting price
        starting_price = int(entry.get())

        # Label for the timer
        timer_label = tk.Label(pop2, text="", font=("Helvetica", 16))
        timer_label.pack(pady=30)

        # Label to display the current bid
        price_label = tk.Label(pop2, text=f'${starting_price}', font=("Beryllium", 45))
        price_label.pack(pady=50)

        # Label to display the highest bidder
        self.highest_bidder = player
        highest_bidder_label = tk.Label(pop2, text=f"Highest bidder: Player {self.highest_bidder.player_no}", font=("Helvetica", 16, "bold"))
        highest_bidder_label.pack(pady=30)

        self.current_bid = starting_price
    
        def increase_bid(player_idx):
            # Increase the current bid and reset the imer
            self.current_bid += 20    
            self.highest_bidder = total_no_players[player_idx-1]  
            price_label.config(text=f'${self.current_bid}')
            highest_bidder_label.config(text=f"Highest bidder: Player {self.highest_bidder.player_no}")
            reset_timer()
            
        player_buttons = []
        # Create bid buttons for each player
        for i in range(1, len(total_no_players)+1):
            player_button = tk.Button(pop2, text=f"P{i} (Bid +$20)", font="bold", command=lambda i=i: increase_bid(i))
            player_button.pack(side="left",padx=30)
            player_buttons.append(player_button)
        
        def reset_timer():
            # Reset the timer to 5 seconds and immediately start the countdown
            self.remaining_time = 5
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            update_timer()

        def update_timer():
            # Update the timer display and continue the countdown
            if self.remaining_time > 0:
                timer_label.config(text=f"Countdown: {self.remaining_time} seconds", font=("Helvetica", 20, "bold"))
                self.timer_id = self.root.after(1000, update_timer)
                self.remaining_time -= 1
            #handle what happens when the timer runs out 
            else:
                timer_label.config(text="Time's up!")
                timer_label.config(text=f"Times up! \n Player {self.highest_bidder.player_no} you have won {property.property_name} for:")
                self.highest_bidder.cash -= self.current_bid
                self.highest_bidder.properties.append(property)
                print(self.highest_bidder.player_no)
                print(self.current_bid)
                print("Player's cash:", self.highest_bidder.cash)

                pygame.display.update()

                for button in player_buttons:
                    button.destroy()
                    close_button = tk.Button(pop2, text = "Close",  font=("Helvetica", 16,), command=lambda: [self.exit_popup(property_popup), self.exit_popup(pop2)])
                    close_button.pack(pady= 40)

        pop2.wait_window()

            
          
class JailManager(Popup):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
    
    def jail_popup(self, player,dice_number):
        player.in_jail = True 
        pop = self.create_popup("Jail manager",400,300)


        #label for jai rules

        #display the property image on the screen
        jail_image = Image.open("images/jail.png")
        resized_image = jail_image.resize((300, 350))
        # Create a PhotoImage object from the resized image
        jail_image = ImageTk.PhotoImage(resized_image)

        label = tk.Label(pop, image = jail_image)
        label.pack()

        def leave_jail():
            player.in_jail = False

        def handle_jail_turn():
            if dice_number[0] == dice_number[1]:
                leave_jail()
            else:
                player.position_int = 10
            
        #create the buttons to buy and auction the propety if unowned
        roll_button = tk.Button(pop,text="Roll", font="bold", command= handle_jail_turn)
        roll_button.pack(side="top", padx=30)
        pay_fee_button = tk.Button(pop, text="Auction", font="bold", command= leave_jail)
        pay_fee_button.pack(side="top",padx=60 )
        pop.wait_window()  





















class Negotiations():
    def __init__(self):
        self.root = tk.Tk()
    
    def negotiation(self,total_no_players):
        pop = tk.Toplevel()
        pop.title("Negotiation window")
    
    def offer_trade(self):
        pass
    
    def submit_trade(self):
        pass

    def accept_trade(self):
        pass