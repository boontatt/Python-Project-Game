import pygame
import game1
import game2
from sys import exit

class Button:
	"""
	Creates a functional button. 
	Will return True or False every time the draw method is called
	depending on whether the button is being pressed
	"""
	def __init__(self, text, text_size, pos, width, height, screen, elevation):
		# Screen to display the button
		self.screen = screen
		
		# Variables needed for the button
		self.pressed = False
		self.hovered = False
		self.elevation = elevation
		self.dynamic_elevation = elevation
		self.ori_y = pos[1]

		# Hovered sound
		# References: https://www.youtube.com/watch?v=gFEbM-8Ypj0&list=PLFM5gSFqaZ4_q7uHLYtBXmvQwEwENEpHu&index=3
		self.hovered_sound = pygame.mixer.Sound("assets/sound/Hovered.wav") 

		# The button itself
		self.top_rect = pygame.Rect(pos, (width, height))
		self.top_rect_color = "#aac9fa"
		
		# The "Shadow" of the button
		self.bottom_rect = pygame.Rect(pos, (width, height))
		self.bottom_rect_color = "#354b5e"

		# Text on the button
		self.font = pygame.font.Font("assets/font/Pixeltype.ttf", text_size)
		self.text_surf = self.font.render(text, False, "White")
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# Code for the elevation effect of the button
		self.top_rect.y = self.ori_y - self.dynamic_elevation
		self.text_rect.center = self.top_rect.center
		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

		# Draw the button
		pygame.draw.rect(self.screen, self.bottom_rect_color, self.bottom_rect, border_radius= 30)
		pygame.draw.rect(self.screen, self.top_rect_color, self.top_rect, border_radius= 30)

		# Displaying the text
		self.screen.blit(self.text_surf, self.text_rect)
		return self.check_clicked()

	def check_clicked(self):
		mouse_pos = pygame.mouse.get_pos() 

		# If the cursor is right on top of the button
		if self.top_rect.collidepoint(mouse_pos):
			self.top_rect_color = "Red"
			if not self.hovered:
				self.hovered = True
				self.hovered_sound.play()
			
			# If we are holding the left click
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elevation = 0
				self.pressed = True
			else:

				# If we are not holding the left click
				self.dynamic_elevation = self.elevation

				# If we did press the button
				if self.pressed:
					self.pressed = False
					return True

				# If we didn't press the button
				else:
					return False
		else:
			# If the cursor is not on top of the button
			self.hovered = False
			self.dynamic_elevation = self.elevation
			self.top_rect_color = "#aac9fa"
			self.pressed = False
			return False


def run(screen, clock):
	# Background Music
	# References: https://www.youtube.com/watch?v=xb0cMDEyMzg&list=PLFM5gSFqaZ4_q7uHLYtBXmvQwEwENEpHu&index=7
	pygame.mixer.music.load("assets/sound/bgm/bgm_mainmenu.mp3")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(loops = -1)

	# Font type and size
	# References: https://github.com/clear-code-projects/UltimatePygameIntro/tree/main/font
	font = pygame.font.Font("assets/font/Pixeltype.ttf", 120)
	
	# Title
	title_surf = font.render("WASSUP bro", False, "White")
	title_rect = title_surf.get_rect(center = (400,150))
	
	# White background title
	bg_title1 = pygame.Surface((title_rect.width + 100, title_rect.height + 50))
	bg_title_rect1 = bg_title1.get_rect(center = (title_rect.center))
	bg_title1.fill((64,64,64))

	# Dark background title
	bg_title2 = pygame.Surface((bg_title_rect1.width + 20, bg_title_rect1.height + 20))
	bg_title_rect2 = bg_title2.get_rect(center = (title_rect.center))
	bg_title2.fill(("White"))
	
	# Background
	# References: https://www.behance.net/gallery/65290819/Pixel-Art-Backgrounds-Tutorial-Skip
	background = pygame.image.load("assets/image/background.jpg").convert()
	background_rect = background.get_rect(topleft = (0,0))

	# Buttons
	game1_button = Button("Trex", 40, (300,400), 200, 40, screen, 5)
	game2_button = Button("Flappy Bird", 40, (300,455), 200, 40, screen, 5)
	quit_button = Button("Quit", 40, (300,510), 200, 40, screen, 5)
	
	# Sound effect when clicking the button
	# References: https://www.youtube.com/watch?v=-D2iL1GYdx0&list=PLFM5gSFqaZ4_q7uHLYtBXmvQwEwENEpHu&index=3
	click_sound = pygame.mixer.Sound("assets/sound/Click_sound.wav")
	
	# Displaying Main Menu Screen
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		
		# Draw the screen
		screen.blit(background, background_rect)
		screen.blit(bg_title2, bg_title_rect2)
		screen.blit(bg_title1, bg_title_rect1)
		screen.blit(title_surf, title_rect)

		# Run game1 if game1 button is clicked
		if game1_button.draw():
			click_sound.play()
			game1.run()

		# Run game2 if game2 button is clicked
		if game2_button.draw():
			click_sound.play()
			game2.run()

		# Quit the game if quit button is clicked
		if quit_button.draw():
			click_sound.play()
			pygame.quit()
			exit()

		pygame.display.update()
		clock.tick(60)
