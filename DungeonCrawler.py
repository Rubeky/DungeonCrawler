#Basic setup from:
#https://realpython.com/pygame-a-primer/

#Initialising pygame library
import pygame
import pygame.freetype
import random
import csv

###############################################################################
###############################################################################

class Game:
    walking = [[None]*4 for _ in range(4)]
    tiles = [None]*4
    black_heart = None
    tool_icons = [None]*4
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
    shadow = [None]*2

###############################################################################

    def __init__(self):
        self.main()

###############################################################################

    def main(self):

        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Dungeon Crawler")
        screen.fill((255, 255, 255))

        self.loadImages()

        #Game-state variables
        running = True
        gameUpdated = False

        #Board attributes
        tile_grid = pygame.Surface((64*16, 64*16)) #[["None"]*16 for _ in range(16)]
        obstacle_grid = [["None"]*16 for _ in range(16)]
        obstacle_type = [["None"]*16 for _ in range(16)]

        #Player attributes
        player_position = [2, 2]    #Relative to bottom corner in blocks, 0-indexing
        player_health = 10          #If it gets to 0, player dies
        player_direction = 2       #Decided with keys, WASD are 0,1,2,3 respectively
        player_score = 0            #Increased by ????? ### TODO:
        currentLife = 0

        #Items list is:
        #0 - Pickaxe
        #1 - Sword
        #2 - Torch
        #3 - Staff
        unlocked_items = [True, True, False, True]
        selected_item = 0

        #Transparent surface
        alphaSurface = pygame.Surface((1920,1080))
        alphaSurface.fill((99, 84, 68))
        alphaSurface.set_alpha(100)

        #Initialising randomised dungeon
        self.generateDungeon(tile_grid, obstacle_grid, obstacle_type)
        #Fade in
        self.fadeIn(player_position, player_direction, tile_grid, obstacle_grid, screen)
        #Drawing initial frame:
        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
        pygame.display.update()

        #Gameloop
        while running:

            #Delay
            pygame.time.delay(50)
            #Checking for events
            for event in pygame.event.get():
                #Exit code if window closed
                if event.type == pygame.QUIT:
                    running = False

                #Movement from WASD, checks from last event and uses that
                #Should implement a stack so you can do multiple moves
                if event.type == pygame.KEYDOWN:

                    #Character movements
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

                    #Item selection
                    if event.key == pygame.K_1 and unlocked_items[0] == True:
                        selected_item = 0
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        self.drawUI(screen, player_health, unlocked_items, selected_item)
                    if event.key == pygame.K_2 and unlocked_items[1] == True:
                        selected_item = 1
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        self.drawUI(screen, player_health, unlocked_items, selected_item)
                    if event.key == pygame.K_3 and unlocked_items[2] == True:
                        selected_item = 2
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        self.drawUI(screen, player_health, unlocked_items, selected_item)
                    if event.key == pygame.K_4 and unlocked_items[3] == True:
                        selected_item = 3
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        self.drawUI(screen, player_health, unlocked_items, selected_item)

                    #Exiting the game
                    if event.key == pygame.K_SPACE:
                        if selected_item == 0:
                            obstacle_grid = self.breakBlock(player_position, player_direction, obstacle_grid, obstacle_type)
                            self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                            self.drawUI(screen, player_health, unlocked_items, selected_item)

                    if event.key == pygame.K_ESCAPE:
                        running = False

            #If game needs to be rerendered due to player movement, this section is used
            if gameUpdated:

                #Checking that there are no walls infront of the player
                can_move = self.playerMovementCheck(player_position, player_direction, obstacle_type)

                # Death screen
                if can_move == 3:
                    self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                    running = self.deathscreen(screen)
                    currentLife += 1

                    self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                    self.drawUI(screen, player_health, unlocked_items, selected_item)

                elif can_move == 2:
                    player_health -= 1
                    if player_health < 1:
                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        running = self.deathscreen(screen)
                        currentLife += 1

                        self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                        self.drawUI(screen, player_health, unlocked_items, selected_item)


                #Moves character
                elif can_move != 0:   #If character can actually move
                    for i in range(0, 64):

                        #pygame.time.delay(1)
                        #Background
                        screen.fill((0, 0, 0))

                        player_position = self.moveCharacter(player_position, player_direction, screen)

                        self.drawBackground(player_position, tile_grid, obstacle_grid, screen)
                        #Character
                        screen.blit(self.walking[player_direction][int(i/8)%4], [960, 480])
                        #The shade
                        screen.blit(alphaSurface,(0,0))
                        pygame.draw.rect(screen,"#000000",[1024, 1024,140,40])
                        #Shadow
                        if selected_item == 3:
                            screen.blit(self.shadow[1], [0, 0])
                            pass
                        else:
                            screen.blit(self.shadow[0], [0, 0])
                            pass
                        #UI
                        self.drawUI(screen, player_health, unlocked_items, selected_item)

                else:  #Change which way they're facing
                    self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
                    #UI
                    self.drawUI(screen, player_health, unlocked_items, selected_item)

                gameUpdated = False

        pygame.quit()

