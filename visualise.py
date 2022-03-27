
import pygame
from pygame.locals import *

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
player = pygame.image.load("images/chair.jpg")

while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen.blit(player, (20,30))
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 