'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3

Written in Python3.4.2, Windows Environ
'''
from random import randint

class City:
    def __init__(self):
        self.max_time = 20
        self.available_time = 20
        self.total_days = 1
        self.current_day = 1
        self.weeks = 1
        self.description =['City Description 1','City Description 2','City Description 3',]
        
    def advance_day(self,penalty=0):
        '''called when ending a day at Hideout or Home, or by a Heist'''
        self.available_time = self.max_time - penalty
        self.total_days += 1
        job.can_work = True
        if self.current_day < 7:
            self.current_day += 1
        else:
            self.current_day = 1
            self.weeks += 1
            '''bank.deductions() here'''
            '''market.refresh() here'''
            
    def print_menu(self):
        print("There are",city.available_time,"hours left available today.")
        print("L for Load | S for Save")
        print("B for Bank | J for Job ")
        print("M for Market | C for Store")
        print("H for Hideout | O for Home")
        print("A for Bar | X for Exit")
        print()
            
    def menu(self):
        print()
        desc = self.description[randint(0,len(self.description)-1)]
        print(desc)
        print()
        while desc != '':
            self.print_menu()
            choice = input("Choose the option: ").lower()
            if choice == "x":
                print("Goodbye")
                desc = ''
                break
            elif choice == "s":
                print("Currently not here")
                #Does not have desc = ''. 
            elif choice == "l":
                print("No saves, no loads")
                #Does not have desc = ''.
            elif choice == 'b':
                desc = ''
                bank.menu()
            elif choice == 'j':
                desc = ''
                job.menu()
            elif choice == 'm':
                desc = ''
                market.menu()
            elif choice == 'c':
                desc = ''
                market.menu(market=False)
            elif choice == 'h':
                desc = ''
                hideout.menu()
            elif choice == 'o':
                desc = ''
                home.menu()
            elif choice == 'a':
                desc = ''
                bar.menu()
            else:
                print("That is not a valid option")
            
        
class Bank:
    def __init__(self):
        '''starts with 600 cash, and a $ symbol'''
        self.account = 600
        self.symbol = "$"
        self.expense_list = {'ble':600,}
        self.expense_sum = 600
        #expenses is a dict, can add more in or remove them. Basic Living Expenses is 600.
        self.description = ["This is the text description for the location. Perhaps make a list, rotate it between a few?",'Bank lol','Stilla bank',]
        self.fee = 15
        #The fee is for when you overdraft, and adds each time the deduction will result in a negative. Perhaps variable?
        self.transaction = False
        
    def update_expense_sums(self):
        #Called whenever an upgrade is installed, and end of week.
        self.expense_sum = 0
        for expense in self.expense_list:
            self.expense_sum += expense_list[expense]
        
        
    def deductions(self):
        #called by End of Week function by City object.
        self.account -= self.expense_sum
        if self.account < 100:
            character.stress += 1
            #if the bank account is too low, it will cause additional stress at the end of the week.
        if self.account < 0:
            self.account -= self.fee
            #Relatively reasonable overdraft fee as it applies at the total deduction, not per expense while in negative.
        self.update_expense_sums()
        #called to remove any now-invalid upgrades
            
    def deposit(self):
        '''reduces cash on hand, increases cash banked'''
        print("You approach the teller to make a deposit.")
        print("You have",self.symbol+str(character.cash_on_hand),"on you.")
        amt = input("'How much you putting in?' ")
        try:
            amt = int(amt)
        except:
            print("Back of the line, comeback with a sensible answer!")
            return None
        if character.cash_on_hand < amt:
            print("You don't have that much money, back of the line!")
        else:
            character.cash_on_hand -= amt
            self.account += amt
            self.transaction = True
            print("You deposited",self.symbol+str(amt),"in your account.")
        
        
    def withdraw(self):
        '''reduces cash on hand, increases cash banked'''
        print("You approach the teller to make a withdrawl.")
        print("You have",self.symbol+str(self.account),"in your account.")
        amt = input("'How much you taking out?' ")
        try:
            amt = int(amt)
        except:
            print("Back of the line, comeback with a sensible answer!")
            return None
            
        if self.account < amt:
            print("You don't have that much money, back of the line!")
        else:
            character.cash_on_hand += amt
            self.account -= amt
            self.transaction = True
            print("You withdrew",self.symbol+str(amt),"from your account.")
        
    def print_menu(self):
        print()
        print(" You have",self.symbol+str(self.account),"in your account, and",self.symbol+str(character.cash_on_hand),"on you.")
        print(" Your expenses are",self.symbol+str(self.expense_sum),"a week.")
        print(" Make a 'D'eposit | Make a 'W'ithdrawl")
        print(" Or you can 'L'eave. ")
        print()
            
    def menu(self):
        '''prints the menu. Options for withdrawl, deposit, viewing accounting sheet, and depart. On Exit, self.transaction set to False, and city.available_time -= 1 '''
        desc = self.description[randint(0,len(self.description)-1)]
        print()
        print(desc)
            
        while desc !='':
            if city.available_time == 0:
                print("The bank is closed, and it is time for you to go home.")
                desc = ''
                city.menu()
            self.print_menu()
            choice = input("Your option: ").lower()
            if choice == "l":
                print("You've left the bank.")
                desc = ''
                if self.transaction:
                    city.available_time -= 1
                city.menu()
            elif choice == 'd':
                self.deposit()
            elif choice == 'w':
                self.withdraw()
            else:
                print("That's not a valid option here.")
                print()
                
class Market:
    #single object for both Company Store and Black Market, since they're nearly the same thing.
    def __init__(self):
        self.store_description = ["This is the text description for the location. Perhaps make a list, rotate it between a few?",'store2','store3',]
        self.market_description = ["This is the text description for the location. Perhaps make a list, rotate it between a few?",'mar1','mar2',]
        self.store_stock = {'Medical Supplies': {'qty':1,'cost':5,},}
        self.market_stock = {'Medical Supplies': {'qty':1,'cost':8,'sale':3,},}
        #stock is the inventory dict that has items available, their price, and their quantity. Nested dicts. store_stock items do not change, market_stock does. Market has additional 'sale' cost as you can sell goods to it as a lower price.
        self.market_items = {}
        #full list of Black Market.
        self.store_keys = list(self.store_stock.keys())
        self.market_keys = list(self.market_items.keys())
        self.transaction = False
        
    def refresh(self):
        for item in self.store_stock:
            qty = randint(1,4)
            self.store_stock[item]['qty'] = qty
        #The Company Store's offerings never change.
        
        self.market_stock = {
        'Identity Papers':{'qty':1,'cost':100000,'sale':0,},
        'Loot':{'qty':0,'cost':100,'sale':25,},
        }
        #every week the Black Market offers new items, except Loot and Identity Papers are always available.
        store_options = randint(1,4) + len(self.market_stock)
        while len(self.market_stock) < store_options:
            item = self.store_keys[randint(0,len(self.store_keys)-1)]
            if not item in self.market_stock:
                qty = randint(1,3)
                cost = self.store_stock[item]['cost']
                market_cost = cost*1.5
                sale_cost = cost*.5
                self.market_stock[item] = {'qty':qty,'cost':cost,'sale':sale_cost}
        #Randomly gets 1-4 items from the Company Store list. Maybe 0-3?
        
        store_options = randint(1,4) + len(self.market_stock)
        while len(self.market_stock) < store_options:
            item = self.market_keys[randint(0,len(self.market_keys)-1)]
            if not item in self.market_stock:
                qty = randint(1,2)
                self.market_stock[item] = self.market_items[item]
                self.market_stock[item]['qty'] = qty
        #randomly selects 1-4 items from the Black Market list, adds 1-2 of them to the stock.
        
    def buy(self, stock, item):
        '''removes cash-on-hand from character, adds item to inventory and removes from stock'''
        self.transaction = True
            
    def sell(self, item, loot=False):
        '''gives character chas on hand, removes item from inventory, places in market stock. ONly for black market'''
        '''if loot=True from menu, it autounloads all loot in inventory in one go'''
        self.transaction = True
            

        
    def print_menu(self,market=True):
        print()
        if market:
            '''prints market specific menu'''
            print("This is the Black Market Menu!")
            print("Will be able to buy or sell things here!")
            print("Nothing to do here but e[x]it out to the city.")
        else:
            '''prints store specific menu'''
            print("This is the Company Store Menu!")
            print("Can buy stuff but out of stock")
            print("Nothing to do here yet but e[x]it out to the city.")
                
            '''on exit, if self.transaction == True, set to False, city.time_available -= 1'''
                
    def buy_menu(self,stock):
        '''lists all the stock options for purchasing'''
            
    def sell_menu(self,stock):
        '''lists inventory items and price earned from them.'''
        
    def menu(self,market=True):
        print()
        if market:
            desc = self.market_description[randint(0,len(self.market_description)-1)]
            stock = self.market_stock
        else:
            desc = self.store_description[randint(0,len(self.store_description)-1)]
            stock = self.store_stock
        print(desc)
        while desc != '':
            self.print_menu(market)
            choice = input("What's your option: ")
            if choice == 'x':
                desc = ''
                city.menu()
            elif choice == 's' and market:
                print("This is here just for code demo, sorry!")
                '''self.sell_menu(stock)'''
            elif choice == 'b':
                print("Just more code demo, sorry!")
                '''self.buy_menu(stock)'''
            else:
                print("Didn't recognize that option")
                
            
class Bar:
    def __init__(self):
        self.description = ["This is the text description for the location. Perhaps make a list, rotate it between a few?",'bar2','bar3',]
        
    def buy_booze(self):
        '''reduces cash on hand, reduces stress'''
        #city.time_available -= 1
        print("You buy some beer. It's beery refreshing.")
        
    def flirt(self):
        '''possible chance of ability to flirt with SO, reduces stress for free'''
        #city.time_available -= 1
        print("You flirt with your SO")
        
    def print_menu(self):
        print()
        print("This is a bar. Buy booze, or flirt with your SO who works here.")
        print("[B]uy Booze for $ | [F]lirt with your SO")
        print("Or e[x]it to the city.")
        print()
        
    def menu(self):
        desc = self.description[randint(0,len(self.description)-1)]
        print()
        print(desc)
        while desc != '':
            self.print_menu()
            choice = input("What'll it be? ").lower()
            if choice == 'x':
                desc = ''
                print()
                print("Well, seeya!")
                print()
                city.menu()
            elif choice == 'f':
                self.flirt()
            elif choice == 'b':
                self.buy_booze()
            else:
                print("Not a valid option")
        
class Job:
    def __init__(self):
        self.description = ["Your workplace",'Shop as busy as ever','This tedious place again']
        self.base_pay = 9.00
        self.can_work = True
    
    def work(self):
        '''formula for work is 9.00 + character.skill[mechanics]. At Mechanics 1 rate is 10.00/hour, Mechanics 2 is 11.00/hour, 5 is 14 etc.'''
        '''10 hours work max, but will auto-consume all availble hours if less. Final pay will be told after Event, and autodeposits in Bank.'''
        '''Work Event adds Stress and reduces Stamina'''
        if city.available_time >= 10:
            hours = 10
            city.available_time -= 10
        else:
            hours = city.available_time
            city.available_time = 0
        money_earned = (self.base_pay + character.mechanics) * hours
        bank.account += money_earned
        self.can_work = False
        print("After",hours,"of hard labor in hte mechanic shop, with a Mechanics Skill of ",character.mechanics,"you have earned",bank.symbol+str(money_earned)+"!")
        print("It gets automatically deposited into your bank account.")
        print("Also you prettymuch get kicked out of the shop when your shift is over")
        print()
        
    def print_menu(self):
        print()
        print("You can [W]ork, or you can ['L']eave.")
        print()
        
    def menu(self):
        desc = self.description[randint(0,len(self.description)-1)]
        print()
        print(desc)
        while desc != '':
            if city.available_time == 0:
                desc = ''
                print("The shop is shut down for the day. You need to go home.")
                city.menu()
            elif not self.can_work:
                desc = ''
                print("The shop might still be open, but you can't work any more hours. No overtime allowed!")
                city.menu()
            else:
                self.print_menu()
                choice = input("Will you do?: ").lower()
                if choice == 'l':
                    desc = ''
                    print()
                    print("You leave your workplace.")
                    print()
                    city.menu()
                elif choice == 'w':
                    desc = ''
                    self.work()
                    city.menu()
                else:
                    print("Not a valid option")
        
class Home:
    def __init__(self):
        self.descritpion = ["This is your home", 'This is the castle', 'This is where you and your so live',]
        self.base_stamina_restoration = 1
        self.base_stress_reduction = 1
        self.bonus_stam = 0
        self.bonus_stress = 0
        self.upgrades = {'Example':{'upkeep':0,'type':'stam','value':0,},}
        
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to bank.expenses'''
        print("Adds an installed upgrade, will pay full weekly cost at end of week.")
        
    def remove_upgrade(self):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        print("Removes an installed upgrade. Will still need to pay weekly bill for it. Submenu")
        
    def end_night(self):
        '''ends the day. consumes all remaining hours, restores stamina and reduces stress via base rate per hour + modifiers. Can cause event that instead raises stress if Health threshhold is breached; the SO doesn't like seeing you hurt and will argue with you over the Heists'''
        print("This would end the day and have you sleep in your bed with your SO, restoring stamina and stress")
        
    def print_menu(self):
        print()
        print(" 'A'dd Upgrade | 'U'ninstall Upgrade ")
        print(" 'R'est        |  'L'eave ")
        print()
        
        
    def menu(self):
        desc = self.description[randint(0,len(self.description)-1)]
        print()
        print(desc)
        while desc != '':
            self.print_menu()
            choice = input("Will you do?: ").lower()
            if choice == 'l':
                desc = ''
                print()
                print("You leave your home.")
                print()
                city.menu()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            elif choice == 'r':
                self.end_night()
            else:
                print("Not a valid option")
        
