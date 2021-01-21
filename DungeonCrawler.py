#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame


class Game:
    #Setting up drawing window
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    def __init__(self):

        running = True

        #Gameloop
        while running:

            #If exit button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)

            pygame.display.flip()

        pygame.quit()

game = Game()
