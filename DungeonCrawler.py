#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame
import random
import csv

###############################################################################
###############################################################################

class Game:
    walking = [[None]*4 for _ in range(4)]
    tiles = [None]*4
    '''
    0 - Nothing
    1 - Wall1
    2 - Wall2
    3 - Wall3
    4 - Cracked wall
    5 - Spike pit
    6 - Vines
    7 - Tentacle
    8 - Box
    9 - Spikes
    '''
    obstacles = [0]*10
    obstacle_types = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    shadow = None

###############################################################################

    def __init__(self):
        self.main()

###############################################################################

    def main(self):

        pygame.init()
        screen = pygame.display.set_mode([1024, 1024])
        pygame.display.set_caption("Dungeon Crawler")
        screen.fill((255, 255, 255))

        self.setupVariables()

        #Game-state variables
        running = True
        gameUpdated = False

        #Board attributes
        tile_grid = [["None"]*16 for _ in range(16)]
        obstacle_grid = [["None"]*16 for _ in range(16)]
        obstacle_type = [["None"]*16 for _ in range(16)]

        #Player attributes
        player_position = [2, 2] #Relative to bottom corner in blocks, 0-indexing
        player_health = 10
        player_direction = -1
        player_score = 0
        items_list = ["", "", "", ""]

        self.generateDungeon(tile_grid, obstacle_grid, obstacle_type)
        #Drawing initial frame:
        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen)

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
                        obstacle_grid = self.breakBlock(player_position, player_direction, obstacle_grid, obstacle_type)
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen)

                    if event.key == pygame.K_ESCAPE:
                        running = False

            if gameUpdated:

                can_move = self.playerMovementCheck(player_position, player_direction, obstacle_type)
                if can_move == 3:
                    self.deathMessage()
                elif can_move == 2:
                    player_health -= 1

                #Moves character
                if can_move != 0:   #If character can actually move
                    for i in range(0, 64):

                        pygame.time.delay(3)
                        #Background
                        screen.fill((0, 0, 0))

                        player_position = self.moveCharacter(player_position, player_direction, screen)

                        self.drawBackground(player_position, tile_grid, obstacle_grid, screen)
                        #Character
                        screen.blit(self.walking[player_direction][int(i/8)%4], [480, 480])
                        #Shadow
                        screen.blit(self.shadow, [0, 0])
                        #UI
                        self.drawUI(player_health, items_list)
                        #Updates it all
                        pygame.display.update()
                else:
                    self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen)


                gameUpdated = False

        pygame.quit()

###############################################################################

    def setupVariables(self):
        walking = [None]*4
        walking[0] = pygame.image.load('Images/Up.png')
        walking[1] = pygame.image.load('Images/Left.png')
        walking[2] = pygame.image.load('Images/Down.png')

        for i in range(4):
            self.walking[0][i] = walking[0].subsurface((0 + i*16, 0, 16, 16))
            self.walking[1][i] = walking[1].subsurface((0 + i*16, 0, 16, 16))
            self.walking[2][i] = walking[2].subsurface((0 + i*16, 0, 16, 16))
            self.walking[3][i] = pygame.transform.flip(self.walking[1][i], True, False)


        tile_sheet = pygame.image.load('Images/Tiles.png')
        #TODO: Choose better tiles
        self.tiles[0] = tile_sheet.subsurface((17 * 17, 17 * 12, 16, 16))
        self.tiles[1] = tile_sheet.subsurface((17 * 18, 17 * 12, 16, 16))
        self.tiles[2] = tile_sheet.subsurface((17 * 17, 17 * 13, 16, 16))
        self.tiles[3] = tile_sheet.subsurface((17 * 18, 17 * 13, 16, 16))

        self.obstacles[0] = tile_sheet.subsurface((17 * 0, 17 * 0, 1, 1))
        self.obstacles[1] = tile_sheet.subsurface((17 * 1, 17 * 5, 16, 16))
        self.obstacles[2] = tile_sheet.subsurface((17 * 2, 17 * 5, 16, 16))
        self.obstacles[3] = tile_sheet.subsurface((17 * 3, 17 * 5, 16, 16))
        self.obstacles[4] = tile_sheet.subsurface((17 * 9, 17 * 3, 16, 16))

        self.shadow = pygame.image.load('Images/Shadow.png')

        #Scaling all the tiles and assets loaded in
        for i in range(0,4):
            self.tiles[i] = pygame.transform.scale(self.tiles[i], (64, 64))
            for j in range(0,4):
                self.walking[i][j] = pygame.transform.scale(self.walking[i][j], (64, 64))

        for i in range(0, 5):
            self.obstacles[i] = pygame.transform.scale(self.obstacles[i], (64, 64))

###############################################################################

    def generateDungeon(self, tile_grid, obstacle_grid, obstacle_type):
        '''
        generateDungeon(self, tile_grid, obstacle_grid, obstacle_type)
         - floor tile array - - ^
         - obstacles in dungeon - - - - - - - ^
         - obstacle types stored for collision - - - - - - - ^

          - This function takes in the grids for floor tiles and obstacles
          - (initialised as empty) and fills them randomly with reasonable
          - obstacles for the player to overcome (ideally)
          - Passed out of this function by reference are:
          - tile_grid
          - obstacle_grid
        '''

        #Randomise tile_grid to be a nice background
        for i in range(0, 16):
            for j in range(0, 16):
                randomNumber = random.randint(0,3)
                tile_grid[i][j] = self.tiles[randomNumber]

        #Generate obstacle_grid using premade tile sequences
        data = list(csv.reader(open("World chunks/Basic.csv")))

        for x in range(0, 4):
            for y in range(0, 4):
                #Note, has to be y,x due to way that csv file is read in
                temp = int(data[y][x])
                obstacle_grid[x][y] = self.obstacles[temp]
                obstacle_type[x][y] = temp

