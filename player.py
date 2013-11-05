import pygame
import os.path

#import map to get access to the MultiplyScale variable
import map

PlayerMove=3


#This class represents the player class
class playerClass(pygame.sprite.Sprite):
	
	def __init__(self,pokemonfile):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self) 

		player_image=pygame.image.load(os.path.join("images","PokemonSprites",pokemonfile)).convert_alpha()

		#Create a image subsurface from the player spritesheet.

		#Player numbers.  Need to add the code to crop transparency.  That, or just use the existing code and put the trainer on a pokemon-style sheet.  I dunno.
		#self.FacingDown=player_image.subsurface(0,0,16,16)
		#self.FacingUp=player_image.subsurface(32,0,16,16)
		#self.FacingLeft=player_image.subsurface(0,16,16,16)
		#self.FacingRight=pygame.transform.flip(self.FacingLeft,True,False)

		# -OR-

#Pokemon sheet


	#Facing down

		#Create a temporary subsurface from the player spritesheet
		TempSubsurface=player_image.subsurface(0,64,32,32)

		#Get the a rectangle that crops out empty alpha space.
		TempRect=TempSubsurface.get_bounding_rect()

		#Create the Surface FacingDown that's the width and height of the cropped rectangle, and make sure it can handle per-pixel transparency.
		self.FacingDown=pygame.Surface((TempRect.width,TempRect.height), flags=pygame.SRCALPHA)

		#Take the original image, move it left and up by the difference between the original rectangle and the cropped rectangle
		#As an example, of the original x is 0 and the cropped x is 40, the command will move the image left by 40 to place it right on the FacingDown Surface.
		self.FacingDown.blit(TempSubsurface, (-TempRect.x,-TempRect.y))

	#Facing Up

		#Create a temporary subsurface from the player spritesheet
		TempSubsurface=player_image.subsurface(0,0,32,32)

		#Get the a rectangle that crops out empty alpha space.
		TempRect=TempSubsurface.get_bounding_rect()

		#Create the Surface FacingDown that's the width and height of the cropped rectangle, and make sure it can handle per-pixel transparency.
		self.FacingUp=pygame.Surface((TempRect.width,TempRect.height), flags=pygame.SRCALPHA)

		#Take the original image, move it left and up by the difference between the original rectangle and the cropped rectangle
		#As an example, of the original x is 0 and the cropped x is 40, the command will move the image left by 40 to place it right on the FacingDown Surface.
		self.FacingUp.blit(TempSubsurface, (-TempRect.x,-TempRect.y))


	#Facing Left

		#Create a temporary subsurface from the player spritesheet
		TempSubsurface=player_image.subsurface(32,0,32,32)

		#Get the a rectangle that crops out empty alpha space.
		TempRect=TempSubsurface.get_bounding_rect()

		#Create the Surface FacingDown that's the width and height of the cropped rectangle, and make sure it can handle per-pixel transparency.
		self.FacingLeft=pygame.Surface((TempRect.width,TempRect.height), flags=pygame.SRCALPHA)

		#Take the original image, move it left and up by the difference between the original rectangle and the cropped rectangle
		#As an example, of the original x is 0 and the cropped x is 40, the command will move the image left by 40 to place it right on the FacingDown Surface.
		self.FacingLeft.blit(TempSubsurface, (-TempRect.x,-TempRect.y))


	#Facing Right

		self.FacingRight=pygame.transform.flip(self.FacingLeft,True,False)

		#Create a temporary rectangle based on the image taken from the player spritesheet.
		# Use that information to scale the subsurface of the image by the amount specified in the variable MultiplyScale.
		TempRect=self.FacingDown.get_rect()
		self.FacingDown=pygame.transform.scale(self.FacingDown, (int(TempRect.width*map.MultiplyScale),int(TempRect.height*map.MultiplyScale)))

		TempRect=self.FacingUp.get_rect()
		self.FacingUp=pygame.transform.scale(self.FacingUp, (int(TempRect.width*map.MultiplyScale),int(TempRect.height*map.MultiplyScale)))

		TempRect=self.FacingLeft.get_rect()
		self.FacingLeft=pygame.transform.scale(self.FacingLeft, (int(TempRect.width*map.MultiplyScale),int(TempRect.height*map.MultiplyScale)))

		TempRect=self.FacingRight.get_rect()
		self.FacingRight=pygame.transform.scale(self.FacingRight, (int(TempRect.width*map.MultiplyScale),int(TempRect.height*map.MultiplyScale)))
		
		#Generate a 2-integer pair that is the average width of each facing image and the average height of the same.
		self.bounding=((self.FacingLeft.get_width()+self.FacingUp.get_width()+self.FacingDown.get_width()+self.FacingRight.get_width())//4),((self.FacingLeft.get_height()+self.FacingUp.get_height()+self.FacingDown.get_height()+self.FacingRight.get_height())//4)

		#Scale each image to that size
		self.FacingUp=pygame.transform.scale(self.FacingUp,self.bounding)
		self.FacingDown=pygame.transform.scale(self.FacingDown,self.bounding)
		self.FacingLeft=pygame.transform.scale(self.FacingLeft,self.bounding)
		self.FacingRight=pygame.transform.scale(self.FacingRight,self.bounding)

		
		#Give the player a starting image
		self.image=self.FacingDown

		#Take the rect from the player image and use it as the player rect.
		self.rect = self.image.get_rect()

		self.ForcedLeft=self.ForcedRight=self.ForcedUp=self.ForcedDown=False

		self.KnockedFramesLeft=0

	#This function is only called once when the player collides with something bouncy or takes damage(?).
	def KnockedBack(self,frames, direction):
		self.ForcedLeft=self.ForcedRight=self.ForcedUp=self.ForcedDown=False
		self.KnockedFramesLeft=frames
		if direction=="up":
			self.ForcedUp=True
		if direction=="down":
			self.ForcedDown=True
		if direction=="left":
			self.ForcedLeft=True
		if direction=="right":
			self.ForcedRight=True

	#This function moves the player backwards until the frame counter runs out.

	def KnockedUpdate(self):
			if self.ForcedLeft:
				self.MoveLeft()
			if self.ForcedRight:
				self.MoveRight()
			if self.ForcedUp:
				self.MoveUp()
			if self.ForcedDown:
				self.MoveDown()

			self.KnockedFramesLeft-=1

			if self.KnockedFramesLeft==0:
				self.ForcedLeft=self.ForcedRight=self.ForcedUp=self.ForcedDown=False


# In diagonal cases: it works because if the non-colliding direction is figured first, it doesn't collide.  If the non-colliding direction is figured second, it's already been moved out of collision.
# Took me a while to figure out why it wasn't jumping around on diagonal collision detection like I thought it should.

	def MoveLeft(self):
		if not self.ForcedRight:
			self.rect.x-=PlayerMove
		if not self.ForcedLeft:
			self.image=self.FacingLeft
			self.rect.width=self.FacingLeft.get_width()
			self.rect.height=self.FacingLeft.get_height()
		for sprite in pygame.sprite.spritecollide(self,map.map_group, False):
			if getattr(sprite, 'walkable', True)==False:
				self.rect.left=sprite.rect.right
			if getattr(sprite, 'bouncy', False)==True:
				self.rect.left=sprite.rect.right
				self.KnockedBack(18,"right")

	def MoveRight(self):
		if not self.ForcedLeft:
			self.rect.x+=PlayerMove
		if not self.ForcedRight:
			self.image=self.FacingRight
			self.rect.width=self.FacingRight.get_width()
			self.rect.height=self.FacingRight.get_height()
		for sprite in pygame.sprite.spritecollide(self,map.map_group, False):
			if getattr(sprite, 'walkable', True)==False:
				self.rect.right=sprite.rect.left
			if getattr(sprite, 'bouncy', False)==True:
				self.rect.right=sprite.rect.left
				self.KnockedBack(18,"left")

	def MoveUp(self):
		if not self.ForcedDown:
			self.rect.y-=PlayerMove
		if not self.ForcedUp:
			self.image=self.FacingUp
			self.rect.width=self.FacingUp.get_width()
			self.rect.height=self.FacingUp.get_height()
		for sprite in pygame.sprite.spritecollide(self,map.map_group, False):
			if getattr(sprite, 'walkable', True)==False:
				self.rect.top=sprite.rect.bottom
			if getattr(sprite, 'bouncy', False)==True:
				self.rect.top=sprite.rect.bottom
				self.KnockedBack(18,"down")

	def MoveDown(self):
		if not self.ForcedUp:
			self.rect.y+=PlayerMove
		if not self.ForcedDown:
			self.image=self.FacingDown
			self.rect.width=self.FacingDown.get_width()
			self.rect.height=self.FacingDown.get_height()
		for sprite in pygame.sprite.spritecollide(self,map.map_group, False):
			if getattr(sprite, 'walkable', True)==False:
				self.rect.bottom=sprite.rect.top
			if getattr(sprite, 'bouncy', False)==True:
				self.rect.bottom=sprite.rect.top
				self.KnockedBack(18,"up")


#Creates a list and initializes each pokemon within the party.
pokemonList=[playerClass("001Bulbasaur.png"),playerClass("002Ivysaur.png"),playerClass("003VenusaurLumin.png"),playerClass("004CharmanderLuminAuto.png"),playerClass("005CharmeleonLuminAuto.png"),playerClass("006CharizardLuminAuto.png"),playerClass("007SquirtleLightnessAuto.png"),playerClass("019Rattata.png"),playerClass("025Pikachu.png")]


#Create a reference to the first pokemon in the list called activePokemon
activePokemon=pokemonList[0]
activePokemon.rect.topleft=(128,128)	#Create the starting point for the player.

def pokemonBump(pokemonList,activePokemon):
	tempPokemon=pokemonList[0]
	del [pokemonList[0]]
	pokemonList.append(tempPokemon)
	del activePokemon
	activePokemon=pokemonList[0]
	activePokemon.rect.topleft=tempPokemon.rect.topleft
	#Point them in the right direction when being switched.
	#Otherwise, the pokemon would face the same direction they were last time they were visible.
	if tempPokemon.image==tempPokemon.FacingLeft:
		activePokemon.image=activePokemon.FacingLeft
	if tempPokemon.image==tempPokemon.FacingRight:
		activePokemon.image=activePokemon.FacingRight
	if tempPokemon.image==tempPokemon.FacingUp:
		activePokemon.image=activePokemon.FacingUp
	if tempPokemon.image==tempPokemon.FacingDown:
		activePokemon.image=activePokemon.FacingDown
	#Copies over the knocked status.  At this rate I'll be copying everything over.  I know there has to be a simpler, object-oriented way to only transfer the attributes I want, but I can't figure it out.  So, this will have to do.
	activePokemon.ForcedDown=tempPokemon.ForcedDown
	activePokemon.ForcedUp=tempPokemon.ForcedUp
	activePokemon.ForcedLeft=tempPokemon.ForcedLeft
	activePokemon.ForcedRight=tempPokemon.ForcedRight
	activePokemon.KnockedFramesLeft=tempPokemon.KnockedFramesLeft

	return pokemonList,activePokemon

def player_input(activePokemon):

	keys=pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		activePokemon.MoveLeft()
	if keys[pygame.K_RIGHT]:
		activePokemon.MoveRight()
	if keys[pygame.K_UP]:
		activePokemon.MoveUp()
	if keys[pygame.K_DOWN]:
		activePokemon.MoveDown()

	if activePokemon.KnockedFramesLeft>=0:
		activePokemon.KnockedUpdate()

	return activePokemon


