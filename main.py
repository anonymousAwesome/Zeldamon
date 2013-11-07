import pygame
import window
import player
import map


pygame.init()

WindowX=640
WindowY=576

#Create the main window
screen=pygame.display.set_mode([WindowX,WindowY])

running=True


# -------- Main Program Loop -----------
while running:
	# ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			running=False # Flag that we are done so we exit this loop
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
						#Cycles through the existing pokemon, using code and variables from the player module
						player.pokemonList,player.activePokemon=player.pokemonBump(player.pokemonList,player.activePokemon)
	#gets player input: Left, Right, Up, Down
	player.player_input(player.activePokemon)

	#Centers the camera on the player
	window.camera_update(player.activePokemon)

	#draws the group made up of map tiles
	window.draw_group(map.map_group)

	#draws the player
	window.draw_single(player.activePokemon)

	#does miscellaneous window stuff
	window.remainder_window_update()

# Close the window and quit.
pygame.quit ()

