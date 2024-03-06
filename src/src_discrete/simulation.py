import pygame
import sys
from world import World

class Simulation:
    def __init__(self, height: int, width: int, tile_size : int):
        pygame.init()
        pygame.display.set_caption("Evolution Simulation")
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        self.world = World(height, width, tile_size)

    def run(self):
        """
        The main loop of the simulation. Updates the state of the animals and plants, handles their interactions,
        and manages the spawning of new animals and plants.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))  # Fill the screen with a white background
            
            self.world.update()
            self.world.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)