class Hideout:
    def __init__(self):
        self.description = ['hideout_1','hideout_2']
        self.base_stamina_restoration = 1
        self.base_health_restoration = 1
        self.upgrades = {}
        self.health_modifier = 0
        self.stamina_modifier = 0
    
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to bank.expenses'''
        print("Adds an installed upgrade, will pay full weekly cost at end of week.")
        
    def remove_upgrade(self):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        print("Removes an installed upgrade. Will still need to pay weekly bill for it. Submenu")
        
    def spend_xp(self,character):
        '''allows character to spend xp to increase skills and stats by +1, cost is current level.'''
        print("This would allow you to spend XP. Perhaps another menu and system?")
        
    def end_night(self, character):
        '''ends the day. Consumes remaining hours. Restores health and stamina as per base, plus mods. Can cause event that raises stress for not being Home'''
        print("Normally, this ends the day, but the mechanic isn't here yet. Would gain health and stamina.")
        
    def heist(self, character):
        '''goes on a heist. May list multiple options with differing difficulty and reward levels. Seperate module'''
        '''requires certain threshold of health AND stamina to attempt'''
        print("Starts the Heist Menu. Not implimented at all currently.")
        
    def print_menu(self):
        print()
        print(" 'T'rain | 'P'lan Heist ")
        print(" 'A'dd or 'U'ninstall Upgrade")
        print(" 'R'est  | 'L'eave Hideout")
        print()
        
    def menu(self):
        desc = self.description[randint(0,len(self.description)-1)]
        print()
        print(desc)
        while desc != '':
            self.print_menu()
            choice = input("Will you do?: ").lower()
            if choice == 'l':
                desc = ''
                print()
                print("Well, seeya!")
                print()
                city.menu()
            elif choice == 't':
                self.spend_xp()
            elif choice == 'p':
                self.heist()
            elif choice == 'r':
                self.end_night()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            else:
                print("Not a valid option")
        
class Character:
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.nickname = "Johnny"
        self.desc = "description"
        self.so_first_name = "Jane"
        self.so_last_name = "Fawn"
        self.so_nickname = "Fawny"
        self.so_desc = "so desc"
        #names and desc. Awww!
        
        
        self.health = 10
        self.stamina = 10
        self.stress = 0
        self.stress_threshhold = 5
        self.shoot = 1
        self.sneak = 1
        self.mechanics = 1
        #stats and skills
        
        self.cash_on_hand = 0
        self.total_xp = 0
        self.available_xp = 0
        #xp and cash, obv. total xp is all XP ever owned, available xp is what can be spent
        
        self.inventory = {}
        self.tools = {'Simple Tools':0}
        self.gun = {'Basic Pistol':0}
        self.clothing = {'Normal Clothing':0}
        #inventory is all the items non-equipped that the character owns.
        #tools, gun, and clothing are equipment that gives a bonus to mechanics, shoot, and sneak respectively.
        
##Still need to flesh out Heists. Difficulty of 0-4, "Simple, Easy, Tough, Challenging, Impossible". 25/50/75/100/200 cash-of-loot per stage. 
##Lower difficult weighted towards 3 stages, higher towards 5. 
##Events will have 4 options, versus Shoot, Sneak, Mechanics, and Stamina. Some options may have a requirement threshhold. Each Event should have at least one attemptable option.
##Character Test is 1d10 + Skill - Stress_Penalty - Wounded_Penalty - Exhaustion_Penalty, versus Option Difficulty + 1d5 + Heist_Difficulty_Modifier[0-4]
##Success is 1XP, plus Reward_Roll of 1d10+Option Difficulty of an Item or Loot[generate cachet list?], value modified by Heist Difficulty.
##Failure is a -1 Health and/or -1 Stamina and/or +1 Stress and/or losing Loot gained thus far on the Heist.
##End of Heist is +1XP and tally's up total.
##Heists use up 15 hours flat. If character has 15 or few hours left it automatically ends the day with no rest. If this ends up being a large deficiet, hours available the next day will go down.
        
'''
class HeistDirector:
    def __init__(self):
        self.heist_types = ['Factory','Office','Warehouse','Airship Docks',]
        self.heist_scenes = {
        'Factory':(('blurb','gunoption','sneakoption','mechanicoption','staminaoption',),),
        'Office':(),
        'Warehouse':(),
        'Airship Docks':(),
        }
        ##These nested lists of Scene Text and appropriate Test Text.
        
        self.heist_blurbs = {
        'Factory':(),
        'Office':(),
        'Warehouse':(),
        'Airship Docks':(),
        }
        self.heist_names = {
        'Factory':(),
        'Office':(),
        'Warehouse':(),
        'Airship Docks':(),
        }
        ##Names and Blurbs, randomly chosen by type
        
        self.difficulty = {
            0: 'Simple',
            1: 'Easy',
            2: 'Tough',
            3: 'Difficult',
            4: 'Challenging',
        }
