class Hideout:
    def __init__(self,game):
        self.prefix = "hide_"
        self.base_stamina_restoration = 1
        self.base_health_restoration = 1
        self.upgrades = {}
        self.health_modifier = 0
        self.stamina_modifier = 0
        self.level_up_options = { '1': ('health','stat'), '2': ('stamina','stat'), '3': ('stress','stat'), '4': ('shoot','skill'), '5': ('sneak','skill'), '6': ('mechanics','skill',), }
        self.menu_options = {'l':self.exit,'t':self.spend_xp_menu,'m':self.mirror,'p':game.director.menu,'r':self.end_night,'i':self.inventory,}
        
    
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to game.bank.expenses'''
        print("Adds an installed upgrade, will pay full weekly cost at end of week.")
        
    def remove_upgrade(self):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        print("Removes an installed upgrade. Will still need to pay weekly bill for it. Submenu")
        
    def spend_xp_menu(self,game):
        '''allows character to spend xp to increase skills and max stats by +1, cost is current level.'''
        print("Training your skills and stats!")
        run_menu = True
        while run_menu:
            self.print_menu_xp(game)
            option = str(input("Your decision: "))
            if option == 'x':
                run_menu = False
                print("Going back to the Hideout menu")
                print()
                self.menu(game)
            elif option in self.level_up_options:
                print("Running option",option)
                if self.level_up_options[option][1] == 'stat':
                    run_menu = game.character.raise_stat(self.level_up_options[option][0])
                elif self.level_up_options[option][1] == 'skill':
                    run_menu = game.character.raise_skill(self.level_up_options[option][0])
                else:
                    pass
            elif option == "cheat":
                game.character.add_xp(100)
                print("Cheater!")
                print()
            else:
                print("Not a valid option, that.")
            
        
    def print_menu_xp(self,game):
        '''called by spend_xp_menu to do the needful'''
        print()
        print("You have",game.character.available_xp,"xp you can spend.")
        print("Enter the number of the skill or stat you wish to train")
        print("1: Max Health",game.character.stats['health']['max'],":",str(game.character.stats['health']['level'])+"xp for +1  |  4: Shoot",str(game.character.skills['shoot']['skill']),":",str(game.character.skills['shoot']['skill'])+"xp for +1") 
        print("2: Max Stamina",game.character.stats['stamina']['max'],":",str(game.character.stats['stamina']['level'])+"xp for +1 |  5: Sneak",str(game.character.skills['sneak']['skill']),":",str(game.character.skills['sneak']['skill'])+"xp for +1") 
        print("3: Max Stress",game.character.stats['stress']['max'],":",str(game.character.stats['stress']['level'])+"xp for +1  |  6: Mechanics",str(game.character.skills['mechanics']['skill']),":",str(game.character.skills['mechanics']['skill'])+"xp for +1")
        print("or choose 'x' to exit")
        print()
        
        
    def end_night(self,game):
        '''ends the day. Consumes remaining hours. Restores health and stamina as per base, plus mods. Can cause event that raises stress for not being Home'''
        hours = game.available_time +4
        stamina_regained = (self.stamina_modifier + self.base_stamina_restoration) * hours
        health_regained = (self.health_modifier + self.base_health_restoration) * hours
        game.character.stats['health']['current'] += health_regained
        game.character.stats['stamina']['current'] += stamina_regained
        if game.character.nights_not_home > 1 and game.randint(1,100)+game.character.nights_not_home >80:
            '''if I had a proper event system, this is where a spawn_event(hideout) would go!'''
            '''instead you just get a 20% chance of more stress.'''
            stress_lost = game.randint(1,2)
            game.character.stats['stress']['current'] -= stress_lost
            print("You miss your SO, and the thoughts of being without them has decreased your stress handling by",stress_lost)
            
        print("Resting in the hideout for",hours,"hours gets you up to",stamina_regained,"stamina and",health_regained,"health back.")
        print("But not more than your max!")
        game.advance_day()
        game.character.nights_not_home += 1
        self.menu(game)
        
    def end_night_penalty(self,game):
        '''ends the day. Called by HeistDirector if the heist used up the next day's hours, too'''
        #there's 24 hours in a day. minimum of 4 for sleep, so normally just 20. But since there was no sleep, we'll count that 4.
        time_lost = game.available_time + 4
        if time_lost > 0:
            time_lost = 0
        #this checks if you were 4 or fewer hours in time-debt, and puts you to 0 instead of a negative. No gaining hours this way!      
        game.character.stats['stamina']['current'] -= 1
        game.character.stats['stress']['current'] += 1
        game.advance_day(penalty=time_lost)
        #calls advance_day function for game.city. Passes penalty along.
        print("Blurb about getting no sleep or arriving back mid-day with no rest.")
        game.character.nights_not_home += 1
        self.menu(game)
        #end_night doesn't need this since it was called from the menu already, but this is called from the HeistManager run_heist method.
        
    def print_menu(self):
        print()
        print(" You can look in the 'M'irror")
        print(" Your 'I'nventory is messy right now")
        print(" 'T'rain | 'P'lan Heist ")
#        print(" 'A'dd or 'U'ninstall Upgrade")
        print(" 'R'est  | 'L'eave Hideout")
        print()
        
    def mirror(self,game):
        game.character.mirror(game)
        self.menu(game)
        
    def inventory(self,game):
        game.character.print_inventory()
        self.menu(game)
        
    def exit(self,game):
        game.city_menu()
    
    
    def menu(self,game):
        desc = game.config.get_text(self.prefix+game.time_of_day())
        print()
        print(desc)
        run_menu = True
        while run_menu:
            game.time_for_menu()
            self.print_menu()
            choice = input("What will you do?: ").lower()
            print()
            if choice in self.menu_options:
                run_menu = False
                self.menu_options[choice](game)
            else:
                print("Not a valid option")