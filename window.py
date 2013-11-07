import pygame


WindowX=640
WindowY=576

pygame.init()
#Create the main window
screen=pygame.display.set_mode([WindowX,WindowY])

#I placed "import map" here because some of map's functions require an active display
#and an initialized pygame.
import map

#Create a Rect the same size as the screen to use as a camera.
VirtualWindow=pygame.Surface.get_rect(screen)


# Used to manage how fast the screen updates
clock=pygame.time.Clock()


pygame.display.set_caption("ZeldaMon")

#Create a Rect the same size as the screen to use as a camera.
VirtualWindow=pygame.Surface.get_rect(screen)

def camera_update(activePokemon):
	"""Update the camera to center over the player."""

	#Place the center of the screen at the center of the player
	VirtualWindow.center=activePokemon.rect.center

	#If the window is further out than the edge of the map, set the window edge to the edge of the map.
	if VirtualWindow.top<map.MapSize.top:
		VirtualWindow.top=map.MapSize.top

	if VirtualWindow.bottom>map.MapSize.bottom:
		VirtualWindow.bottom=map.MapSize.bottom

	if VirtualWindow.left<map.MapSize.left:
		VirtualWindow.left=map.MapSize.left

	if VirtualWindow.right>map.MapSize.right:
		VirtualWindow.right=map.MapSize.right


def draw_group(sprite_group):
	#Sets screen to white, then blits all sprites to the display screen surface.
	screen.fill((255,255,255))
	for a in sprite_group:
		#If the tile collides with the camera rect; in other words, if the tile is at all on-screen:
		if a.rect.colliderect(VirtualWindow):
			#blit the image of the tile sprite (a.image) to the coordinates listed in the sprite minus the x/y coordinates of the virtual window.
			screen.blit (a.image, [(a.rect.x-VirtualWindow.x),(a.rect.y-VirtualWindow.y)])

def draw_single(sprite):
	screen.blit (sprite.image, [(sprite.rect.x-VirtualWindow.x),(sprite.rect.y-VirtualWindow.y)])


def remainder_window_update():
	#Updates the physical screen with what's been blitted to the screen surface.
	pygame.display.flip()

	# Limit to 80 frames per second
	clock.tick(80)
	# Display FPS on the title bar instead of "zeldamon"
	pygame.display.set_caption(str(clock.get_fps()))