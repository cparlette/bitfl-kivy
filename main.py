from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.animation import Animation

# Version used by buildozer for android builds
__version__ = "0.0.4"

class Location(Button):
	button_index = NumericProperty(1)
	popup_menu = None
	def clicked(self):
		#this particular button was clicked, so instruct the player to move here
		#check first to see if the player is in the middle of moving
		if self.parent.player1.is_moving == 0:
			self.parent.player1.move(self.button_index)
		

class BITFLGame(FloatLayout):
	#player_stats = StringProperty("")
	#list of the buttons, must be instantiated later or else it's just empty ObjectProperties
	location_list = []
	'''
	location_list numbering scheme looks like this:
	0	1	2	3	4
	13				5
	12				6
	11	10	9	8	7
	'''
	def initial_setup(self):
		#add the menu buttons here, although this might be a poor place
		#Luxury Apartments
		self.upper_left.popup_menu = CustomPopup()
		self.upper_left.popup_menu.title = self.upper_left.text
		self.upper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Relax", on_press=lambda a: self.change_player_stats(happiness=5)))
		self.upper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Read a book", on_press=lambda a: self.change_player_stats(knowledge=5)))
		
		#Rent Office
		self.upper_midleft.popup_menu = CustomPopup()
		self.upper_midleft.popup_menu.title = self.upper_midleft.text
		self.upper_midleft.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Pay Rent", on_press=lambda a: self.change_player_stats(money=-100)))
		self.upper_midleft.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Get your mail", on_press=lambda a: self.change_player_stats(happiness=1)))

		#Standard Apartment
		self.upper_center.popup_menu = CustomPopup()
		self.upper_center.popup_menu.title = self.upper_center.text
		self.upper_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Relax", on_press=lambda a: self.change_player_stats(happiness=5)))
		self.upper_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Read a book", on_press=lambda a: self.change_player_stats(knowledge=5)))
		self.upper_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Throw a party", on_press=lambda a: self.change_player_stats(happiness=15, money=-50)))
		self.upper_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Work remotely doing data entry", on_press=lambda a: self.change_player_stats(money=25, happiness=-1)))
		
		#Pawn Shop
		self.upper_midright.popup_menu = CustomPopup()
		self.upper_midright.popup_menu.title = self.upper_midright.text
		self.upper_midright.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy book on sale", on_press=lambda a: self.change_player_stats(knowledge=5, money=-10)))
		self.upper_midright.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Sell your guitar", on_press=lambda a: self.change_player_stats(money=75, happiness=-3)))
		
		#Z-Mart
		self.upper_right.popup_menu = CustomPopup()
		self.upper_right.popup_menu.title = self.upper_right.text
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Refrigerator", on_press=lambda a: self.change_player_stats(money=-250, happiness=5)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Bicycle", on_press=lambda a: self.change_player_stats(money=-150, happiness=10)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Encyclopedia Set", on_press=lambda a: self.change_player_stats(money=-50, knowledge=10)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Stereo", on_press=lambda a: self.change_player_stats(money=-100, happiness=15)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Gaming Computer", on_press=lambda a: self.change_player_stats(money=-350, happiness=20)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy DVD", on_press=lambda a: self.change_player_stats(money=-10, happiness=1)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Yanni's Greatest Hits", on_press=lambda a: self.change_player_stats(money=-30, happiness=2)))
		self.upper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Call of Duty 27", on_press=lambda a: self.change_player_stats(money=-60, happiness=5)))
		
		#Fast Food Restaurant
		self.midupper_right.popup_menu = CustomPopup()
		self.midupper_right.popup_menu.title = self.midupper_right.text
		self.midupper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Sad Meal", on_press=lambda a: self.change_player_stats(money=-5, happiness=-1)))
		self.midupper_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Gigantoburger Combo", on_press=lambda a: self.change_player_stats(money=-15, happiness=1)))
		
		#Clothing Store
		self.midlower_right.popup_menu = CustomPopup()
		self.midlower_right.popup_menu.title = self.midlower_right.text
		self.midlower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Casual Clothes", on_press=lambda a: self.change_player_stats(money=-50, happiness=10)))
		self.midlower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Business Casual Clothes", on_press=lambda a: self.change_player_stats(money=-130, happiness=5)))
		self.midlower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Business Clothes", on_press=lambda a: self.change_player_stats(money=-250, happiness=2)))
		self.midlower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Formal Clothes", on_press=lambda a: self.change_player_stats(money=-360, happiness=1)))
		
		#Socket City
		self.lower_right.popup_menu = CustomPopup()
		self.lower_right.popup_menu.title = self.lower_right.text
		self.lower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Washer/Dryer", on_press=lambda a: self.change_player_stats(money=-300)))
		self.lower_right.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Refrigerator", on_press=lambda a: self.change_player_stats(money=-250)))
		
		#University
		self.lower_midright.popup_menu = CustomPopup()
		self.lower_midright.popup_menu.title = self.lower_midright.text
		self.lower_midright.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Take CompSci Class", on_press=lambda a: self.change_player_stats(knowledge=50)))
		self.lower_midright.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Take English Class", on_press=lambda a: self.change_player_stats(knowledge=50)))
		
		#Blank
		self.lower_center.popup_menu = CustomPopup()
		self.lower_center.popup_menu.title = self.lower_center.text
		self.lower_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Knowledge", on_press=lambda a: self.change_player_stats(knowledge=1)))
		self.lower_center.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Money", on_press=lambda a: self.change_player_stats(money=50)))
		
		#Employment Office
		self.lower_midleft.popup_menu = CustomPopup()
		self.lower_midleft.popup_menu.title = self.lower_midleft.text
		self.lower_midleft.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Knowledge", on_press=lambda a: self.change_player_stats(knowledge=1)))
		self.lower_midleft.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Money", on_press=lambda a: self.change_player_stats(money=50)))
		
		#Factory
		self.lower_left.popup_menu = CustomPopup()
		self.lower_left.popup_menu.title = self.lower_left.text
		self.lower_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Knowledge", on_press=lambda a: self.change_player_stats(knowledge=1)))
		self.lower_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Increase Money", on_press=lambda a: self.change_player_stats(money=50)))
		
		#Bank
		self.midlower_left.popup_menu = CustomPopup()
		self.midlower_left.popup_menu.title = self.midlower_left.text
		self.midlower_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Withdraw Money", on_press=lambda a: self.change_player_stats(money=200)))
		self.midlower_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Rob Bank", on_press=lambda a: self.change_player_stats(money=550)))
		
		#Black's Market
		self.midupper_left.popup_menu = CustomPopup()
		self.midupper_left.popup_menu.title = self.midupper_left.text
		self.midupper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Bacon", on_press=lambda a: self.change_player_stats(money=-10, happiness=10)))
		self.midupper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Sushi", on_press=lambda a: self.change_player_stats(money=-20, happiness=20)))
		self.midupper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Salad", on_press=lambda a: self.change_player_stats(money=-10, happiness=2)))
		self.midupper_left.popup_menu.ids.right_popup_section.add_widget(
			Button(text="Buy Frozen Pizza", on_press=lambda a: self.change_player_stats(money=-10, happiness=5)))
		
		#set up the location_list after the buttons are actually buttons and not just ObjectProperty
		#there might be a better way but this actually works
		self.location_list = [self.upper_left, self.upper_midleft,
						self.upper_center, self.upper_midright, self.upper_right,
						self.midupper_right, self.midlower_right, self.lower_right,
						self.lower_midright, self.lower_center, self.lower_midleft,
						self.lower_left, self.midlower_left, self.midupper_left
						]
	
	def update_player_stats(self):
		#print out the current player stats in the middle of the screen
		stats = "Player 1 current stats\n"
		stats += "Knowledge: "+str(self.player1.knowledge)+"\n"
		stats += "Money: "+str(self.player1.money)+"\n"
		stats += "Happiness: "+str(self.player1.happiness)+"\n"
		App.get_running_app().player_stats = stats

	def change_player_stats(self, knowledge=0, money=0, happiness=0):
		self.player1.knowledge += knowledge
		self.player1.money += money
		self.player1.happiness += happiness
		self.update_player_stats()

	

class Player(Widget):
	#player stats
	knowledge = 0
	money = 1000
	happiness = 50
	#keep track of where the player is currently
	location_index = NumericProperty(2)
	is_moving = NumericProperty(0)
	
	#finished_moving is needed since an animation's on_complete needs to call a function
	def finished_moving(self, instance, value):
		#update the player to not be moving
		self.is_moving = 0
		#Open the popup from that location
		self.parent.location_list[self.location_index].popup_menu.open()
		
	
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
	pass

class BITFLApp(App):
	player_stats = StringProperty("")
	def build(self):
		game = BITFLGame()
		#need to setup the button list AFTER instantiation, not sure if there's a better way
		game.initial_setup()
		game.update_player_stats()
		return game

if __name__ == '__main__':
	BITFLApp().run()