## Sets the names of the difficulty numbers.
        self.heist_options = []
        ## for keeping track of options until generated again.
        
        self.xp_earned = 0
        self.loot = 0
    
    def generate_heist_options(self):
        self.heist_options = []
        for each in range(3):
            type = self.heist_types[randint(0,3)]
            #gets type. Needs to be updated if more types added.
            name = self.heist_names[type][randint(0,len(self.heist_names[type])-1)]
            blurb = self.heist_blurbs[type][randint(0,len(self.heist_blurbs[type])-1)]
            difficulty = randint(0,4)
            ##Needs weighting based on XP
            self.heist_options.append((type,name,blurb,difficulty,))
            
    def generate_heist(self,heist):
        type = heist[0]
        name = heist[1]
        blurb = heist[2]
        difficulty = heist[3]
        event_count = randint(3-5)
        event_numbers = []
        while event_numbers < event_count:
            number = randint(0,len(self.heist_scenes[type])-1)
            if number not in event_numbers:
                event_numbers.append(number)
        #needs weighting of some sort for difficulty
        print(name+": "+blurb)
        for event in event_numbers:
            success = False
            scene = self.heist_scenes[type][event]
            blurb = scene[0]
            gunopt = (scene[1], randint(1,3) * 1 + difficulty)
            sneakopt = (scene[2], randint(1,3) * 1 + difficulty)
            mechopt = (scene[3], randint(1,3) * 1 + difficulty)
            stamopt = (scene[4], randint(1,3) * 1 + difficulty)
            
            Assuming gunopt for now 
            choice = input("Option: ")
            if choice == "1":
                charroll = character.shoot - character.stress_penalty - character.health_penalty - character.stamina_penalty + randint(1,10)
                testroll = gunopt[1] + randint(1,5)
                if charroll >= testroll:
                    success = True
                    self.xp_earned += 1
                    self.loot = randint(1+difficulty,3+difficulty)
                    '''
city = City()
bank = Bank()
market = Market()
bar = Bar()
job = Job()
home = Home()
hideout = Hideout()
character = Character()
                    
if __name__ == '__main__':
    city.menu()