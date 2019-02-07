import pygame, sys, time
from pygame.locals import *
from DecisionFactory import *
PURPLE = (189, 23, 173)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (130, 130, 130)

GROUND = 0
WALL = 1
PORTAL = 2
PLAYER = 3

colors = {
		PLAYER : GREEN,
		PORTAL : PURPLE,
                GROUND : BLACK,
                WALL : GREY
	}

tilemap = [
            [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
            [GROUND, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, GROUND, GROUND, GROUND, GROUND, GROUND,GROUND, WALL, GROUND],
            [GROUND, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, GROUND],
            [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
	]

TILESIZE = 40
MAPWIDTH = 10
MAPHEIGHT = 10

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

df = DecisionFactory()
#player position
position = (0, 0)

def determineResult(decision):
    dx = 0
    dy = 0
    if decision == 'up':
        dy = -1
    elif decision == 'down':
        dy = 1
    elif decision == 'left':
        dx = -1
    elif decision == 'right':
        dx = 1

    result = tilemap[position[0] + dx][position[1] + dy]
    print "Original: (" + str(position[0]) + ", " + str(position[1]) + ")"
    print "New:      (" + str(position[0] + dx) + ", " + str(position[1] + dy) + ")"
    if result == WALL:
        return 'wall'
    elif result == GROUND:
        return 'success'
    elif result == PORTAL:
        return 'foundPortal'
    else:
        return 'error'

def initPlayerAndPortal():
    #initPlayer
    success = False
    global position
    while success == False:
        rx = random.randint(1, MAPWIDTH - 1)
        ry = random.randint(1, MAPHEIGHT - 1)
        if tilemap[rx][ry] != WALL:
            tilemap[rx][ry] = PLAYER
            print rx
            print ry
            position = (rx, ry)
            success = True

    success = False
    while success == False:
        rx = random.randint(1, MAPWIDTH - 2)
        ry = random.randint(1, MAPHEIGHT - 2)
        if tilemap[rx][ry] != WALL and tilemap[rx][ry] != PLAYER:
            tilemap[rx][ry] = PORTAL
            success = True

def movePlayer(position, decision):
    global tilemap
    tilemap[position[0]][position[1]] = GROUND
    if decision == 'up':
        tilemap[position[0]][position[1] - 1] = PLAYER
    elif decision == 'down':
        tilemap[position[0]][position[1] + 1] = PLAYER
    elif decision == 'left':
        tilemap[position[0] - 1][position[1]] = PLAYER
    elif decision == 'right':
        tilemap[position[0] + 1][position[1]] = PLAYER

def printTilemap():
    for x in range(0, MAPHEIGHT):
        for y in range(0, MAPWIDTH):
            print tilemap[x][y],
        print

initPlayerAndPortal()
steps = 0

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
                
        time.sleep(0.7)
        printTilemap()
        decision = df.get_decision()
        #get result of 'walk'
        result = determineResult(decision) 
        print result
        if result == 'foundPortal':
            print "Found portal in " + str(steps) + " steps!\n"
            df.put_result('success')
            pygame.quit()
            sys.exit()
        else:
            df.put_result(result)
        print decision
        if result == 'success':
            movePlayer(position, decision)
	for row in range(MAPHEIGHT):
		for column in range(MAPWIDTH):
			pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]], (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
        steps += 1
	pygame.display.update()

