#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame
import random

###############################################################################
###############################################################################

class Game:
    walking = [[None]*4 for _ in range(4)]
    tiles = [None]*4

###############################################################################

    def __init__(self):

        self.main()

###############################################################################

    def main(self):

        pygame.init()
        screen = pygame.display.set_mode([1024, 1024])
        pygame.display.set_caption("Dungeon Crawler")
        screen.fill((255, 255, 255))

        walking = [None]*4
        walking[0] = pygame.image.load('Images/Up.png')
        walking[1] = pygame.image.load('Images/Left.png')
        walking[2] = pygame.image.load('Images/Down.png')

        for i in range(4):
            self.walking[0][i] = walking[0].subsurface((0 + i*16, 0, 16, 16))
            self.walking[1][i] = walking[1].subsurface((0 + i*16, 0, 16, 16))
            self.walking[2][i] = walking[2].subsurface((0 + i*16, 0, 16, 16))
            self.walking[3][i] = pygame.transform.flip(self.walking[1][i], True, False)

        '''self.walking = [\
        [pygame.image.load('Images/Up1.png'), pygame.image.load('Images/Up2.png'), pygame.image.load('Images/Up3.png'), pygame.image.load('Images/Up4.png')],\
        [pygame.image.load('Images/Left1.png'), pygame.image.load('Images/Left2.png'), pygame.image.load('Images/Left3.png'), pygame.image.load('Images/Left4.png')],\
        [pygame.image.load('Images/Down1.png'), pygame.image.load('Images/Down2.png'), pygame.image.load('Images/Down3.png'), pygame.image.load('Images/Down4.png')],\
        [pygame.image.load('Images/Right1.png'), pygame.image.load('Images/Right2.png'), pygame.image.load('Images/Right3.png'), pygame.image.load('Images/Right4.png')]\
        ]'''

        tile_sheet = pygame.image.load('Images/Tiles.png')
        #TODO: Choose better tiles
        self.tiles[0] = tile_sheet.subsurface((17 * 17, 17 * 10, 16, 16))
        self.tiles[1] = tile_sheet.subsurface((17 * 18, 17 * 10, 16, 16))
        self.tiles[2] = tile_sheet.subsurface((17 * 10, 17 * 11, 16, 16))
        self.tiles[3] = tile_sheet.subsurface((17 * 10, 17 * 12, 16, 16))


        #Scaling all the tiles and assets loaded in
        for i in range(0,4):
            self.tiles[i] = pygame.transform.scale(self.tiles[i], (64, 64))
            for j in range(0,4):
                self.walking[i][j] = pygame.transform.scale(self.walking[i][j], (64, 64))

        running = True
        gameUpdated = False
        tile_grid =  [["None"]*16 for _ in range(16)]
        obstacle_grid = [["None"]*16 for _ in range(16)]

        #Player attributes
        player_position = [160, 160] #Relative to top corner of board, in "pixels"
        player_health = 10
        player_direction = -1
        player_score = 0
        items_list = ""

        self.generateDungeon(tile_grid, obstacle_grid)
        self.showScreen(player_position, player_direction, tile_grid, obstacle_grid, screen, player_health, items_list)

        screen.blit(self.walking[2][0], [480, 480])

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
                player_position, player_health = self.showScreen(player_position, player_direction, tile_grid, obstacle_grid, screen, player_health, items_list)
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
        for i in range(0, 16):
            for j in range(0, 16):
                randomNumber = random.randint(0,3)
                tile_grid[i][j] = self.tiles[randomNumber]

        #Generate obstacle_grid using premade tile sequences
        for x in range(0, 4):
            for y in range(0, 4):
                for i in range(0, 4):
                    for j in range(0, 4):
                        pass

###############################################################################

    '''
    drawMovement(self, player_position, player_direction)
     - player coordinates - ^
     - which direction is intended - - - - - ^

     - This function draws the walking animation between blocks
    '''
    def showScreen(self, player_position, player_direction, tile_grid, obstacle_grid, screen, player_health, items_list):

        response = self.playerMovementCheck(player_position, player_direction, obstacle_grid)
        if response == 3:
            self.deathMessage()
        elif response == 2:
            player_health -= 1

        for i in range(0, 8):
            pygame.time.delay(120)
            #Background
            screen.fill((255, 255, 255))

            if player_direction == 0:
                player_position[1] += 8
            if player_direction == 1:
                player_position[0] -= 8
            if player_direction == 2:
                player_position[1] -= 8
            if player_direction == 3:
                player_position[0] += 8

            self.drawBackground(player_position, tile_grid, obstacle_grid, screen)
            #Character
            screen.blit(self.walking[player_direction][i%4], [480, 480])
            #UI
            self.drawUI(player_health, items_list)
            #Updates it all
            pygame.display.update()



        return player_position, player_health

###############################################################################

    def drawBackground(self, player_position, tile_grid, obstacle_grid, screen):
        #Find where the tiles start relative to the screen
        tile_pos = [480 - 32 - player_position[0], 480 - player_position[1]]
        for i in range(0, 16):
            for j in range(0, 16):
                screen.blit(tile_grid[i][j], ((tile_pos[0] + 64*i), ( - tile_pos[1] + 64*j)))
                if tile_grid[i][j] == "None":
                    pass
                elif tile_grid[i][j] == "Tile1":
                    pass
                elif tile_grid[i][j] == "Tile2":
                    pass
                elif tile_grid[i][j] == "Tile3":
                    pass
                elif tile_grid[i][j] == "Tile4":
                    pass
                elif tile_grid[i][j] == "RareTile":
                    pass
                elif tile_grid[i][j] == "VeryRareTile":
                    pass


                #Draw walls/objects
                pass
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
        #Check for "wall", "pit", "cracked wall", "box", ""
        pass

###############################################################################

    def breakBlock(self, player_position, player_direction, obstacle_grid):
        #Check for "cracked_wall" in front of player, break it
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
