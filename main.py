from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.animation import Animation

# Version used by buildozer for android builds
__version__ = "0.0.3"

class Location(Button):
	button_index = NumericProperty(1)
	def clicked(self):
		#this particular button was clicked, so instruct the player to move here
		#check first to see if the player is in the middle of moving
		if self.parent.player1.is_moving == 0:
			self.parent.player1.move(self.button_index)
		

class BITFLGame(FloatLayout):
	#the player
	player1 = ObjectProperty(None)
	
	#all the buttons
	upper_left = ObjectProperty(None)
	upper_midleft = ObjectProperty(None)
	upper_center = ObjectProperty(None)
	upper_midright = ObjectProperty(None)
	upper_right = ObjectProperty(None)
	midupper_right = ObjectProperty(None)
	midlower_right = ObjectProperty(None)
	lower_right = ObjectProperty(None)
	lower_midright = ObjectProperty(None)
	lower_center = ObjectProperty(None)
	lower_midleft = ObjectProperty(None)
	lower_left = ObjectProperty(None)
	midlower_left = ObjectProperty(None)
	midupper_left = ObjectProperty(None)
	
	# the center of the screen
	middle_section = ObjectProperty(None)
	player_stats = ObjectProperty(None)
	
	#list of the buttons, must be instantiated later or else it's just empty ObjectProperties
	location_list = []
	'''
	location_list numbering scheme looks like this:
	0	1	2	3	4
	13				5
	12				6
	11	10	9	8	7
	'''
	def set_list(self):
		#set up the location_list after the buttons are actually buttons and not just ObjectProperty
		#there might be a better way but this actually works
		self.location_list = [self.upper_left, self.upper_midleft,
						self.upper_center, self.upper_midright, self.upper_right,
						self.midupper_right, self.midlower_right, self.lower_right,
						self.lower_midright, self.lower_center, self.lower_midleft,
						self.lower_left, self.midlower_left, self.midupper_left
						]
	
	def player_stats(self):
		#print out the current player stats in the middle of the screen
		stats = "Player 1 current stats\n"
		stats += "Knowledge: "+str(self.player1.knowledge)+"\n"
		stats += "Money: "+str(self.player1.money)+"\n"
		stats += "Happiness: "+str(self.player1.happiness)+"\n"
		return stats
	

class Player(Widget):
	#player stats
	knowledge = 0
	money = 100
	happiness = 50
	#keep track of where the player is currently
	location_index = NumericProperty(2)
	is_moving = NumericProperty(0)
	
	#finished_moving is needed since an animation's on_complete needs to call a function
	def finished_moving(self, instance, value):
		#update the player to not be moving
		self.is_moving = 0
		'''
		#OLD WAY of doing the popup
		#Create a popup with this location's information
		content = Button(text=self.parent.location_list[self.location_index].text)
		popup = Popup(title='Test popup', content=content, size_hint=(.8, .8))
		# bind the on_press event of the button to the dismiss function
		content.bind(on_press=popup.dismiss)
		#open the popup
		popup.open()
		'''
		popup = CustomPopup()
		popup.title = "TESTING THIS"
		popup.ids.left_label.text = "whatup"
		popup.open()
		
		#try changing the middle_section text here just to see if it works
	
	def move(self, target_button_index):
		#tell the other buttons that we're moving, so they don't work
		self.is_moving = 1
		
		#find out how far away we are from the target button if we go clockwise
		direction = 'clockwise'
		distance = 0
		total_locations = len(self.parent.location_list)
		max_distance = total_locations / 2
		if target_button_index > self.location_index:
			distance = target_button_index - self.location_index
		else:
			#handle if we wrap around from 13 to 0
			distance += (total_locations - self.location_index)
			distance += target_button_index
		
		#if it's too far to go clockwise, then go counter-clockwise
		if distance > max_distance:
			direction = 'counterclockwise'
			distance = (total_locations - distance)
		
		#make a list of buttons in the correct order
		#I had to add +/-1 to all the indices because I don't want the current button, and I want to get
		#the target button as well.  There's probably a cleaner way to do that rather than +1
		button_list = []
		if direction == 'clockwise':
			if target_button_index == 0:
				#special case where the target is 0 (upper left)
				button_list = self.parent.location_list[self.location_index+1:]
				button_list.append(self.parent.location_list[0])
			elif self.location_index + distance > total_locations:
				#player is wrapping around from 13 to 0
				button_list = self.parent.location_list[self.location_index+1:]
				button_list += self.parent.location_list[:target_button_index+1]
			else:
				#player is going clockwise without wrapping around the upper left
				button_list = self.parent.location_list[self.location_index+1:target_button_index+1]
		elif direction == 'counterclockwise':
			if target_button_index == 0:
				#special case where the target is 0 (upper left)
				button_list = self.parent.location_list[self.location_index-1::-1]
			elif self.location_index == 0:
				#special case where the player is currently on 0 (upper left)
				button_list = self.parent.location_list[total_locations:target_button_index-1:-1]
			elif self.location_index - distance < 0:
				#player is wrapping around from 0 to 13
				button_list = self.parent.location_list[self.location_index-1::-1]
				button_list += self.parent.location_list[total_locations:target_button_index-1:-1]
			else:
				#player is going counterclockwise without wrapping around the upper left
				button_list = self.parent.location_list[self.location_index-1:target_button_index-1:-1]
		
		#debugging
		print "button_list is"
		for button in button_list:
			print button.button_index
		print "==end of button list"
		print "direction is "+direction
		print "distance is "+str(distance)
		print "self.location_index is "+str(self.location_index)
		print "target_button_index is "+str(target_button_index)
		print "total_locations is "+str(total_locations)
		print "max_distance is "+str(max_distance)
		
		
		#make the animation, set the initial duration to 0 so it starts immediately
		animation = Animation(duration=0)
		#have the player move to the next button in the list
		for button in button_list:
			animation += Animation(
							pos=(
								button.center[0]-(self.size[0]/2),
								button.center[1]-(self.size[1]/2)
							),
							duration=.3
						)
		#when the animation completes, call finished_moving(), which will set is_moving to 0
		animation.bind(on_complete=self.finished_moving)
		#run the animations
		animation.start(self)
		
		#set the players location_index so we know where he is
		self.location_index = target_button_index

class CustomPopup(Popup):
	def do_something(self):
		self.parent.knowledge += 1

class BITFLApp(App):
	def build(self):
		game = BITFLGame()
		#need to setup the button list AFTER instantiation, not sure if there's a better way
		game.set_list()
		print "==HEY=="
		print game.location_list
		print game.upper_left
		return game

if __name__ == '__main__':
	BITFLApp().run()


