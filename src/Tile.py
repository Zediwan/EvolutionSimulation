from __future__ import annotations
from typing import List, Optional
from pygame import Rect, Surface, SRCALPHA, draw, Color
from bounded_variable import BoundedVariable
import random
from config import *

import entities.organism as organism

"""
The Tile class represents a tile in a game. It is an abstract base class (ABC) that provides common functionality for different types of tiles.

Attributes:
    rect (pygame.Rect): The rectangle representing the tile's position and size.
    cell_size (int): The size of the tile in pixels.
    neighbours (dict): A dictionary of the tile's neighboring tiles, with directions as keys and Tile objects as values.

Methods:
    update(): Abstract method that should be implemented by subclasses to update the tile's state.
    draw(screen: pygame.Surface): Draws the tile on the screen.
    add_neighbor(direction: Direction, tile: Tile): Adds a neighbor tile in the specified direction.
    get_neighbor(direction: Direction) -> Tile: Returns the neighbor tile in the specified direction.
    get_directions() -> list[Direction]: Returns a list of directions to the tile's neighbors.
    get_random_neigbor() -> Tile: Returns a random neighbor tile.
"""
class Tile():
    # Water
    MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
    BASE_WATER_LEVEL = 0
    WATER_BOUND = BoundedVariable(BASE_WATER_LEVEL, MIN_WATER_VALUE, MAX_WATER_VALUE)
    
    WATER_FLOW_AT_BORDER = 1
    DOES_WATER_FLOW = True
    WATER_FLOW_BETWEEN_TILES = 1
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    
    WATER_EVAPORATE_THRESHOLD = 2
    DROWNABLE_WATER_THRESHOLD = 3
    
    # Land
    MIN_GRASS_VALUE, MAX_GRASS_VALUE = 0, 10
    BASE_GRASS_VALUE = MIN_GRASS_VALUE
    GROWTH_BOUND = BoundedVariable(BASE_GRASS_VALUE, MIN_GRASS_VALUE, MAX_GRASS_VALUE)
    
    LAND_DAMAGE = 30
    
    DIRT_COLOR = Color(155, 118, 83, ground_alpha)
    MIN_GRASS_COLOR = Color(235, 242, 230, ground_alpha)
    MAX_GRASS_COLOR = Color(76, 141, 29, ground_alpha)
    
    BASE_GROWTH_RATE = 1
    BASE_GROWTH_CHANCE = .01
    
    WATER_GROWTH_RATE_INCREASE = 5
    WATER_GROWTH_CHANCE_INCREASE = .05
    
    COMMON_GROWTH_THRESHOLD_PERCENTAGE = .5
    POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE = .9
    GROWTH_LOSS_CHANCE = .02
    GROWTH_LOSS = 1
    
    def __init__(self, rect: Rect, tile_size: int, height: int = 0,
                 organisms: Optional[List[organism.Organism]] = None,
                 starting_water_level: Optional[int] = None,
                 water: BoundedVariable = WATER_BOUND,
                 starting_growth_level: Optional[int] = None,
                 growth: BoundedVariable = GROWTH_BOUND
                 ):
        # Organisms
        if organisms:
            self.organisms: list[organism.Organism] = organisms
        else:
            self.organisms: list[organism.Organism] = []
                    
        # Water
        self.water: BoundedVariable = water.copy()
        if starting_water_level:
            self.water.value = starting_water_level
        elif height == -1:
            self.water.value = random.randint(self.MIN_WATER_VALUE, self.MAX_WATER_VALUE)
            
        # Growth
        self.growth: BoundedVariable = growth.copy()
        if starting_growth_level:
            self.growth.value = starting_growth_level
        else:
            self.growth.value = random.randint(self.MIN_WATER_VALUE, self.MAX_WATER_VALUE)
        
        # Tile
        self.height:int = height
        self.tile_size: int = max(tile_size, MIN_TILE_SIZE)
        self.rect: Rect = rect
        self.is_border_tile: bool = False
        self.neighbors: dict[Direction, Tile] = {}
        
        # Drawing
        self.color: Color = Color(0,0,0,0)
        self.temp_surface: Surface = Surface((self.rect.width, self.rect.height), SRCALPHA)
        

    def update(self):
        if self.organisms:
            for org in self.organisms:
                org.update()
                
        # Water Update # TODO: refactor into separate method
        if self.DOES_WATER_FLOW:
            if self.is_border_tile and self.height == -1:
                self.water.add_value(self.WATER_FLOW_AT_BORDER)
            if self.water.value > 0: 
                if  self.water.value <= self.WATER_EVAPORATE_THRESHOLD:
                    self.water.add_value(-1)
                
                lowest_water_tiles = []
                lowest_water_value = self.MAX_WATER_VALUE + 1
                
                for neighbor in self.neighbors.values():
                    if neighbor.height <= self.height and neighbor.water.value <= self.water.value and 0 < neighbor.water.value <= lowest_water_value:
                        lowest_water_tiles.append(neighbor)
                        lowest_water_value = neighbor.water.value
                if lowest_water_tiles:
                    chosen_water_tile = random.choice(lowest_water_tiles)
                    if chosen_water_tile:
                        dif = self.water.value - lowest_water_value
                        if dif > 0:
                            self.transfer_water(min(self.WATER_FLOW_BETWEEN_TILES, dif), chosen_water_tile)
                    
        # Growth Update # TODO: refactor into separate method
        growth_chance = self.BASE_GROWTH_CHANCE
        growth_rate = self.BASE_GROWTH_RATE
        
        # Check if neighbour has water
        for neighbor in self.neighbors.values():
            ratio = neighbor.water.ratio()
            if ratio > 0 and self.water.value < 3:
                growth_rate += (int)(self.WATER_GROWTH_RATE_INCREASE * ratio)
                growth_chance += (int)(self.WATER_GROWTH_CHANCE_INCREASE * ratio)
        
        if random.random() < growth_chance:
            if self.growth.ratio() < self.COMMON_GROWTH_THRESHOLD_PERCENTAGE:
                self.growth.add_value(growth_rate)
            else:
                neighbor = self.get_random_neigbor()
                if neighbor:
                    tile = random.choice((self, neighbor))
                else:
                    tile = self
                tile.growth.add_value(growth_rate)
        
        if self.growth.ratio() > self.POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE:
            if random.random() < self.GROWTH_LOSS_CHANCE:
                self.growth.add_value(-self.GROWTH_LOSS)
        
    # TODO: this method does not currently work / display the borders, find a way to fix it
    def draw(self, screen: Surface):
        draw.rect(self.temp_surface, tile_border_color, self.rect, tile_outline_thickness)
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))
        
        if self.organisms:
            for org in self.organisms:
                if org.is_alive():
                    org.draw(screen)
        else:
            g_ratio = self.growth.ratio()
            growth_color = self.DIRT_COLOR.lerp(self.MIN_GRASS_COLOR, g_ratio).lerp(self.MAX_GRASS_COLOR, g_ratio)
            w_ratio = self.water.ratio()
            water_color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, w_ratio)
            
            self.color = growth_color.lerp(water_color, min(w_ratio,.75))
            self.temp_surface.fill(self.color)
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))
        
        from config import draw_water_level
        if(draw_water_level):
            text = font.render(str(self.water.value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))
            
        from config import draw_growth_level
        if(draw_growth_level):
            text = font.render(str(self.growth.value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))
        
    def transfer_water(self, amount : int, tile: Tile):
        if amount < 0:
            raise ValueError("Amount to transfer is negative.")
        if self.water.value < tile.water.value:
            raise ValueError("Water flow is wrong.")
        if not self.is_neighbor(tile):
            raise ValueError("Tile to transfer to is not a neighbour.")
    
        max_transfer = min(amount, self.water.value - self.MIN_WATER_VALUE, self.MAX_WATER_VALUE - tile.water.value)
        if max_transfer > 0:
            self.water.add_value(-max_transfer)
            tile.water.add_value(max_transfer)
        
    def leave(self, organism: organism.Organism):
        if self.organisms:
            self.organisms.remove(organism)
        
    def enter(self, organism: organism.Organism):
        if not self.organisms:
            self.organisms.append(organism)
        
        assert organism.tile == self, "Tiles Organism and Organisms tile are not equal."
        
    def is_occupied(self) -> bool:
        return bool(self.organisms)

    def add_neighbor(self, direction: Direction, tile: Tile):
        # TODO find out why this is not working properly and alway raising the error
        self.neighbors[direction] = tile

    def get_directions(self) -> List[Direction]:
        return list(self.neighbors.keys())
    
    def get_neighbors(self) -> List[Tile]:
        return list(self.neighbors.values())

    def get_neighbor(self, direction: Direction) -> Tile|None:
        return self.neighbors.get(direction, None)

    def get_random_neigbor(self) -> Tile:
        return self.neighbors[random.choice(self.get_directions())]
    
    def get_random_unoccupied_neighbor(self) -> Tile|None:
        unoccupied_neighbors = [tile for tile in self.neighbors.values() if not tile.is_occupied()]

        if not unoccupied_neighbors:
            return None
        return random.choice(unoccupied_neighbors)
    
    def is_neighbor(self, tile: Tile) -> bool:  
        if not self.neighbors.values():
            return False
        return tile in self.neighbors.values()
    