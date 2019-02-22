'''
	ALEC BOULWARE
	MATT ADAMS
	SEAN BRITTINGHAM

	COSC 490
	SPRING 2019
	DECISION FACTORY AND FRAMEWORK
'''

'''
	TODO: none!
'''

import pygame, sys, time
from pygame.locals import *
from DecisionFactory import *
from inputMap import readMap

#declare tile colors
PURPLE = (189, 23, 173) #portal
BLACK = (0, 0, 0)       #ground/none
GREEN = (0, 255, 0)     #player
GREY = (130, 130, 130)  #wall

#declare tile types
F = 0
W = 1
G = 2
P = 3
N = 'x' #refers to a spot that cannot be spawned in,
	#note that if a player walks over this spot, it will become F

#assign colors
colors = {
		P : GREEN,
		G : PURPLE,
		F : BLACK,
		W : GREY, 
		N : BLACK
	}
#map for Walter to wander in
tilemap = []

#dimensions
TILESIZE = 40
MAPWIDTH = 10		#default- used if no map file is passed at execution
MAPHEIGHT = 10		#default- used if no map file is passed at execution

#define position globally
position = (0, 0)



'''

'''
def initPlayerAndPortal():
	#check for initOverride
	initOverride = False
	if len(sys.argv) >= 3:
		for i in range(len(sys.argv)):
			if sys.argv[i] == "-initOverride" or sys.argv[i] == "-r":
				initOverride = True

#check if player or portal already exists in textmap
	playerExists = False
	portalExists = False
	global position
	for y in range(0, MAPHEIGHT):
		for x in range(0, MAPWIDTH):
			if tilemap[x][y] == 3:
				if initOverride == False:
					playerExists = True
					position = [x, y]
				else:
					tilemap[x][y] = 0
			if tilemap[x][y] == 2:
				if initOverride == False:
					portalExists = True
				else:
					tilemap[x][y] = 0	

	if playerExists == False:
		#initPlayer
		success = False
		while success == False:
			rx = random.randint(0, MAPWIDTH - 1)
			ry = random.randint(0, MAPHEIGHT - 1)

			if tilemap[rx][ry] != W and tilemap[rx][ry] != N:
				tilemap[rx][ry] = P
				position = [rx, ry]
				success = True

	if portalExists == False:
		#init portal
		success = False
		while success == False:
			rx = random.randint(1, MAPWIDTH - 2)
			ry = random.randint(1, MAPHEIGHT - 2)
			if tilemap[rx][ry] != W and tilemap[rx][ry] != P and tilemap[rx][ry] != N:
				tilemap[rx][ry] = G
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
	d_ver = 0 #d_ver? I hardly know her! LOL my bad i meant to change it back, x/y were confusing me atm. - In a world where x=y, who can blame thee?
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
  
	if result == W:
		return 'wall'
	elif result == F:
		return 'success'
	elif result == N:
		return 'success'
	elif result == G:
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

	tilemap[position[0]][position[1]] = F
	
	if decision == 'up':
		tilemap[position[0]][position[1] - 1] = P
		position[1] = position[1]-1
	elif decision == 'down':
		tilemap[position[0]][position[1] + 1] = P
		position[1] = position[1]+1
	elif decision == 'left':
		tilemap[position[0] - 1][position[1]] = P
		position[0] = position[0]-1
	elif decision == 'right':
		tilemap[position[0] + 1][position[1]] = P
		position[0] = position[0]+1

'''
Fixes Matrix so that y!=x. Ask no questions, just take it for granted,
I don't even understand.
'''
def fixMatrix(matrix):
    newMatrix = [[0 for y in range(MAPHEIGHT)] for x in range(MAPWIDTH)]
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            newMatrix[x][y] = matrix[y][x]
    global tilemap
    tilemap = newMatrix

def main():
	if len(sys.argv) >= 2: #reads file name, ignores all other arguments passed
		if sys.argv[1] == "-noGraphics" or sys.argv[1] == "-ng":
			map_file = "map00.txt"
		elif sys.argv[1] == "-initOverride" or sys.argv[1] == "-r":
			map_file = "map00.txt"	
		elif sys.argv[1] == "-fast" or sys.argv[1] == "-f":
			map_file = "map00.txt"
		else:
			map_file = sys.argv[1]
	else:
		map_file = "map00.txt"

	global MAPHEIGHT
	global MAPWIDTH
	global tilemap

	map_info = readMap(map_file)
	MAPHEIGHT = map_info[0][1]
	MAPWIDTH = map_info[0][0]
	tilemap = map_info[1]
        
        #swap tiles to match the input map
        fixMatrix(tilemap)

	#turn off map printing w/ -noGraphics
	noGraphics = False
	if len(sys.argv) >= 2:
		for i in range(len(sys.argv)):
			if sys.argv[i] == "-noGraphics" or sys.argv[i] == "-ng":
				noGraphics = True
	if noGraphics == False:
		#initialize the display
		pygame.init()
		pygame.display.set_caption("Walter Wanderley")
       		DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

	initPlayerAndPortal()
	steps = 0               #steps to find goal
	df = DecisionFactory()  #initialize DecisionFactory
	
	fast = False
	if len(sys.argv) >= 2:
		for i in range(len(sys.argv)):
			if sys.argv[i] == "-fast" or sys.argv[i] == "-f":
				fast = True
	printTilemap()
	while True:
		if noGraphics == False:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
		
		if fast == False:		
			time.sleep(0.08)
		print

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
		steps += 1
                print "Steps: ", steps
		if result == 'success':
			movePlayer(position, decision)

	    	printTilemap()
		
		if noGraphics == False:
			#draw map to screen	
			for column in range(MAPWIDTH):
				for row in range(MAPHEIGHT):
					pygame.draw.rect(DISPLAYSURF, colors[tilemap[column][row]], (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
			
			pygame.display.update()


'''
	Flow control
'''
if __name__ == "__main__":
	main()
