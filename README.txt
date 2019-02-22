TODO: Nada

CHNGES:
      Ready to show off on monday. Up to date minus Alec's work for the week.
      

OVERRIDE INITIALIZATION/NO GRAPHICS/NO SLEEP HOWTO:
By using a map with a 'p' and/or 'g' tile in them, we can override their positions and randomly place them by using the command:
      `python framework.py mapXX.txt -initOverride` or `-r`
      
We can also turn off graphics with the -noGraphics parameter
      `python framework.py mapXX.txt -noGraphics` or `-ng`
      
Lastly, we can make the program not sleep inbetween steps by the command
      `python framework.py mapXX.txt -fast` or `-f`
      
NOTE: The mapXX.txt is optional in all of these. The command line parameters can also appear in any order, so long 
      as the mapXX.txt comes first


READING MAPS BY INPUT
      IMPORTANT: map files must have a new line at the end of the matrix
      
HOW TO DO:
python framework.py <map_file_name>
(test map will be used if no map file is passed)

ex:
WWWWW
WFFFW
WFFFW
WFFFW
WWWWW

<end-of-file>

NOTE:
changed the following (I know there is a bit of lost of meaning with these variable names but it is the most efficient method that I could come up with):
GRND 	->	F	#floor
WALL 	->	W 	#wall
PLAYER	->	P 	#player
PORTAL	->	G 	#goal
NONE 	-> 	N 	#none
