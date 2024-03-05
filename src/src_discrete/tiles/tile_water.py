import pygame
import random
from tiles.tile_base import Tile
from config import *

class WaterTile(Tile):
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = MIN_WATER_VALUE):
        super().__init__(rect, cell_size)
        self.font = pygame.font.Font(None, 24)  # Choose the font and size
        self.water_value = value
        
    def update(self):
        self.color = min_water_color.lerp(max_water_color, self.water_value / MAX_WATER_VALUE)
        neigbour = self.neighbours[random.choice(self.getDirections())]
        if isinstance(neigbour, WaterTile):
            if self.water_value >= neigbour.water_value:
                self.transfer_water(1, neigbour) #TODO: make this a variable
        
        self.invariant()
                    
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        if(DRAW_WATER_LEVEL):
            text = self.font.render(str(self.water_value), True, (0, 0, 0))  # Create a text surface
            screen.blit(text, (self.rect.x, self.rect.y))  # Draw the text surface on the screen at the tile's position

    def transfer_water(self, amount : int, water_tile):
        assert isinstance(water_tile, WaterTile), "water_tile must be an instance of WaterTile"
        assert amount >= 0, "Amount to transfer is negative."
        assert self.water_value >= water_tile.water_value, "Water flow is wrong."
        assert self.is_neighbour(water_tile), "Tile to transfer to is not a neighbour."
        
        if self.water_value - amount >= MIN_WATER_VALUE and self.water_value - amount <= MAX_WATER_VALUE :
            if water_tile.get_value() + amount >= MIN_WATER_VALUE and water_tile.get_value() + amount <= MAX_WATER_VALUE :
                self.add_to_value(-amount)
                water_tile.add_to_value(amount)
        
        water_tile.invariant()
        self.invariant()
    
    def is_neighbour(self, tile):        
        for direction in self.getDirections():
            neigbour = self.neighbours[direction]
            if neigbour == tile:
                return True
            
        return False
    
    def water_level_allowed(self, value = None):
        if(value == None):
            value = self.water_value
        return value >= MIN_WATER_VALUE and value <= MAX_WATER_VALUE
    
    def get_value(self):
        return self.water_value
    
    def set_value(self, value):
        assert value >= MIN_WATER_VALUE, "Value is smaller than minimum."
        assert value <= MAX_WATER_VALUE, "Value is larger than maximum."
        self.water_value = value
        
        self.invariant()
        
    def add_to_value(self, change):
        assert self.water_value + change >= MIN_WATER_VALUE, "Water level would be below minimum."
        assert self.water_value + change <= MAX_WATER_VALUE, "Water level would be above maximum."
        
        self.water_value += change
        
        self.invariant()
    
    def invariant(self):
        assert self.water_value >= MIN_WATER_VALUE, "Value is smaller than minimum. " ; self.water_value
        assert self.water_value <= MAX_WATER_VALUE, "Value is larger than maximum. " ; self.water_value