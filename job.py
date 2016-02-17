class Job:
    def __init__(self,game):
        self.prefix = "job_"
        self.base_pay = 10.00
        self.can_work = True
        self.event_string = ''
        self.hours = 0
        self.earned = 0
        self.modified_pay = 0
        self.modified_hours = 0
        self.base_per_hour_stat_cost = {'stamina':1, 'stress': 0, 'health':0,}
        self.modified_per_hour_stat_cost = self.base_per_hour_stat_cost
        self.total_stat_cost = {'stamina':0, 'stress': 0, 'health':0,}
        
    def reset_modified(self):
        self.modified_pay = 0
        self.modified_hours = 0
        self.modified_per_hour_stat_cost = self.base_per_hour_stat_cost
        self.total_stat_cost = {'stamina':0, 'stress': 0, 'health':0,}
    
    def work(self,game):
        '''formula for work is 9.00 + game.character.skill[mechanics]. At Mechanics 1 rate is 10.00/hour, Mechanics 2 is 11.00/hour, 5 is 14 etc.'''
        '''10 hours work max, but will auto-consume all availble hours if less. Final pay will be told after Event, and autodeposits in game.bank.'''
        '''Work Event adds Stress and reduces Stamina'''
        self.reset_modified()
        game.available_time -= self.hours
        self.modified_pay = self.base_pay + game.character.skills['mechanics']['mod']
        self.modified_hours = self.hours
        
        game.event_manager.job_event(game)
        '''job events can cause unpaid hours, extra pay hours, bonus or penalty to wages, or a skill or stat boost'''
        self.earned = self.modified_pay * self.modified_hours
        
        for stat in self.modified_per_hour_stat_cost:
            self.total_stat_cost[stat] = self.modified_hours * self.modified_per_hour_stat_cost[stat]
            game.character.stats[stat]['current'] -= self.total_stat_cost[stat]
        game.bank.account += self.earned
        game.character.add_xp(1)
        self.can_work = False
        
        if self.event_string != '':
            print(self.event_string)
        print("After",self.hours,"of hard labor in the mechanic shop, with a total Mechanics Skill of ",game.character.skills['mechanics']['mod'],"you have earned",game.config.symbol+str(self.earned)+"!")
        
        print("It gets automatically deposited into your bank account.")
        print("Work also took out of you",self.total_stat_cost['stamina'],"points of stamina",self.total_stat_cost['stress'],"stress control",self.total_stat_cost['health'],"health.")
        print("Also you pretty much get kicked out of the shop when your shift is over")
        x = input("Press Enter to Continue")
        print()
        
    
        
    def print_menu(self,game):
        
        game.time_for_menu()
        print()
        print("You can [W]ork for",self.hours,"hours, or you can ['L']eave.")
        print()
        
    def can_work_check(self,game):
        if game.available_time <= 0:
            print("The shop is shut down for the day. You need to go game.home.")
            return False
        elif not self.can_work:
            print("The shop might still be open, but you can't work any more hours. No overtime allowed!")
            return False
        else:
            return True
        
    def menu(self,game):
        desc = game.config.get_text(self.prefix+game.time_of_day())
        if game.available_time >= 10:
            self.hours = 10
        else:
            self.hours = game.available_time
        print()
        print(desc)
        run_menu = self.can_work_check(game)
        while run_menu:
            self.print_menu(game)
            choice = input("Will you do?: ").lower()
            print()
            if choice == 'l':
                print("You leave your workplace.")
                run_menu = False
            elif choice == 'w':
                run_menu = False
                self.work(game)
            else:
                print("Not a valid option")
        if not run_menu:
            game.city_menu()