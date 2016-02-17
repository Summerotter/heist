class Home:
    def __init__(self,game):
        self.prefix = "home_"
        self.base_stamina_restoration = 1
        self.base_stress_restoration = 1
        self.bonus_stam = 0
        self.bonus_stress = 0
        self.upgrades = {'Example':{'upkeep':0,'type':'stam','value':0,},}
        
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to game.bank.expenses'''
        print("Adds an installed upgrade, will pay full weekly cost at end of week.")
        
    def remove_upgrade(self):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        print("Removes an installed upgrade. Will still need to pay weekly bill for it. Submenu")
        
    def end_night(self,game):
        '''ends the day. consumes all remaining hours, restores stamina and reduces stress via base rate per hour + modifiers. Can cause event that instead raises stress if Health threshhold is breached; the SO doesn't like seeing you hurt and will argue with you over the Heists'''
        hours = game.available_time
        if game.randint(1,100) >60 and game.character.stats['health']['penalty']:
            '''if I had a proper event system, this is where a spawn_event(home) would go!'''
            '''instead you just get a 40% chance of no stress healing and additional penalty if you're at or below Health threshold.'''
            stamina_regained = (self.bonus_stam + self.base_stamina_restoration) * hours
            game.character.stats['stamina']['current'] += stamina_regained
            stress_lost = game.randint(1,2)
            game.character.stats['stress']['current'] -= stress_lost 
            print("You had a fight with your SO over your escapades. They're worried you might not come back one day, but you know its the only way for a better life for you two. You've lost",stress_lost,"points worth of stress handling.")
            print("You did recover some stamina, up to",stamina_regained,"points worth.")
        else:
            stamina_regained = (self.bonus_stam + self.base_stamina_restoration) * hours
            stress_regained = (self.bonus_stress + self.base_stress_restoration) * hours
            game.character.stats['stress']['current'] += stress_regained
            game.character.stats['stamina']['current'] += stamina_regained
            print("Resting in your home for",hours,"hours gets you up to",stamina_regained,"stamina and",stress_regained,"stress hanlding back.")
            print("But not more than your max!")
        game.advance_day()
        game.character.nights_not_home = 0
        #kicks you back to game.hideout.menu()
        
    def print_menu(self):

        print()
        print(" 'A'dd Upgrade | 'U'ninstall Upgrade ")
        print(" 'R'est        |  'L'eave ")
        print()
        
    def win(self,game):
        win_text = ('win1','win2','win3','intro1','win4','win5','win6','title','title2')
        for each in win_text:
            print(game.config.get_text(each))
            x = input("...")
        x = input("Press Enter to End")
        
        
    def menu(self,game):
        menu = True
        if 'papers' in game.character.inventory:
            if game.character.inventory['papers'] >0:
                self.win()
                print("Thank you for playing!")
                menu = False
                game.main_menu()
        else:
            desc = game.config.get_text(self.prefix+game.time_of_day())
            print()
            print(desc)
        while menu:
            game.time_for_menu()
            self.print_menu()
            choice = input("Will you do?: ").lower()
            if choice == 'l':
                desc = ''
                print()
                print("You leave your game.home.")
                print()
                game.city_menu()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            elif choice == 'r':
                self.end_night(game)
            else:
                print("Not a valid option")