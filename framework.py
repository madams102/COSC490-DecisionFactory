'''
    ALEC BOULWARE
    MATT ADAMS
    SEAN BRITTINGHAM

    COSC 490
    SPRING 2019
    DECISION FACTORY AND FRAMEWORK
'''

'''
    KNOWN ISSUES:
        -rows in the tilemap appear as columns in the real-time matrix & 
         the game-screen.
    CHANGES:
        Thurs Feb 7:
            -formatting
            -added some comments
            -GROUND to GRND, keeps tile map squre and easier to read
            -redesigned map to wall is on border, player was spawning out of bounds
            -edited movePlayer so that the axes correspond properly to position 
            -fixed indentation in main()
            -made position variable global

    FIXED:
        -player duplicating; movement improved
        -directions now corresponding, UP=UP as it should

    TODO:
        -add textfile input for map
        -eventually add a scrolling map for larger sized maps

    COMMENTS:
        -good call on __main__ Sean, I think you were trying to explain that 
         to me on Wednesday - in one ear out the other, as they say -- Matt
        
    -SB
'''

import pygame, sys, time
from pygame.locals import *
from DecisionFactory import *

#declare tile colors
PURPLE = (189, 23, 173) #portal
BLACK = (0, 0, 0)       #ground/none
GREEN = (0, 255, 0)     #player
GREY = (130, 130, 130)  #wall

#declare tile types
GRND = 0
WALL = 1
PORTAL = 2
PLAYER = 3
NONE = 'x' #refers to a spot that cannot be spawned in,
           #note that if a player walks over this spot, it will become GRND
#assign colors
colors = {
		PLAYER : GREEN,
		PORTAL : PURPLE,
        GRND : BLACK,
        WALL : GREY, 
        NONE : BLACK
	}

#hard-coded test map, note the NONE's in the middle and how they appear 
#                     in the real-time array when running
tilemap = [
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, NONE, NONE, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, GRND, GRND, GRND, GRND, GRND, GRND, GRND, GRND, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
          ]

#dimensions
TILESIZE = 40
MAPWIDTH = 10
MAPHEIGHT = 10

#define position globally
position = (0, 0)
#pygame set-up
pygame.init()
pygame.display.set_caption("Decision Factory")  #names window
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))


'''

'''
def initPlayerAndPortal():
    #initPlayer
    success = False
    global position
    while success == False:
        rx = random.randint(0, MAPWIDTH - 1)
        ry = random.randint(0, MAPHEIGHT - 1)
        if tilemap[rx][ry] != WALL and tilemap[rx][ry] != NONE:
            tilemap[rx][ry] = PLAYER
            print "player rx:", rx
            print 'player ry:', ry
            position = [rx, ry]
            success = True

    #init portal
    success = False
    while success == False:
        rx = random.randint(1, MAPWIDTH - 2)
        ry = random.randint(1, MAPHEIGHT - 2)
        if tilemap[rx][ry] != WALL and tilemap[rx][ry] != PLAYER and tilemap[rx][ry] != NONE:
            tilemap[rx][ry] = PORTAL
            success = True

'''
    print map to std. out
'''
def printTilemap():
    for y in range(0, MAPHEIGHT):
        for x in range(0, MAPWIDTH):
            print tilemap[x][y],
        print

'''

'''
def determineResult(decision):
    d_ver = 0 #d_ver? I hardly know her!
    d_hor = 0 
    if decision == 'up':
        d_ver = -1
    elif decision == 'down':
        d_ver = 1
    elif decision == 'left':
        d_hor = -1
    elif decision == 'right':
        d_hor = 1

    global position
    result = tilemap[position[0] + d_hor][position[1] + d_ver]
    print "Starting:", position
    trying = (position[0] + d_hor, position[1] + d_ver)
    print "Trying:", trying
  
    if result == WALL:
        return 'wall'
    elif result == GRND:
        return 'success'
    elif result == NONE:
        return 'success'
    elif result == PORTAL:
        return 'foundPortal'
    else:
        return 'error'

'''
.
'''
def movePlayer(position, decision):
    global tilemap

    old_x = position[0]
    old_y = position[1]

    tilemap[position[0]][position[1]] = GRND
    
    if decision == 'up':
        tilemap[position[0]][position[1] - 1] = PLAYER
        position[1] = position[1]-1
    elif decision == 'down':
        tilemap[position[0]][position[1] + 1] = PLAYER
        position[1] = position[1]+1
    elif decision == 'left':
        tilemap[position[0] - 1][position[1]] = PLAYER
        position[0] = position[0]-1
    elif decision == 'right':
        tilemap[position[0] + 1][position[1]] = PLAYER
        position[0] = position[0]+1



def main():
    initPlayerAndPortal()
    steps = 0               #steps to find goal
    df = DecisionFactory()  #initialize DecisionFactory
    # position = (0, 0)       #set player position

    while True:
    	for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
        time.sleep(0.07)
        print
        printTilemap()

        decision = df.get_decision()
        print "Decision: ", decision
        #get result of 'walk'
        result = determineResult(decision) 
        print "Result: ", result
       

        if result == 'foundPortal':
            print "Found portal in", steps, "steps!\n"
            df.put_result('success')
            pygame.quit()
            sys.exit()
        else:
            df.put_result(result)
        # print "Decision:", decision
        
        if result == 'success':
            steps += 1
            print "Steps: ", steps
            
            movePlayer(position, decision)

    
        for row in range(MAPWIDTH):
    		for column in range(MAPHEIGHT):
    			pygame.draw.rect(DISPLAYSURF, colors[tilemap[column][row]], (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
        
        # steps += 1
    	pygame.display.update()
        # print "Steps: ", steps


'''
    Flow control
'''
if __name__ == "__main__":
    main()
