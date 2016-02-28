#main.py
import os,pickle
from .game_code import core

class Main:
	def __init__(self,config):
		'''stuff'''
	self.save_list = {"a": None, "b":None, "c":None, "d":None,}
	self.loaded = False
	
	if not config.save_dir in os.listdir():
		os.mkdir(config.save_dir)
	try:
		f = open(config.save_dir+'/main.otter','rb')
		self.save_list = pickle.load(f)
		f.close()
	except FileNotFoundError:
		f = open(config.save_dir+'/main.otter','wb')
		pickle.dump(self.save_list,f)
		f.close()
		
	self.city = core.Game(config)
	
	


	def print_main_menu(self):
		print()
		'''lists the options for the main menu'''
		if self.loaded:
			r_text = '''"r" to run your loaded game, or 's' to save it.'''
		else:
			r_text = '''"r" to run a new game! '''
		print("--| Main Menu |--")
		print(r_text)
		print("Or 'l' to load a saved game, and 'q' to quit.")

	def main_menu(self,core):
		'''out of game menu for loading, saving, starting new game'''
		'''has city input for method because its being silly'''
		run_menu = True
		
		while run_menu:
			self.print_main_menu()
			choice = input("Well, what'll it be: ").lower()
			
			if choice == 'q':
				run_menu = False
				print("Goodbye!")
				
			elif choice == 'r' and self.loaded:
				print("Entering active game")
				run_menu = False
				core.city_menu()
				
			elif choice == 'r' and not self.loaded:
				run_menu = False
				print("Starting a new game")
				self.loaded = True
				core.city_menu(new_game=True)
				
			elif choice == 's':
				self.save_menu()
				
			elif choice == 'l':
				self.load_menu()
				
			else:
				print("Not a valid option")
		
	def print_save_load_menu(self):
		'''formats and makes pretty the info in self.save_life'''
		print()
		print("Save Game List!")
		for each in ('A','B','C','D'):
			print(each+":", self.save_list[each.lower()])
		print("Or 'x' to quit this menu.")
		print()
		
	def overwrite_prot(self):
		print("Warning, may overwrite save.")
		option = input("Enter 'y' to overwrite: ").lower()
		if option == 'y':
			print("Overwriting")
			return True
		else:
			print("Cancelling")
			return False
		
	def save_menu(self):
		save_menu = True
		go = True
		while save_menu:
			self.print_save_load_menu()
			option = input("Make your choice: ").lower()
			if option == 'x':
				save_menu = False
			elif option in self.save_list:
				if self.save_list[option] != None:
					if self.overwrite_prot():
						self.save_game(option)
				else:
					self.save_game(option)
					
	def save_game(self,option):
		name = self.character.first_name
		xp = self.character.total_xp
		time = self.total_days
		f = open(config.save_dir+'/main.otter','wb')
		self.save_list[option] = ((name,xp,time))
		pickle.dump(self.save_list,f)
		f.close()
		f = open(config.save_dir+"/"+option+".otter",'wb')
		pickle.dump(self,f)
		f.close()
		
	def load_game(self,option):
		'''gets the filename from self.save_list[option], pickle loads it and sets game = loaded_game, and self.loaded to True'''
		try:
			f = open(config.save_dir+"/"+option+".otter",'rb')
			self = pickle.load(f)
			f.close()
			self.loaded = True
			print("Game loaded!")
		except:
			print("Error: Game not loaded!")
			self.loaded = False
	


		
		
	def load_menu(self):
		'''load version of save game, includes check if self.loaded is true for overwriting loaded games'''
		menu = False
		for each in self.save_list:
			if self.save_list[each] != None:
				menu = True
		if not menu:
			print("There are no save games to load!")
		while menu:
			self.print_save_load_menu()
			choice = input("Your option: ").lower()
			if choice == 'x':
				menu = False
			elif choice in self.save_list and self.loaded:
				print("Warning: This will overwrite your loaded game.")
				option = input("'Y' to load the game: ").lower()
				if option == 'y':
					self.load_game(choice)
					menu = False
			elif choice in self.save_list:
				menu = False
				self.load_game(choice)
				self.loaded = True
				x = input("Enter to continue")