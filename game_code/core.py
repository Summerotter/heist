'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3

Written in Python3.4.2, Windows Environ
'''

class Game:
    '''NOT IMPLIMENTED'''
    def __init__(self,config,main):
        self.config = config
        self.loaded = False

        '''grab the save file master info here'''
        '''key = name, date last played, in-game date, earned xp, total wealth, filename'''
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

        self.director = Director(self)
        self.bank = Bank(self)
        self.market = Market(self)
        self.bar = Bar(self)
        self.home = Home(self)
        self.hideout = Hideout(self)
        self.character = Character(self)
        self.event_manager = EventManager(self)
        self.job = Job(self)

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

    def city_menu(self,new_game=False):
        if new_game:
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


