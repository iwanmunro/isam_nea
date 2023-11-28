
class Property():
    def __init__(self, name,price,img_path,owner,property_group):
        self.property_name = name
        self.price = price
        self.owner = owner
        self.image = img_path
        self.property_group = property_group
        self.mortgage_status = False
        self.houses = 0
        self.hotels = 0

        
    def land_on_property(self):
        pass

    def calculate_rent(self):
        pass
        
    def add_houses(self):
        pass

    def add_hotel(self):
        pass 

    def auction(self):
        pass