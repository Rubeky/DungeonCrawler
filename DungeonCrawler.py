#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame
import os

print(os.getcwd())

###############################################################################
###############################################################################

class Game:
    walking = [[]]

###############################################################################

    def __init__(self):

        self.main()

###############################################################################

    def main(self):

        pygame.init()
        screen = pygame.display.set_mode([1024, 1024])
        pygame.display.set_caption("Dungeon Crawler")
        screen.fill((255, 255, 255))


        self.walking = [\
        [pygame.image.load('Images/Up1.png'), pygame.image.load('Images/Up2.png'), pygame.image.load('Images/Up3.png'), pygame.image.load('Images/Up4.png')],\
        [pygame.image.load('Images/Left1.png'), pygame.image.load('Images/Left2.png'), pygame.image.load('Images/Left3.png'), pygame.image.load('Images/Left4.png')],\
        [pygame.image.load('Images/Down1.png'), pygame.image.load('Images/Down2.png'), pygame.image.load('Images/Down3.png'), pygame.image.load('Images/Down4.png')],\
        [pygame.image.load('Images/Right1.png'), pygame.image.load('Images/Right2.png'), pygame.image.load('Images/Right3.png'), pygame.image.load('Images/Right4.png')]\
        ]

        for i in range(0,4):
            for j in range(0,4):
                self.walking[i][j] = pygame.transform.scale(self.walking[i][j], (64, 64))

        running = True
        gameUpdated = False
        tile_grid =  [["Empty"]*10 for _ in range(10)]
        obstacle_grid = [["None"]*10 for _ in range(10)]

        self.generateDungeon(tile_grid, obstacle_grid)

        #Player attributes
        player_position = [160, 160] #Relative to top corner of board, in "pixels"
        player_health = 10
        player_direction = ""
        player_score = 0
        items_list = ""


        pygame.display.update()

        #Gameloop
        while running:

            pygame.time.delay(50)
            #Checking for events
            for event in pygame.event.get():
                #Exit code if window closed
                if event.type == pygame.QUIT:
                    running = False

                #Movement from WASD, checks from last event and uses that
                #Should implement a stack so you can do multiple moves
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player_direction = 0
                        gameUpdated = True
                    if event.key == pygame.K_a:
                        player_direction = 1
                        gameUpdated = True
                    if event.key == pygame.K_s:
                        player_direction = 2
                        gameUpdated = True
                    if event.key == pygame.K_d:
                        player_direction = 3
                        gameUpdated = True

                    if event.key == pygame.K_SPACE:
                        obstacle_grid = self.breakBlock(player_position, player_direction, obstacle_grid)
                        gameUpdated = True

                    if event.key == pygame.K_ESCAPE:
                        running = False

            if gameUpdated:
                #Populates screen
                player_position, player_health = self.drawMovement(player_position, player_direction, tile_grid, obstacle_grid, screen, player_health, items_list)
                player_direction = ""


                gameUpdated = False

            pygame.display.update()

        pygame.quit()


###############################################################################
    '''
    generateDungeon(self, tile_grid, obstacle_grid)
     - floor tile array - - ^
     - obstacles in dungeon - - - - - - - ^

      - This function takes in the grids for floor tiles and obstacles
      - (initialised as empty) and fills them randomly with reasonable
      - obstacles for the player to overcome (ideally)
      - Passed out of this function by reference are:
      - tile_grid
      - obstacle_grid
    '''
    def generateDungeon(self, tile_grid, obstacle_grid):
        #Randomise tile_grid to be a nice background
        #Generate obstacle_grid using premade tile sequences
        pass

###############################################################################

    '''
    drawMovement(self, player_position, player_direction)
     - player coordinates - ^
     - which direction is intended - - - - - ^

     - This function draws the walking animation between blocks
    '''
    def drawMovement(self, player_position, player_direction, tile_grid, obstacle_grid, screen, player_health, items_list):

        response = self.playerMovementCheck(player_position, player_direction, obstacle_grid)
        if response == 3:
            self.deathMessage()
        elif response == 2:
            player_health -= 1

        for i in range(0, 16):
            pygame.time.delay(100)
            #Background
            screen.fill((255, 255, 255))
            self.drawToScreen(player_position, tile_grid, obstacle_grid)
            #Character
            screen.blit(self.walking[player_direction][i%4], [480, 480])
            #UI
            self.drawUI(player_health, items_list)
            #Updates it all
            pygame.display.update()


        return player_position, player_health

###############################################################################

    def drawToScreen(self, player_position, tile_grid, obstacle_grid):
        #Find where the tiles start relative to the screen
        tile_pos = [480 - player_position[0], 480 - player_position[1]]
        for i in range(0, 16):
            for j in range(0,16):
                #Draw tiles at position (tile_pos + 64*distance)
                #Draw walls/objects

        pass

###############################################################################

    def drawUI(self, player_health, items_list):
        #Draw healthbar
        #Draw Taskbar image
        #Draw items in "Taskbar"
        pass

###############################################################################

    '''
    playerMovementCheck(self, player_position, player_direction, obstacle_grid)
     - player coordinates - - - - - ^
     - which direction is intended - - - - - - - - ^
     - the obstacle grid passed in from main - - - - - - - - - - - - ^

     - This function takes inputs and checks if a player movement is valid
     - Possible returns:
     0: No, wall is blocking your way
     1: Movement is fine
     2: Movement is fine but 1 damage should be taken
     3: Instant death (such as a spike pit)
     4: Box to push ## TODO:
    '''
    def playerMovementCheck(self, player_position, player_direction, obstacle_grid):
        #Check for "wall", "pit", "cracked wall",
        pass

###############################################################################

    def breakBlock(self, player_position, player_direction, obstacle_grid):
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
