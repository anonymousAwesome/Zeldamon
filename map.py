import pygame
import numpy as np
import os.path
import window

MapSpriteX=16
MapSpriteY=16

MultiplyScale=4

SpriteSizeX=MapSpriteX*MultiplyScale
SpriteSizeY=MapSpriteY*MultiplyScale


#creating a numpy array to store the map information
MapArray=np.array([
						[1,1,1,2,1,1,1,1,1,2,3,3,2,1,1,1,1,1,2,1],
						[2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2],
						[2,1,4,0,4,0,4,0,4,0,4,0,4,0,4,0,4,0,1,2],
						[2,0,0,0,0,2,0,0,0,0,0,1,1,1,1,1,1,1,1,2],
						[2,0,2,0,0,2,0,0,0,0,1,1,1,1,1,1,1,1,1,2],
						[2,0,0,0,0,2,0,0,5,0,0,5,5,1,1,1,1,1,1,2],
						[2,0,2,0,0,2,0,0,5,0,1,1,1,1,1,1,1,1,1,2],
						[2,0,0,0,0,2,0,0,5,0,0,1,5,1,1,1,1,1,1,2],
						[1,0,2,0,0,2,0,0,0,0,1,1,1,1,1,1,1,1,1,2],
						[1,0,0,0,0,2,0,5,0,0,0,1,1,1,1,1,1,1,1,2],
						[1,0,2,0,0,2,0,5,0,0,1,1,1,1,1,1,1,1,1,2],
						[1,0,0,0,0,2,0,0,5,5,5,5,5,1,1,1,1,1,1,2],
						[1,0,2,0,0,2,0,0,0,0,1,1,1,1,1,1,1,1,1,2],
						[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
						])

# -OR-
#MapArray=np.ones((64,48))

#Figure the size of the map in pixels
MapSize=pygame.Rect(0,0,MapArray.shape[1]*SpriteSizeX,MapArray.shape[0]*SpriteSizeY)


#loads the tileset image into system memory
tilemap_image=pygame.image.load(os.path.join("images","pokemonSprites.png")).convert()


#defining the locations within the tilemap image: [x,y]
#Technically this isn't necessary; I could take the lists here and place them directly into the dictionary below.  I don't do this because I want it to be human-readable.
#I'll remove this step once I code a parser for the Tiled .TMX format.
blank=[112,0]
flower=[64,64]
gravel=[192,0]
CosmeticGrassFull=[256,0]
CosmeticGrassSparse=[256,48]
barrier=[224,64,"Solid"]
realgrass=[272,0]
fence=[240,64]
bouncy=[256,64,"bouncy"]

TileDict={
			0:blank,
			1:gravel,
			2:barrier,
			3:realgrass,
			4:CosmeticGrassSparse,
			5:bouncy
			}


#This class holds a tile image and rect in memory.
class ImageBlock(pygame.sprite.Sprite):
	
	def __init__(self,imageFile,tilemapx,tilemapy):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self) 

		#Load image from disk and create a subsurface of the specified location within the tilemap
		self.image = imageFile.subsurface(tilemapx,tilemapy,MapSpriteX,MapSpriteY)

		#scales the images to the expected tile size
		self.image=pygame.transform.scale(self.image,(SpriteSizeX, SpriteSizeY))

		# Fetch the rectangle object that has the dimensions of the image with the command self.image.get_rect()
		# Use the retrieved rect to update the position of the ImageBlock object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()


def generate_map_tiles():
	map_tiles_group=pygame.sprite.Group()

	#for each x,y coordinate and the associated array value:
	for index, x in np.ndenumerate(MapArray):
	
		#Create a block based on the x,y coordinates given at the appropriate place in the tile dictionary.
		# new block object = block class (where to pull the image from, the first value in the array in the appropriate place in the tile dictionary, the second value in same)
		block = ImageBlock(tilemap_image,TileDict[x][0],TileDict[x][1])
		if "Solid" in TileDict[x]:
			block.walkable=False
		if "bouncy" in TileDict[x]:
			block.bouncy=True

		# Draw the block at the location on-screen equivalent to its location in the array
		block.rect.x = index[1]*SpriteSizeX
		block.rect.y = index[0]*SpriteSizeY

		# Add the block to the list of background sprites
		map_tiles_group.add(block)
	return map_tiles_group


map_group=generate_map_tiles()