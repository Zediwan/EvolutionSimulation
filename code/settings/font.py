import pygame

import settings.screen

# TODO add all the fonts
# TODO is this still needed?
tile_font_size: int = int(1.1 * settings.screen.TILE_SIZE)
tile_font: pygame.font.Font = pygame.font.Font(None, tile_font_size)