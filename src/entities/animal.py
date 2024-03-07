import math
import random
from pygame import Color, Rect, Surface
from entities.organism import Organism
from config import *
from bounded_variable import BoundedVariable
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile
from tiles.tile_base import Tile

class Animal(Organism):
    ANIMAL_COLOR = pygame.Color("black")
    
    MIN_ANIMAL_HEALTH, MAX_ANIMAL_HEALTH = Organism.MIN_ORGANISM_HEALTH, Organism.MAX_ORGANISM_HEALTH
    MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY = Organism.MIN_ORGANISM_ENERGY, Organism.MAX_ORGANISM_ENERGY

    BASE_ANIMAL_HEALTH: int = MAX_ANIMAL_HEALTH - 50
    BASE_ANIMAL_ENERGY: int = MAX_ANIMAL_ENERGY - 50
    
    BASE_ANIMAL_HEALTH_BOUND: BoundedVariable = BoundedVariable(BASE_ANIMAL_HEALTH, MIN_ANIMAL_HEALTH, MAX_ANIMAL_HEALTH)
    BASE_ANIMAL_ENERGY_BOUND: BoundedVariable = BoundedVariable(BASE_ANIMAL_ENERGY, MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY)
    
    MIN_ANIMAL_WATER_AFFINITY, MAX_ANIMAL_WATER_AFFINITY = WaterTile.MIN_WATER_VALUE + 1, WaterTile.MAX_WATER_VALUE
    BASE_ANIMAL_WATER_AFFINITY: int = 5
    BASE_ANIMAL_WATER_AFFINITY_BOUND: BoundedVariable = BoundedVariable(BASE_ANIMAL_WATER_AFFINITY, MIN_ANIMAL_WATER_AFFINITY, MAX_ANIMAL_WATER_AFFINITY)
    
    MIN_ANIMAL_LAND_AFFINITY, MAX_ANIMAL_LAND_AFFINITY = GrassTile.MIN_GRASS_VALUE + 1, GrassTile.MAX_GRASS_VALUE
    BASE_ANIMAL_LAND_AFFINITY: int = 10
    BASE_ANIMAL_LAND_AFFINITY_BOUND: BoundedVariable = BoundedVariable(BASE_ANIMAL_LAND_AFFINITY, MIN_ANIMAL_LAND_AFFINITY, MAX_ANIMAL_LAND_AFFINITY)
    
    GRASS_CONSUMPTION = 1
    ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD = .9
    ANIMAL_REPRODUCTION_CHANCE = .01
    DEATH_SOIL_NUTRITION = 1
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, 
                 health: BoundedVariable = BASE_ANIMAL_HEALTH_BOUND, 
                 energy: BoundedVariable = BASE_ANIMAL_ENERGY_BOUND,
                 waterAffinity: BoundedVariable = BASE_ANIMAL_WATER_AFFINITY_BOUND, 
                 landAffinity: BoundedVariable = BASE_ANIMAL_LAND_AFFINITY_BOUND
                 ):
        
        if not shape:
            shape = tile.rect
            
        if not color:
            color = pygame.Color(random.randint(55,200), random.randint(55,200), random.randint(55,200))
            
        super().__init__(tile, shape, color, health, energy)
        self.waterAffinity: BoundedVariable = waterAffinity.copy()
        self.landAffintiy: BoundedVariable = landAffinity.copy()
        
    def update(self):
        super().update()
        #TODO: add visual that displays an animals health and energy
        
        if isinstance(self.tile, WaterTile):
            DROWNING_DAMAGE = math.floor(self.tile.water.value * 10 / self.waterAffinity.value)     # TODO: think of a good formula for this
            self.loose_health(DROWNING_DAMAGE) 
        elif isinstance(self.tile, GrassTile):
            LAND_SUFFOCATION_DAMAGE = math.floor(GrassTile.LAND_DAMAGE / self.landAffintiy.value)   # TODO: think of a good formula for this
            self.loose_health(LAND_SUFFOCATION_DAMAGE)
            
            GROWTH_NUTRITION = self.tile.growth.value   # TODO: think of a good formula for this
            self.gain_enery(GROWTH_NUTRITION)
            self.tile.growth.add_value(-self.GRASS_CONSUMPTION)
        
        direction = self.think()
        if direction:
            self.enter_tile(direction)
            
        self.reproduce()

    def reproduce(self):
        if self.ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD <= self.health.ratio():
            unoccupied_neighbor = self.tile.get_random_unoccupied_neighbor()
            if unoccupied_neighbor:
                if random.random() <= self.ANIMAL_REPRODUCTION_CHANCE:
                    self.copy(unoccupied_neighbor) # Reproduce to a neighbor tile
        
    def think(self) -> Tile|None:
        return random.choice((self.tile.get_random_unoccupied_neighbor(), None))
    
    def die(self):
        assert self.health.value <= self.MIN_ANIMAL_HEALTH, "Organism tries to die despite not being dead."
        if isinstance(self.tile, GrassTile):
            self.tile.grow(self.DEATH_SOIL_NUTRITION)
        self.tile.leave()
    
    def draw(self, screen: Surface):
        super().draw(screen)
    
    def copy(self, tile: Tile):
        newWA = self.waterAffinity.copy()
        newWA.mutate()
        newLA = self.landAffintiy.copy()
        newLA.mutate()
        return Animal(tile, color = self.color, waterAffinity=newWA, landAffinity=newLA)