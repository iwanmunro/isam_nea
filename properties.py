import pygame

class Property():
    def __init__(self, name,price,img_path,owner,property_group,coord):
        self.property_name = name
        self.price = price
        self.owner = owner
        self.image = self.property_image(img_path)
        self.property_group = property_group
        self.mortgage_status = False
        self.houses = 0
        self.hotels = 0
        self.coord = coord
        
    
    def property_image(self, img_path):
        if img_path is not None:
            return pygame.transform.scale(pygame.image.load(img_path), (250, 250))
        else:
            return None

    
    def land_on_property(self):
        pass

    def calculate_rent(self):
        pass
        
    def add_houses(self):
        pass

    def add_hotel(self):
        pass 

