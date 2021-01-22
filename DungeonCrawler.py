#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame
import time

###############################################################################
###############################################################################

class Game:
    #Setting up drawing window
    pygame.init()
    screen = pygame.display.set_mode([900, 900])
    pygame.display.set_caption("Dungeon Crawler")

###############################################################################

    def __init__(self):

        self.main()
        pass

###############################################################################

    def main(self):

        running = True
        tile_grid =  [["Empty"]*10 for _ in range(10)]
        obstacle_grid = [["None"]*10 for _ in range(10)]

        self.generateDungeon(tile_grid, obstacle_grid)

        #Player attributes
        player_x = 5
        player_y = 5
        player_health = 10
        player_direction = ""
        player_score = 0
        items_list = ""


        #Gameloop
        while running:

            time.sleep(0.1)
            #Checking for events
            for event in pygame.event.get():
                #Exit code if window closed
                if event.type == pygame.QUIT:
                    running = False

                #Movement from WASD, checks from last event and uses that
                #Should implement a stack so you can do multiple moves
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player_direction = "a"
                    if event.key == pygame.K_d:
                        player_direction = "d"
                    if event.key == pygame.K_w:
                        player_direction = "w"
                    if event.key == pygame.K_s:
                        player_direction = "s"

                    if event.key == pygame.K_SPACE:
                        obstacle_grid = self.breakBlock(player_x, player_y, player_direction, obstacle_grid)

            ##Printing layers##
            #Background - Not sure if needed, maybe black?
            self.screen.fill((0, 0, 0))

            #Tiles and walls, setting up collisions?
            for i in range(0, 9):
                for j in range(0, 9):
                    #Draw each tile
                    #Draw each wall
                    pass

            #Player - Movement of player
            player_x, player_y, player_health = self.playerMove(player_x, player_y, player_direction, player_health, obstacle_grid)
            player_direction = ""

            #Filter? For lighting
            #Image of a circle with feathered edges for lighting

            #UI
            self.drawUI(player_health, items_list)

        pygame.quit()


###############################################################################

    def generateDungeon(self, tile_grid, obstacle_grid):
        #Randomise tile_grid to be a nice background
        #Generate obstacle_grid using a turtle? maybe using a maze generator
        pass

###############################################################################

    def playerMove(self, player_x, player_y, player_direction, player_health, obstacle_grid):

        if player_direction == "a":
            response = self.playerMovementCheck(player_x, player_y, "a", obstacle_grid)
            if response == 1:
                player_x -= 1
            elif response == 2:
                player_x -= 1
                player_health -= 1
            elif response == 3:
                self.deathMessage()

        elif player_direction == "d":
            response = self.playerMovementCheck(player_x, player_y, "d", obstacle_grid)
            if response == 1:
                player_x -= 1
            elif response == 2:
                player_x -= 1
                player_health -= 1
            elif response == 3:
                self.deathMessage()

        elif player_direction == "w":
            response = self.playerMovementCheck(player_x, player_y, "w", obstacle_grid)
            if response == 1:
                player_x -= 1
            elif response == 2:
                player_x -= 1
                player_health -= 1
            elif response == 3:
                self.deathMessage()

        elif player_direction == "s":
            response = self.playerMovementCheck(player_x, player_y, "s", obstacle_grid)
            if response == 1:
                player_x -= 1
            elif response == 2:
                player_x -= 1
                player_health -= 1
            elif response == 3:
                self.deathMessage()


        return player_x, player_y, player_health
        pass

###############################################################################

    def drawUI(self, player_health, items_list):
        #Draw healthbar
        #Draw Taskbar image
        #Draw items in "Taskbar"
        pass

###############################################################################

    '''
    playerMovementCheck(self, player_x, player_y, player_direction, obstacle_grid)
     - player x-coordinate - - - ^
     - player y-coordinate - - - - - - - - ^
     - which direction is intended - - - - - - - - - - - ^
     - the obstacle grid passed in from main - - - - - - - - - - - - - - ^

     - This function takes inputs and checks if a player movement is valid
     - Possible returns:
     0: No, wall is blocking your way
     1: Movement is fine
     2: Movement is fine but 1 damage should be taken
     3: Instant death (such as a spike pit)
    '''
    def playerMovementCheck(self, player_x, player_y, player_direction, obstacle_grid):
        #Check for "wall", "pit", "cracked wall",
        pass

###############################################################################

    def breakBlock(self, player_x, player_y, player_direction, obstacle_grid):
        #Check for "cracked_wall", break it
        return obstacle_grid

###############################################################################

    def deathMessage(self, death_type, player_score):
        #Draw respawn/quit screen
        #Buttons to respawn or quit
        #Text for "YOU DIED" and "score = x"
        pass

###############################################################################
###############################################################################

game = Game()