###############################################################################

    def drawStill(self, player_position, player_direction, tile_grid, obstacle_grid, screen):
        '''
        drawStill just draws a still frame of the game, no movement included
        '''

        screen.fill((0, 0, 0))
        self.drawBackground(player_position, tile_grid, obstacle_grid, screen)
        #Character
        screen.blit(self.walking[player_direction][1], [480, 480])
        #Shadow
        screen.blit(self.shadow, [0, 0])
        #Updates it all
        pygame.display.update()

###############################################################################

    def moveCharacter(self, player_position, player_direction, screen):
        '''
        drawMovement(self, player_position, player_direction)
         - player coordinates - ^
         - which direction is intended - - - - - ^

         - This function draws the walking animation between blocks
        '''

        if player_direction == 0:
            player_position[1] += 1/64
        if player_direction == 1:
            player_position[0] -= 1/64
        if player_direction == 2:
            player_position[1] -= 1/64
        if player_direction == 3:
            player_position[0] += 1/64

        return player_position

###############################################################################

    def drawBackground(self, player_position, tile_grid, obstacle_grid, screen):
        #Find where the tiles start relative to the screen
        for i in range(0, 16):
            for j in range(0, 16):
                drawing_x = 480 - 64*player_position[0] + 64*i
                drawing_y = 512 + 64*player_position[1] - 64*j
                if tile_grid[i][j] != None:
                    screen.blit(tile_grid[i][j], (drawing_x, drawing_y))
                if obstacle_grid[i][j] != "None":
                    screen.blit(obstacle_grid[i][j], (drawing_x, drawing_y))
                pass
        pass

###############################################################################

    def drawUI(self, player_health, items_list):
        #Draw healthbar, check if empty, if yes, self.deathMessage()
        #Draw Taskbar image
        #Draw items in "Taskbar"
        pass

###############################################################################

    def blockInFront(self, player_position, player_direction):

        if player_direction == 0:
            playerlooking_x = player_position[0]
            playerlooking_y = player_position[1] + 1
        elif player_direction == 1:
            playerlooking_x = player_position[0] - 1
            playerlooking_y = player_position[1]
        elif player_direction == 2:
            playerlooking_x = player_position[0]
            playerlooking_y = player_position[1] - 1
        elif player_direction == 3:
            playerlooking_x = player_position[0] + 1
            playerlooking_y = player_position[1]
        else:
            return -1, -1

        return int(playerlooking_x), int(playerlooking_y)

###############################################################################

    def playerMovementCheck(self, player_position, player_direction, obstacle_type):
        '''
        playerMovementCheck(self, player_position, player_direction, obstacle_type)
         - player coordinates - - - - - ^
         - which direction is intended - - - - - - - - ^
         - what all obstacle grid objects actually are - - - - - - - - - - ^

         - This function takes inputs and checks if a player movement is valid
         - Possible returns:
         0: No, wall is blocking your way
         1: Movement is fine
         2: Movement is fine but 1 damage should be taken (such as spikes)
         3: Instant death (such as a spike pit)
         4: Box to push ## TODO:
         5: Wall which is breakable
        '''


        playerlooking_x, playerlooking_y = self.blockInFront(player_position, player_direction)

        if obstacle_type[playerlooking_x][playerlooking_y] == 0:
            return 1
        elif obstacle_type[playerlooking_x][playerlooking_y] == 1:
            return 0
        elif obstacle_type[playerlooking_x][playerlooking_y] == 2:
            return 0
        elif obstacle_type[playerlooking_x][playerlooking_y] == 3:
            return 0
        elif obstacle_type[playerlooking_x][playerlooking_y] == 4:
            return 0
        elif obstacle_type[playerlooking_x][playerlooking_y] == 5:
            return 3
        elif obstacle_type[playerlooking_x][playerlooking_y] == 6:
            return 0
        elif obstacle_type[playerlooking_x][playerlooking_y] == 7:
            return 1
        elif obstacle_type[playerlooking_x][playerlooking_y] == 8:
            return 4
        elif obstacle_type[playerlooking_x][playerlooking_y] == 9:
            return 2


###############################################################################

    def breakBlock(self, player_position, player_direction, obstacle_grid, obstacle_type):
        '''
        breakBlock(self, player_position, player_direction, obstacle_grid, obstacle_type)
         - player coordinates - ^
         - which direction is intended - - - - - ^
         - the obstacle grid passed in from main - - - - - - - - ^
         - what all obstacle grid objects actually are - - - - - - - - - - - - ^
        '''
        playerlooking_x, playerlooking_y = self.blockInFront(player_position, player_direction)

        if obstacle_type[playerlooking_x][playerlooking_y] == 4:
            obstacle_grid[playerlooking_x][playerlooking_y] = self.obstacles[0]
            obstacle_type[playerlooking_x][playerlooking_y] = 0

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