###############################################################################

    '''loads in all images required for the game'''
    def loadImages(self):
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
        self.obstacles[5] = tile_sheet.subsurface((17 * 12, 17 * 3, 16, 16))

        self.shadow[0] = pygame.image.load('Images/ShadowSmall.png')
        self.shadow[1] = pygame.image.load('Images/ShadowLarge.png')
        self.black_heart = pygame.image.load('Images/Black Heart.png')
        self.black_heart = pygame.transform.scale(self.black_heart, (64, 64))

        self.tool_icons[0] = pygame.image.load('Images/Pickaxe.png')
        self.tool_icons[1] = pygame.image.load('Images/Sword.png')
        self.tool_icons[2] = pygame.image.load('Images/Staff.png')
        self.tool_icons[3] = pygame.image.load('Images/Torch.png')

        #Scaling all the tiles and assets loaded in
        for i in range(0,4):
            self.tiles[i] = pygame.transform.scale(self.tiles[i], (64, 64))
            self.tool_icons[i] = pygame.transform.scale(self.tool_icons[i], (64, 64))
            for j in range(0,4):
                self.walking[i][j] = pygame.transform.scale(self.walking[i][j], (64, 64))

        for i in range(0, 5):
            self.obstacles[i] = pygame.transform.scale(self.obstacles[i], (64, 64))

        self.obstacles[5] = pygame.transform.scale(self.obstacles[5], (64, 64))

