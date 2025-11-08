import pygame 
import mainmenu

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initializing pygame
pygame.init()
pygame.display.set_caption("WASSUP bro")
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# Running the game / Displaying the main menu
mainmenu.run(SCREEN, CLOCK)