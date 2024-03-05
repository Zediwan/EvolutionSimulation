import random
import pygame
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile
from config import *

class Grid():
    def __init__(self, rows : int, cols : int, tile_size : int):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.tiles = [[self.create_tile(col, row) for col in range(self.cols)] for row in range(self.rows)]
        self.add_cell_neighbours()
    
    def update(self):
        # Create a list of all tiles
        tiles_list = [tile for row in self.tiles for tile in row]
        
        # Shuffle the list
        random.shuffle(tiles_list)
        
        # Update each tile
        for tile in tiles_list:
            tile.update()
            
    def draw(self, screen : pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw(screen)
                
    def create_tile(self, col, row):
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        
        if SURROUNDED_BY_WATER and (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1):
            tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        elif random.random() >= LAND_PERCENTAGE:
            tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        else:
            tile = GrassTile(rect, self.tile_size, random.randint(0,10))
        return tile
    
    def add_cell_neighbours(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row][col]
                if row > 0:
                    tile.addNeighbour(NORTH, self.tiles[row - 1][col])
                if col < self.cols - 1:
                    tile.addNeighbour(EAST, self.tiles[row][col + 1])
                if row < self.rows - 1:
                    tile.addNeighbour(SOUTH, self.tiles[row + 1][col])
                if col > 0:
                    tile.addNeighbour(WEST, self.tiles[row][col - 1])