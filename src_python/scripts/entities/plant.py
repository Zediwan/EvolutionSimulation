import pygame
from scripts.entities.dna import DNA
from scripts.entities.organism import Organism

class Plant(Organism):
    ENERGY_GAINED_FROM_SUN = .001
    
    def __init__(self, x, y, dna: DNA):
        super().__init__(x, y, dna)
        
    def update(self):
        self.gainEnergy(Plant.ENERGY_GAINED_FROM_SUN)
        if(self.energy == self.calculate_max_energy()):
            self.spendEnergy(10)
            #self.shape.inflate_ip(.1,.1)