###############################################################################

    '''Randomly generates dungeon tiles and obstacles'''
    def generateDungeon(self, tile_grid, obstacle_grid, obstacle_type):
        '''
        generateDungeon(self, tile_grid, obstacle_grid, obstacle_type)
         - floor tile array - - - ^
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
                #tile_grid[i][j] = self.tiles[randomNumber]
                tile_grid.blit(self.tiles[randomNumber], (64*i, 64*j))

        #Generate obstacle_grid using premade tile sequences
        data = list(csv.reader(open("World chunks/Basic.csv")))

        for x in range(0, 4):
            for y in range(0, 4):
                #Note, has to be y,x due to way that csv file is read in
                temp = int(data[y][x])
                obstacle_grid[x][y] = self.obstacles[temp]
                obstacle_type[x][y] = temp

###############################################################################

    '''Draws the fade-in sequence'''
    def fadeIn(self, player_position, player_direction, tile_grid, obstacle_grid, screen):
        '''
        fadeIn(self, player_position, player_direction, tile_grid, obstacle_grid, screen)
         - player coords - ^
         - direction the player is facing - ^
         - grid of world tiles - - - - - - - - - - - - - - - ^
         - obstacle items stored for collision - - - - - - - - - - - - - ^
         - screen to draw on - - - - - - - - - - - - - - - - - - - - - - - - - - - - ^


        '''
        #This is taken from https://gamedev.stackexchange.com/questions/75572/fade-in-screen-in-pygame
        alphaSurface = pygame.Surface((1920,1080)) # The custom-surface of the size of the screen.
        alphaSurface.fill((0,0,0)) # Fill it with whole white before the main-loop.
        alphaSurface.set_alpha(255) # Set alpha to 0 before the main-loop.
        alph = 255 # The increment-variable.

        for i in range(0,128):
            pygame.time.delay(1)
            self.drawStill(player_position, player_direction, tile_grid, obstacle_grid, screen, 0)
            alph -= 2 # Increment alpha by a really small value (To make it slower, try 0.01)
            alphaSurface.set_alpha(alph) # Set the incremented alpha-value to the custom surface.
            screen.blit(alphaSurface,(0,0)) # Blit it to the screen-surface (Make them separate)
            pygame.display.update()


###############################################################################

    '''drawStill just draws a still frame of the game, no movement included'''
    def drawStill(self, player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item):
        '''
        drawStill(self, player_position, player_direction, tile_grid, obstacle_grid, screen, selected_item)
         - position of the player ^
         - which way the player is facing - - - ^
         - the floor grid to draw in - - - - - - - - - - - - - ^
         - the obstacle grid to draw in - - - - - - - - - - - - - - - - - - ^
         - the screen to draw onto - - - - - - - - - - - - - - - - - - - - - - - - - - ^
         - which item is selected - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ^
        '''
        alphaSurface = pygame.Surface((1920,1080))
        alphaSurface.fill((99, 84, 68))
        alphaSurface.set_alpha(100)

        screen.fill((0, 0, 0))
        self.drawBackground(player_position, tile_grid, obstacle_grid, screen)
        #Character
        screen.blit(self.walking[player_direction][1], [960, 480])
        #The shade
        screen.blit(alphaSurface,(0,0))
        #Shadow
        if selected_item == 3:
            screen.blit(self.shadow[1], [0, 0])
        else:
            screen.blit(self.shadow[0], [0, 0])


###############################################################################

    '''This function draws the walking animation between blocks'''
    def moveCharacter(self, player_position, player_direction, screen):
        '''
        moveCharacter(self, player_position, player_direction, screen)
         - player coordinates - ^
         - which direction is intended - - - - - ^
         - screen to draw on - - - - - - - - - - - - - - - - - - ^
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

    '''Draws the background of the game'''
    def drawBackground(self, player_position, tile_grid, obstacle_grid, screen):
        drawing_x = 960 - 64*player_position[0]
        drawing_y = 512 + 64*player_position[1] - 64*15
        screen.blit(tile_grid, (drawing_x, drawing_y))
        #Find where the tiles start relative to the screen
        for i in range(0, 16):
            for j in range(0, 16):
                drawing_x = 960 - 64*player_position[0] + 64*i
                drawing_y = 512 + 64*player_position[1] - 64*j
                if obstacle_grid[i][j] != "None":
                    screen.blit(obstacle_grid[i][j], (drawing_x, drawing_y))

###############################################################################

    '''Draws the UI of the game'''
    def drawUI(self, screen, player_health, unlocked_items, selected_item):
        '''
        drawUI(self, screen, player_health, unlocked_items, selected_item)
        - drawing item ^
        - player health - - - - - ^
        - array of unlocked items to draw - - - - ^
        - which item is currently being held - - - - - - - - - - ^
        '''
        pygame.draw.rect(screen, "#000000", (1800, 50, 50, 300), 10)
        pygame.draw.rect(screen, "#111111", (1800, 50, 50, player_health*30))
        #Draw grey heart underneath the rectangle
        screen.blit(self.black_heart, (1792, 350))

        pygame.draw.rect(screen, "#111111", (812 + 88*selected_item, 798, 68, 68), 5)
        #Draw items in "Taskbar", no taskbar image is needed
        for i in range(0,4):
            if unlocked_items[i]:
                screen.blit(self.tool_icons[i], (814 + 88*i, 800))

        pygame.display.update()

###############################################################################

    '''Simply returns the id of the block in front of the player'''
    def blockInFront(self, player_position, player_direction):
        '''
        blockInFront(self, player_position, player_direction)
         - position of the player ^
         - direction that the player is facing - ^
        '''

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

    '''Returns what should be done if the player walks forward'''
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

    '''Breaks the block infront of the player if it is cracked'''
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

    '''Shows deathscreen overlay'''
    def deathscreen(self, screen):
        dead = True
        death_font = pygame.font.Font("Fonts/Simvoni-Bold.otf", 70)
        text = death_font.render("You have died", True, "#300010")
        textRect = text.get_rect()
        textRect.center = (512, 512)

        #Deathscreen

        screen.blit(text, textRect)
        pygame.display.update()

        while dead:
            pygame.time.delay(50)

            #Draw the deathscreen with buttons and all
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    #FIND BUTTON LOCATION
                    if x < 100 and x > 0:
                       if y < 100 and y > 0:
                           dead = False
                           return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dead = False
                        return False

###############################################################################
###############################################################################

'''Spawning in the game'''
game = Game()
