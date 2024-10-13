import pygame 
from game import Game


pygame.init()

size = (1200, 800)
screen = pygame.display.set_mode(size)

menu_height = 100
game_area_height = 600 - menu_height
game_area_rect = pygame.Rect(0, menu_height, 800, game_area_height)

pygame.display.set_caption("Reaction Game")


game = Game()

run = True

while run: 

    game.run()