import random
import numpy as np

'''
All functions related to memory will start with "m_"
'''

class DecisionFactory:
	def __init__(self, name='Walter Wanderley'):
		self.name = name
		self.directions = ['wait', 'up', 'down', 'right', 'left']
		self.failed_directions = []
		self.last_result = 'start'
		self.last_direction = 'wait'
                self.pos = [0, 0] #this is the players x,y coords in the 'memory'
                self.memory = np.full((1, 1), '?')
	#Note: we have relativistic coordinates recorded here, since the map
	# is relative to the player's sfirst known and recorded position:
	#self.state.pos = (0,0)
        
        def m_printMem(self):
            for y in range(0, len(self.memory)):
                    for x in range(0, len(self.memory[0])):
                        print self.memory[y][x],
                    print

        def m_fixMatrix(self):
            newMatrix = [[0 for y in range(len(self.memory))] for x in range(len(self.memory[0]))]
            for y in range(len(self.memory)):
                for x in range(len(self.memory[0])):
                    newMatrix[x][y] = self.memory[y][x]
            self.memory = newMatrix

        def m_extendArray(self, direction):
                if direction == 'up':
                    self.pos[0] -= 1
                elif direction == 'down':
                    self.pos[0] += 1
                elif direction == 'left':
                    self.pos[1] += 1
                elif direction == 'right':
                    self.pos[1] -= 1

                #check if player is in memories current bounds
                if 0 >= self.pos[0]: #check left side
                    self.pos[0] += 1
                    self.memory = np.insert(self.memory, 0, '?', axis=0)
                elif len(self.memory) < self.pos[0]: #check right side
                    self.pos[0] -= 1
                    self.memory = np.insert(self.memory, len(self.memory-1), '?', axis=0)
                elif 0 >= self.pos[1]: #check top side
                    self.pos[1] -= 1
                    self.memory = np.insert(self.memory, 0, '?', axis=1)
                elif len(self.memory[0]) < self.pos[1]: #check bottom side
                    self.pos[1] += 1
                    self.memory = np.insert(self.memory, len(self.memory[0]-1), '?', axis=1)

#        def movePos(self, direction):

	def get_decision(self, verbose = True):
		# return self.random_direction()
                self.m_fixMatrix()
                print self.pos
		self.m_printMem()
                direction = self.better_than_random()
                self.m_extendArray(direction)
#                self.movePos()
                return direction 


	def random_direction(self):
		#random.randint(0,4) #Includes wait state
		r = random.randint(1,4) #Does NOT include wait state

		return self.directions[r]

	def better_than_random(self):
		r = self.random_direction()

		# print "Last result: ", self.last_result
		# print "Last direction: ", self.last_direction

		self.failed_directions.extend(self.last_direction)

		if self.last_result != 'success':
			self.failed_directions.extend(self.last_direction)

			r = random.randint(1,4)

			while self.directions[r] in self.failed_directions:
				# print "Failed:", self.failed_directions
				r = random.randint(1,4)

			# print self.directions[r]
			return self.directions[r]
		
		else:	
			self.failed_directions = []


			# r = self.last_direction
			r = self.random_direction()
			# print r
			return r

	def put_result(self, result):
		self.result = result

