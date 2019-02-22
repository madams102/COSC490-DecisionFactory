import sys

def readMap(file):
	try:
		src = open(file)	#opens file as read-only
	except:
		print "Input File Error:", file, "could not be found."
		#could use th s to gen random map if prompted by user?
		sys.exit(1)

	dimensions = [0,0] #0: height/rows, 1: width/cols
	tilemap = []
	

	try:
		while True:
			i = 0
			row = []
			line = src.readline()
			
			if not line:			#if no line is read
					break
			
			dimensions[1] += 1
			while line[i] != '\n':
				if line[i].upper() == 'F':
					row.append(0)
				elif line[i].upper() == "W":
					row.append(1)
				else:
					row.append('x')

				i += 1

			if i > dimensions[0]:
				dimensions[0] = i		

			tilemap.append(row)

	except:
		print "Format Error: File does not match expected input. See README for formatting tips."
		sys.exit(2)

	src.close()
	map_info = [dimensions, tilemap]
	return map_info
