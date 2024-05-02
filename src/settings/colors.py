import random

import pygame

# Simulation
SIMULATION_BACKGROUND_COLOR: pygame.Color = pygame.Color("white")
MENU_BACKGROUND_COLOR: pygame.Color = pygame.Color("grey")
STAT_BAR_BACKGROUND_COLOR: pygame.Color = pygame.Color("grey")
STAT_BAR_BORDER_COLOR: pygame.Color = pygame.Color("black")
STAT_BAR_FONT_COLOR: pygame.Color = pygame.Color("black")

# Stat Panel
STAT_PANEL_BACKGROUND_COLOR: pygame.Color = pygame.Color("black")
STAT_PANEL_FONT_COLOR: pygame.Color = pygame.Color("white")

# Tile pygame.Colors
WATER_COLOR: pygame.Color = pygame.Color(26, 136, 157)
SAND_COLOR: pygame.Color = pygame.Color(228, 232, 202)
SCORCHED_COLOR: pygame.Color = pygame.Color(153, 153, 153)
BARE_COLOR: pygame.Color = pygame.Color(187, 187, 187)
TUNDRA_COLOR: pygame.Color = pygame.Color(221, 221, 187)
SNOW_COLOR: pygame.Color = pygame.Color(248, 248, 248)
TEMPERATE_DESERT_COLOR: pygame.Color = pygame.Color(228, 232, 202)
SHRUBLAND_COLOR: pygame.Color = pygame.Color(195, 204, 187)
TAIGA_COLOR: pygame.Color = pygame.Color(203, 212, 187)
GRASSLAND_COLOR: pygame.Color = pygame.Color(196, 212, 170)
TEMPERATE_DECIDUOUS_FOREST_COLOR: pygame.Color = pygame.Color(180, 200, 169)
TEMPERATE_RAIN_FOREST_COLOR: pygame.Color = pygame.Color(163, 196, 168)
SUBTROPICAL_DESERT_COLOR: pygame.Color = pygame.Color(233, 220, 198)
TROPICAL_SEASONAL_FOREST_COLOR: pygame.Color = pygame.Color(169, 204, 163)
TROPICAL_RAIN_FOREST_COLOR: pygame.Color = pygame.Color(156, 187, 169)

# Organism pygame.Colors
BASE_ORGANISM_COLOR: pygame.Color = pygame.Color("black")


# Animals pygame.Colors
def BASE_ANIMAL_COLOR():
    return pygame.Color(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


# Plant pygame.Colors
BASE_PLANT_COLOR: pygame.Color = pygame.Color(76, 141, 29)
PLANT_TILE_COLOR_VISIBILITY: float = (
    0.2  # If the number is bigger the color of the plant gets more importance than the tile color
)