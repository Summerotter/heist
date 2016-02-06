'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3


'''
from random import randint

class City:
    def __init__(self):
        self.max_time = 20
        self.available_time = 20
        self.total_days = 1
        self.current_day = 1
        self.weeks = 1
        
    def advance_day(self,penalty=0):
        '''called when ending a day at Hideout or Home, or by a Heist'''
        self.available_time = self.max_time - penalty
        self.total_days += 1
        if self.current_day < 7:
            self.current_day += 1
        else:
            self.current_day = 1
            self.weeks += 1
            '''bank.deductions() here'''
            '''market.refresh() here'''
            
    def menu(self,character):
        '''prints the menu, changes character.locatoin'''
        
class Bank:
    def __init__(self):
        '''starts with 600 cash, and a $ symbol'''
        self.account = 600
        self.symbol = "$"
        self.expenses = {'ble':600,}
        #expenses is a dict, can add more in or remove them. Basic Living Expenses is 600.
        self.description = "This is the text description for the location. Perhaps make a list, rotate it between a few?"
        self.fee = 15
        #The fee is for when you overdraft, and adds each time the deduction will result in a negative. Perhaps variable?
        self.transaction = False
        
    def deductions(self,character):
        for expense in self.expenses:
            self.account -= self.expenses[expense]
        if self.account < 100:
            character.stress += 1
            #if the bank account is too low, it will cause additional stress at the end of the week.
        if self.account < 0:
            self.account -= self.fee
            #Relatively reasonable overdraft fee as it applies at the total deduction, not per expense while in negative.
        '''and then recalcs expenses based on hideout and home upgrades being removed'''
            
    def deposit(self,character):
        '''reduces cash on hand, increases cash banked'''
        self.transaction = True
        
    def withdraw(self,character):
        '''reverse of above'''
        self.transaction = True
            
    def menu(self,character):
        #prints the menu. Options for withdrawl, deposit, viewing accounting sheet, and depart. On Exit, self.transaction set to False, and city.available_time -= 1
        
class Market:
    #single object for both Company Store and Black Market, since they're nearly the same thing.
    def __init__(self):
        self.store_description = "This is the text description for the location. Perhaps make a list, rotate it between a few?"
        self.market_description = "This is the text description for the location. Perhaps make a list, rotate it between a few?"
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
        
        def buy(self, character, stock, item):
            '''removes cash-on-hand from character, adds item to inventory and removes from stock'''
            self.transaction = True
            
        def sell(self, character, item, loot=False):
            '''gives character chas on hand, removes item from inventory, places in market stock. ONly for black market'''
            '''if loot=True from menu, it autounloads all loot in inventory in one go'''
            self.transaction = True
        
        def menu(self,market=True,character):
            if market:
                '''prints market specific menu'''
            else:
                '''prints store specific menu'''
                
            '''on exit, if self.transaction == True, set to False, city.time_available -= 1'''
                
        def buy_menu(self,stock):
            '''lists all the stock options for purchasing'''
            
        def sell_menu(self,character,stock):
            '''lists inventory items and price earned from them.'''
            
class Bar:
    def __init__(self):
        description = "This is the text description for the location. Perhaps make a list, rotate it between a few?"
        
    def buy_booze(self, character):
        '''reduces cash on hand, reduces stress'''
        city.time_available -= 1
        
    def flirt(self, character):
        '''possible chance of ability to flirt with SO, reduces stress for free'''
        city.time_available -= 1
        
    def menu(self):
        '''prints description, lists options and exit.'''
        '''no transaction needed here'''
        
class Job:
    def __init__(self):
        description = "STUFF"
        base_pay = 9.00
    
    def work(self, character,bank):
        '''formula for work is 9.00 + character.skill[mechanics]. At Mechanics 1 rate is 10.00/hour, Mechanics 2 is 11.00/hour, 5 is 14 etc.'''
        '''10 hours work max, but will auto-consume all availble hours if less. Final pay will be told after Event, and autodeposits in Bank.'''
        '''Work Event adds Stress and reduces Stamina'''
        
    def menu(self):
        '''self explanatory.'''
        
class Home:
    def __init__(self):
        self.descritpion = "Stuff"
        self.base_stamina_restoration = 1
        self.base_stress_reduction = 1
        self.bonus_stam = 0
        self.bonus_stress = 0
        self.upgrades = {'Example':{'upkeep':0,'type':'stam','value':0,},}
        
    def add_upgrade(self, character,bank):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to bank.expenses'''
        
    def remove_upgrade(self, character, bank):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        
    def end_night(self, character):
        '''ends the day. consumes all remaining hours, restores stamina and reduces stress via base rate per hour + modifiers. Can cause event that instead raises stress if Health threshhold is breached; the SO doesn't like seeing you hurt and will argue with you over the Heists'''
        
    def menu(self):
        '''self explanatory'''
        
class Hideout:
    def __init__(self):
        self.description = 'stuff'
        self.base_stamina_restoration = 1
        self.base_health_restoration = 1
    
    '''same stuff for Home class for upgrades'''
        
    def spend_xp(self,character):
        '''allows character to spend xp to increase skills and stats by +1, cost is current level.'''
        
    def end_night(self, character):
        '''ends the day. Consumes remaining hours. Restores health and stamina as per base, plus mods. Can cause event that raises stress for not being Home'''
        
    def heist(self, character):
        '''goes on a heist. May list multiple options with differing difficulty and reward levels. Seperate module'''
        '''requires certain threshold of health AND stamina to attempt'''
        
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
        self.clothing = ('Normal Clothing':0}
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
            '''
            '''... print menu, menu while, yada yada '''
            ''' Assuming gunopt for now '''
            '''
            choice = input("Option: ")
            if choice == "1":
                charroll = character.shoot - character.stress_penalty - character.health_penalty - character.stamina_penalty + randint(1,10)
                testroll = gunopt[1] + randint(1,5)
                if charroll >= testroll:
                    success = True
                    self.xp_earned += 1
                    self.loot = randint(1+difficulty,3+difficulty)
                    '''