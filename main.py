'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3

Written in Python3.4.2, Windows Environ
'''
class Game:
    '''NOT IMPLIMENTED'''
    def __init__(self):
        self.loaded = False
        self.save_list = {"a": None, "b":None, "c":None, "d":None,}
        import pickle
        try:
            f = open('main.otter','rb')
            self.save_list = pickle.load(f)
            f.close()
        except FileNotFoundError:
            f = open('main.otter','wb')
            pickle.dump(self.save_list,f)
            f.close()
        '''grab the save file master info here'''
        '''key = name, date last played, in-game date, earned xp, total wealth, filename'''
        from settings import GameConfiguration
        self.config = GameConfiguration()
        from random import randint
        self.randint = randint
        
        from director import Director
        from bank import Bank
        from market import Market
        from bar import Bar
        from home import Home
        from hideout import Hideout
        from player import Character
        from event_manager import EventManager
        from job import Job
        
        self.director = Director(self)
        self.bank = Bank(self)
        self.market = Market(self)
        self.bar = Bar(self)
        self.home = Home(self)
        self.hideout = Hideout(self)
        self.character = Character(self)
        self.event_manager = EventManager(self)
        self.job = Job(self)
        
        self.loaded = False
        
        #Former City Stuff Start
        
        self.max_time = 20
        self.available_time = 20
        self.total_days = 1
        self.current_day = 1
        self.weeks = 1
        self.prefix = "city_"
        
        
        
        self.city_menu_choices = {'a':self.bar.menu,'x':self.main_menu,'h':self.hideout.menu,'o':self.home.menu,
        'm':self.market.menu,'c':self.market.menu,'b':self.bank.menu,'j':self.job.menu}
        #Former City Stuff End
        
    def intro(self):
        intro_texts = ("intro1","intro2","intro3","intro4","title","title2")
        for item in intro_texts:
            print(self.config.get_text(item))
            x=input("...")
        x=input("Enter the Game")
    
    
    
    def print_main_menu(self):
        '''lists the options for the main menu'''
        if self.loaded:
            r_text = '''"r" to run your loaded game, or 's' to save it.'''
        else:
            r_text = '''"r" to run a new game! '''
        print("--| Main Menu |--")
        print(r_text)
        print("Or 'l' to load a saved game, and 'q' to quit.")

    def main_menu(self):
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
                self.city_menu()
                self.loaded = True
            elif choice == 'r' and not self.loaded:
                print("Starting a new game")
                #self.intro()
                run_menu = False
                self.loaded = True
                self.city_menu()
            elif choice == 's':
                self.save_menu()
            elif choice == 'l':
                self.load_menu()
            else:
                print("Not a valid option")
                
    #former city stuff section
    
    def advance_day(self,penalty=0):
        '''called when ending a day at Hideout or Home, or by a Heist'''
        self.available_time = self.max_time + penalty
        self.total_days += 1
        self.job.can_work = True
        self.character.update_everything()
        if self.current_day < 7:
            self.current_day += 1
        else:
            self.current_day = 1
            self.weeks += 1
            self.bank.deductions(self)
            '''self.market.refresh() here'''
            
    def time_of_day(self):
        '''returns a string for time-based description key generation'''
        '''Currently -1 to available time because 20 isn't in range(14,20) but in 14,21 and I want to keep the ranges somewhat sane'''
        if self.available_time -1 in range(14,20):
            return 'morning'
        elif self.available_time -1 in range(9,14):
            return 'afternoon'
        elif self.available_time -1 in range(4,9):
            return 'evening'
        else:
            return 'night'
            
    def time_for_menu(self):
        print("It is day",self.current_day," of week", str(self.weeks)+".")
        print("There are",self.available_time,"hours left available today.")
            
    def print_city_menu(self):
        self.time_for_menu()
        print("B for Bank | J for Job ")
        print("M for Market | C for Store")
        print("H for Hideout | O for Home")
        print("A for Bar | X for Main Menu")
        print()
            
    def city_menu(self):
        print()
        desc = self.config.get_text(self.prefix+self.time_of_day())
        #results in city_morning, from prefix "city_" and time_of_day "morning"
        print(desc)
        print()
        run_menu = True
        while run_menu:
            self.print_city_menu()
            choice = input("Choose the option: ").lower()
            if choice in self.city_menu_choices:
                run_menu = True
                if choice == 'c':
                    self.city_menu_choices[choice](self,market=False)
                elif choice == 'x':
                    self.city_menu_choices[choice]()
                else:
                    self.city_menu_choices[choice](self)
            else:
                print("That is not a valid option")
                
    #saving and loading section
                
    def print_save_load_menu(self):
        '''formats and makes pretty the info in self.save_life'''
        for each in self.save_list:
            print(each, self.save_list[each])
        
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
                    if overwrite_prot():
                        self.save_game(option)
                else:
                    self.save_game(option)
                    
    def save_game(self,option):
        name = self.character.first_name
        xp = self.character.total_xp
        time = self.city.total_days
        f = open('main.otter','wb')
        self.save_list[option] = ((name,xp,time))
        pickle.dump(self.save_list,f)
        f.close()
        f = open(option+".otter",'wb')
        pickle.dump(self,f)
        f.close()
        
    def load_game(self,option):
        '''gets the filename from self.save_list[option], pickle loads it and sets game = loaded_game, and self.loaded to True'''
        try:
            f = open(option+".otter",'rb')
            self = pickle.load(f)
            f.close()
            self.loaded = True
            print("Game loaded this is load_game!")
            print(self.loaded)
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
            choice = input("'x' to quit, or select an option to load that game: ").lower()
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
                        
                        

##import pickle


##game = Game()


                    
##if __name__ == '__main__':
##    #intro()
##    #game.city.menu()
##    game.main_menu()
##    #game.market.menu()
    