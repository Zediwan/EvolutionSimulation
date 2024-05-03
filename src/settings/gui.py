import pygame

pygame.font.init()

draw_height_level = False
draw_animal_energy = False
draw_animal_health = False
show_dead_organisms_stats = True

menu_text: float = "Simulation Paused - Menu"
menu_font_size: float = 36
menu_font: pygame.font.Font = pygame.font.Font(None, menu_font_size)

# This defines the size of the panel in relation to the simulation height
stat_panel_height_percentage: float = 0.03
# This defines the size of the font in relation to the panel size
stat_panel_font_percentage: float = 1
stat_panel_line_width: int = 4