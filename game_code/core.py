'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3

Written in Python3.4.2, Windows Environ
'''

class Game:
    def __init__(self,config,main):
        self.config = config
        self.loaded = False

        from random import randint
        self.randint = randint

        from .director import Director
        from .bank import Bank
        from .market import Market
        from .bar import Bar
        from .home import Home
        from .hideout import Hideout
        from .player import Character
        from .event_manager import EventManager
        from .job import Job
        from game_data.items import upgrades
        

        self.director = Director(self)
        self.bank = Bank(self)
        self.market = Market(self)
        self.bar = Bar(self)
        self.home = Home(self)
        self.hideout = Hideout(self)
        self.character = Character(self)
        self.event_manager = EventManager(self)
        self.job = Job(self)
        self.upgrade_list = upgrades

        #Former City Stuff Start

        self.max_time = 20
        self.available_time = 20
        self.total_days = 1
        self.current_day = 1
        self.weeks = 1
        self.prefix = "city_"



        self.city_menu_choices = {'a':self.bar.menu,'x':main.main_menu,'h':self.hideout.menu,'o':self.home.menu,
        'm':self.market.menu,'c':self.market.menu,'b':self.bank.menu,'j':self.job.menu}
        #Former City Stuff End

    def intro(self):
        intro_texts = ("intro1","intro2","intro3","intro4","title","title2")
        for item in intro_texts:
            print(self.config.get_text(item))
            x=input("...")
        x=input("Enter the Game")


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

    def city_menu(self,skip=False,new_game=False):
        if new_game:
            self.character_maker(skip)
        if new_game and not skip:
            self.intro()
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
                run_menu = False
                if choice == 'c':
                    self.city_menu_choices[choice](self,market=False)
                elif choice == 'x':
                    self.city_menu_choices[choice]()
                else:
                    self.city_menu_choices[choice](self)
            else:
                print("That is not a valid option")


    def character_maker(self,skip):
    #first, the player
        if skip:
            self.character.first_name = "John"
            self.character.last_name = "Doe"
            self.character.nickname = "Johny"
            self.character.race = (2,"Fox")
            self.character.gender = (1,"male")
            self.character.so_first_name = "Jim"
            self.character.so_last_name = "Jacobs"
            self.character.so_nickname = "Jimmy"
            self.character.so_race = (2,"Fox")
            self.character.so_gender = (1,'male')
            self.character.cash_on_hand = 100000
            return None
        print()
        print("First we need to know a bit about you.")
        print()
        name = False
        while not name:
            print()
            firstname = input("What is your first name: ")
            lastname = input("What is your last name: ")
            nickname = input("What is your nickname: ")
            print("You have put as your name", firstname,"'"+nickname+"'",lastname)
            correct = input("If this is correct, enter 'y' to continue: ")
            if correct.lower() == 'y':
                name = True
                self.character.first_name = firstname
                self.character.last_name = lastname
                self.character.nickname = nickname
        
        race = False
        print()
        races = ((1,'Wolf'),(2,'Fox'),(3,'Otter'),(4,'Coyote'),(5,'Rabbit'),(6,'Tiger'),(7,'Ermine'),(8,'Squirrel'),)
        print("What race are you?")
        while not race:
            print()
            print("[1] Wolf | [2] Fox | [3] Otter | [4] Coyote")
            print("[5] Rabbit | [6] Tiger | [7] Ermine | [8] Squirrel")
            choice = input("Please put in the number of the race you want: ")
            if not choice in ["1","2","3","4","5","6","7","8"]:
                print("Please put in a valid entry")
                print()
            else:
                race_chosen = races[int(choice)-1]
                print("You are a",race_chosen[1])
                correct = input("Enter y to accept: ")
                if correct.lower() == 'y':
                    self.character.race = race_chosen
                    race = True
                else:
                    print("Trying again")
                    print()
                    
        gender = False
        genders = ((1,'male'),(2,'female'),)
        print()
        print("Dev note: Due to programming limitations, genders are binary at this point in time.")
        while not gender:
            print()
            print("Are you [1] Male or [2] Female?")
            choice = input("Please put in the number of the option you want: ")
            if not choice in ['1','2']:
                print("Please enter a valid option.")
            else:
                selection = genders[int(choice)-1]
                print("You have selected",selection[1].title())
                confirm = input("If correct, enter 'y': ")
                if confirm.lower() == 'y':
                    self.character.gender = selection
                    gender = True
                else:
                    print("Allright, retrying.")
            
                    
    #and now, the SO
        print()
        print("And now, about your significant other...")
        print()
        name = False
        while not name:
            print()
            firstname = input("What is your SO's first name: ")
            lastname = input("What is your SO's last name: ")
            nickname = input("What is your SO's nickname: ")
            print("You have put as your SO's name", firstname,"'"+nickname+"'",lastname)
            correct = input("If this is correct, enter 'y' to continue: ")
            if correct.lower() == 'y':
                name = True
                self.character.so_first_name = firstname
                self.character.so_last_name = lastname
                self.character.so_nickname = nickname
        
        print()
        race = False
        races = ((1,'Wolf'),(2,'Fox'),(3,'Otter'),(4,'Coyote'),(5,'Rabbit'),(6,'Tiger'),(7,'Ermine'),(8,'Squirrel'),)
        print("What race is your SO?")
        while not race:
            print()
            print("[1] Wolf | [2] Fox | [3] Otter | [4] Coyote")
            print("[5] Rabbit | [6] Tiger | [7] Ermine | [8] Squirrel")
            choice = input("Please put in the number of the race you want: ")
            if not choice in ["1","2","3","4","5","6","7","8"]:
                print("Please put in a valid entry")
                print()
            else:
                race_chosen = races[int(choice)-1]
                print("Your SO is a",race_chosen[1])
                correct = input("Enter y to accept: ")
                if correct.lower() == 'y':
                    self.character.so_race = race_chosen
                    race = True
                else:
                    print("Let's try again")
                    print()
        
        gender = False
        genders = ((1,'male'),(2,'female'),)
        print()
        print("Dev note: Due to programming limitations, genders are binary at this point in time.")
        while not gender:
            print()
            print("Is your SO [1] Male or [2] Female?")
            choice = input("Please put in the number of the option you want: ")
            if not choice in ['1','2']:
                print("Please enter a valid option.")
            else:
                selection = genders[int(choice)-1]
                print("Your so is",selection[1].title())
                confirm = input("If this is correct, enter 'y': ")
                if confirm.lower() == 'y':
                    self.character.so_gender = selection
                    gender = True
                else:
                    print("Allright, retrying.")
        