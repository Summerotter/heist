'''The Heist Game
Written by Henry Thiel/Bengaley Summercat
Started 2/5/2016
For Schmozy. :3

Written in Python3.4.2, Windows Environ
'''
from random import randint

def pause_x():
    print()
    x = input("Press Enter to continue...")
    print()

def intro():
    intro_texts = ("intro1","intro2","intro3","intro4","title","title2")
    for item in intro_texts:
        print(config.get_text(item))
        x=input("...")
    x=input("Enter the Game")
    
class City:
    def __init__(self,game):
        self.max_time = 20
        self.available_time = 20
        self.total_days = 1
        self.current_day = 1
        self.weeks = 1
        self.prefix = "city_"
        
        
    def advance_day(self,penalty=0):
        '''called when ending a day at Hideout or Home, or by a Heist'''
        self.available_time = self.max_time + penalty
        self.total_days += 1
        game.job.can_work = True
        game.character.update_everything()
        if self.current_day < 7:
            self.current_day += 1
        else:
            self.current_day = 1
            self.weeks += 1
            game.bank.deductions()
            '''game.market.refresh() here'''
            
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
            
    def print_menu(self):
        game.city.time_for_menu()
        print("B for Bank | J for Job ")
        print("M for Market | C for Store")
        print("H for Hideout | O for Home")
        print("A for Bar | X for Main Menu")
        print()
            
    def menu(self):
        print()
        desc = config.get_text(self.prefix+game.city.time_of_day())
        #results in city_morning, from prefix "city_" and time_of_day "morning"
        print(desc)
        print()
        while desc != '':
            self.print_menu()
            choice = input("Choose the option: ").lower()
            if choice == "x":
                desc = ''
                game.main_menu()
            elif choice == "s":
                print("Currently not here")
                #Does not have desc = ''. 
            elif choice == "l":
                print("No saves, no loads")
                #Does not have desc = ''.
            elif choice == 'b':
                desc = ''
                game.bank.menu()
            elif choice == 'j':
                desc = ''
                game.job.menu()
            elif choice == 'm':
                desc = ''
                game.market.menu()
            elif choice == 'c':
                desc = ''
                game.market.menu(market=False)
            elif choice == 'h':
                desc = ''
                game.hideout.menu()
            elif choice == 'o':
                desc = ''
                game.home.menu()
            elif choice == 'a':
                desc = ''
                game.bar.menu()
            else:
                print("That is not a valid option")
            
        
class Bank:
    def __init__(self,game):
        '''starts with 600 cash, and a $ symbol'''
        self.prefix = "bank_"
        self.account = 600
        self.symbol = "$"
        self.expense_list = {'ble':600,}
        self.expense_sum = 600
        #expenses is a dict, can add more in or remove them. Basic Living Expenses is 600.
        self.fee = 15
        #The fee is for when you overdraft, and adds each time the deduction will result in a negative. Perhaps variable?
        self.transaction = False
        
    def update_expense_sums(self):
        #Called whenever an upgrade is installed, and end of week.
        old_expense = self.expense_sum
        self.expense_sum = 0
        for expense in self.expense_list:
            self.expense_sum += self.expense_list[expense]
        if old_expense != self.expense_sum:
            print("Your weekly bills haven changed, and are now ",self.symbol+str(self.expense_sum),"a week.")
        else:
            print("Your weekly bills have not changed, and remain ",self.symbol+str(self.expense_sum),"a week.")
        
        
    def deductions(self):
        #called by End of Week function by City object.
        self.account -= self.expense_sum
        print("At the end of the 7th day, your account has been debited",self.symbol+str(self.expense_sum)," automatically. Your account now has",self.symbol+str(self.account),"in it.")
        if self.account < 100:
            game.character.stats['stress']['current'] -= 1
            print("Because your account is so low, you are stressing out about money, and lost some of your stress handling.")
            #if the bank account is too low, it will cause additional stress at the end of the week.
        if self.account < 0:
            self.account -= self.fee
            #Relatively reasonable overdraft fee as it applies at the total deduction, not per expense while in negative.
            print("Because you went into the negative, you also got a",self.symbol+str(self.fee),"fee for overdrafting.")
        self.update_expense_sums()
        x = input("Press Enter to Continue")
        #called to remove any now-invalid upgrades
            
    def deposit(self):
        '''reduces cash on hand, increases cash banked'''
        print("You approach the teller to make a deposit.")
        print("You have",self.symbol+str(game.character.cash_on_hand),"on you.")
        amt = input("'How much you putting in?' ")
        try:
            amt = int(amt)
        except:
            print("Back of the line, comeback with a sensible answer!")
            return None
        if game.character.cash_on_hand < amt:
            print("You don't have that much money, back of the line!")
        else:
            game.character.cash_on_hand -= amt
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
            game.character.cash_on_hand += amt
            self.account -= amt
            self.transaction = True
            print("You withdrew",self.symbol+str(amt),"from your account.")
        
    def print_menu(self):
        
        game.city.time_for_menu()
        print()
        print(" You have",self.symbol+str(self.account),"in your account, and",self.symbol+str(game.character.cash_on_hand),"on you.")
        print(" Your expenses are",self.symbol+str(self.expense_sum),"a week.")
        print(" Make a 'D'eposit | Make a 'W'ithdrawl")
        print(" Or you can 'L'eave. ")
        print()
            
    def menu(self):
        '''prints the menu. Options for withdrawl, deposit, viewing accounting sheet, and depart. On Exit, self.transaction set to False, and game.city.available_time -= 1 '''
        desc = config.get_text(self.prefix+game.city.time_of_day())
        print()
        print(desc)
            
        while desc !='':
            if game.city.available_time == 0:
                print("The bank is closed, and it is time for you to go game.home.")
                desc = ''
                game.city.menu()
            self.print_menu()
            choice = input("Your option: ").lower()
            if choice == "l":
                print("You've left the game.bank.")
                desc = ''
                if self.transaction:
                    game.city.available_time -= 1
                game.city.menu()
            elif choice == 'd':
                self.deposit()
            elif choice == 'w':
                self.withdraw()
            else:
                print("That's not a valid option here.")
                print()
                
class Market:
    #single object for both Company Store and Black Market, since they're nearly the same thing.
    def __init__(self,game):
        '''imports white and black from items.py for internal item list
        actual stock in store_stock and market_stock
        initialized as empty dicts, refresh method fixes that.
        '''
        import items
        self.store_items = items.white
        self.market_items = items.black
        self.store_prefix = "store_"
        self.market_prefix = "market_"
        self.market_stock = {'keys':{}}
        self.store_stock = {'keys':{}}
        self.store_keys = list(self.store_items.keys())
        self.market_keys = list(self.market_items.keys())
        self.market_price_mod = config.market_cost
        self.market_sale_mod = config.market_sale
        self.transaction = False
        
        self.refresh()
        
    def refresh(self):
        '''loads up a new week's worth of stock for both markets.'''
        
        #Company Store
        self.store_stock = {'keys':{}}
        #clearing out old data
        
        for item in self.store_keys:
            qty = randint(-1,3)
            if self.store_items[item]['qty']+qty > 0:
                self.store_stock[item] = self.store_items[item]
                self.store_stock[item]['qty'] = qty
                self.store_stock['keys'][len(self.store_stock['keys'] ) +1] = item
        #The Company Store always carries same good, but might be out, no need to list them.
        #Keys value is tupple menu_option,item_key. 

        #Black Market
        self.market_stock = {
        'papers':{'qty':1,'cost':100000,'value':1,'sale':0,'key':'papers',},
        'keys':{},
        }
        #Black market also resets, but keeps 'papers', win condition item, and 'loot', special sale item.
        self.blackmarket_refresh(self.store_keys,self.store_items)
        self.blackmarket_refresh(self.market_keys,self.market_items,store=False)
        self.market_stock['keys'][len( self.market_stock['keys'] ) +1] = 'papers'
        
    def blackmarket_refresh(self,keys,items,store=True):
        '''handles adding items for the black market, called twice'''
        if store:
            qty = (1,2)
            count = (2,3)
            price_mod = self.market_price_mod
        else:
            qty = (0,1)
            count = (3,4) 
            price_mod = 1
        for item in range(randint(count[0],count[1])):
            item_key = keys[randint(0,len(keys)-1)]
            if items[item_key]['value'] > 0:
                if not item_key in self.market_stock:
                    self.market_stock['keys'][len( self.market_stock['keys'] ) +1] = item_key
                    self.market_stock[item_key] = items[item_key]
                    self.market_stock[item_key]['qty'] += randint(qty[0],qty[1])
                    self.market_stock[item_key]['cost'] = round(price_mod * self.market_stock[item_key]['cost'])
                else:
                    self.market_stock[item_key]['qty'] += 1
                    #if it rolls the same item twice, gets an extra
                    
   
                    
    def remove_item(self,stock,item):
        '''checks if its market or store by loking for papers
        then reduces the qty by 1
        '''
        if 'papers' in stock:
            self.market_stock[item]['qty'] -= 1
        else:
            self.store_stock[item]['qty'] -= 1
        
    def buy(self, stock, item):
        '''removes cash-on-hand from character, adds item to inventory and removes from stock'''
        print("Item: ", item)
        if stock[item]['qty'] < 1:
            print("They're out of this item.")
        elif game.character.cash_on_hand >= stock[item]['cost']:
            print("This item costs $"+str(stock[item]['cost'])+", and you have $"+str(game.character.cash_on_hand))
            choice = input("Enter 'y' to confirm purchase: ").lower()
            if choice == 'y':
                game.character.add_item(item,stock[item])
                game.character.cash_on_hand -= stock[item]['cost']
                if 'papers' in stock:
                    print(self.market_stock[item]['qty'])
                    self.market_stock[item]['qty'] -= 1
                    print(self.market_stock[item]['qty'])
                else:
                    self.store_stock[item]['qty'] -= 1
                    
                self.transaction = True
            else:
                print("You can come back later.")
        else:
            print("You stare longingly at the "+stock[item]['key']+", but you can't afford it right now.")
            x = input("Hit Enter to Continue")

            
    def sell(self, item):
        '''gives character chas on hand, removes item from inventory, places in market stock. ONly for black market'''
        self.transaction = True
        print(item)
        if item[0] == 'loot':
            game.character.inventory['loot'] = 0
            game.character.cash_on_hand += item[1]*item[2]
            print("You just sold",item[1],"pieces of loot for $"+str(item[1]*item[2])+"!")
            print()
            x = input("Enter to continue.")
            print()
        else:
            game.character.remove_item(item[0])
            game.character.cash_on_hand += item[2]
            print("You just sold a",item[0],"for $"+str(item[2])+"!")
            print()
            x = input("Enter to continue.")
            print()

        
    def print_menu(self,market=True):
        '''on exit, if self.transaction == True, set to False, game.city.time_available -= 1'''
        game.city.time_for_menu()
        print()
        if market:
            '''prints market specific menu'''
            print("This is the Black Market Menu!")
            print("You can see what you can [b]uy, and what you can [s]ell.")
        else:
            '''prints store specific menu'''
            print("This is the Company Store Menu!")
            print("You can check out what goods we have to [b]uy.")
        print("Or e[x]it out to the game.city.")
            
                
    def buy_menu(self,stock):
        run_menu = True
        while run_menu:
            self.print_buy_menu(stock)
            
            choice = input("What are ya buying? ")
            if config.is_int(choice):
                choice = int(choice)
            if str(choice).lower() == "x":
                run_menu = False
            elif choice in stock['keys']:
                self.buy(stock,stock['keys'][choice])
            else:
                print("didn't catch that.")
        '''lists all the stock options for purchasing'''
        
    def print_buy_menu(self,stock):
        for i in range(1,len(stock['keys'])+1):
            if i in stock['keys']:
                item = stock[stock['keys'][i]]
                print(str(i)+":",item['key']+":"+str(item['value']), "Cost: $"+str(item['cost'])," ",item['qty'],"available."  )
        print("Or 'x' to back out of this menu")
            
    def sell_menu(self):
        items = {}
        for item in game.character.inventory:
            if item in self.market_items and game.character.inventory[item] > 0: 
                items[len(items)+1]= (item,game.character.inventory[item],self.market_items[item]['sell'])
            elif item in self.store_items and game.character.inventory[item] > 0:
                items[len(items)+1]= (item,game.character.inventory[item],self.store_items[item]['sell'])
            elif item == 'loot' and game.character.inventory['loot'] > 0:
                items[len(items)+1]= (item,game.character.inventory[item],game.character.loot_value)
        run_menu = True
        while run_menu:
            if len(items) == 0:
                print("You don't have anything for sale!")
                run_menu = False
            self.print_sell_menu(items)
            choice = input("What is your choice: ").lower()
            if config.is_int(choice):
                choice = int(choice)
            if choice == 'x':
                run_menu = False
            elif choice in items:
                run_menu = False
                self.sell(items[choice])
            else:
                print("Did not get a valid option")
                
                
    def print_sell_menu(self,items):
        
        print()
        for i in range(len(items)+1):
            if i in items:
                print(i, "Item: ",items[i][0], "Qty: ",items[i][1], "Sale Price: ",items[i][2])
        print("And 'x' to leave this menu.")
        print()
        
        
    
        
    def menu(self,market=True):
        print()
        if market:
            desc = config.get_text(self.market_prefix+game.city.time_of_day())
            stock = self.market_stock
            keys = self.market_keys
        else:
            desc = config.get_text(self.store_prefix+game.city.time_of_day())
            stock = self.store_stock
            keys = self.store_keys
        print(desc)
        while desc != '':
            self.print_menu(market)
            choice = input("What's your option: ")
            if choice == 'x':
                desc = ''
                game.city.menu()
            elif choice == 's' and market:
                self.sell_menu()
            elif choice == 'b':
                print("You begin to brows some wares.")
                self.buy_menu(stock)
            elif choice == "rich":
                game.character.cash_on_hand += 1000000
                print("And you've now got a million dollars!")
                x = input("Enter to continue")
            elif choice == "looty":
                game.character.inventory['loot'] = 100
                print("And some Heinikan")
                x = input("enter to continue")
            else:
                print("Didn't recognize that option")
                
            
class Bar:
    def __init__(self,game):
        self.beer_base = 4
        self.beer_price = 10
        self.beer_stress = 3
        self.event_interrupt = False
        self.so_stress = 1
        self.prefix = "bar_"
        
    def new_beer(self,value):
        self.beer_stress += value
        if self.beer_stress < 1:
            self.beer_stress = 1
            print(config.get_text('beer1'))
        elif self.beer_stress > 5:
            self.beer_stress = 5
            print(config.get_text('beer2'))           
        self.beer_price = self.beer_stress*2 + self.beer_base
        

        
        
    def buy_booze(self):
        '''reduces cash on hand, reduces stress'''
        
        game.event_manager.bar_event()
        if self.event_interrupt:
            self.event_interrupt = False
            '''this is in case the event says no beer or something'''
        elif game.character.cash_on_hand >= self.beer_price:
            game.character.cash_on_hand -= self.beer_price
            game.character.stats['stress']['current'] += self.beer_stress
            game.city.available_time -= 1
            print("You buy some beer and spend an hour drinking it. You regain",self.beer_stress,"points of stress.")
        else:
            print("You need money to buy beer!")
        
            
        
        
    def flirt(self):
        '''possible chance of ability to flirt with SO, reduces stress for free'''
        game.event_manager.bar_event()
        if self.event_interrupt:
            self.event_interrupt = False
        else:
            game.city.available_time -= 1
            game.character.stats['stress']['current'] += self.so_stress
            print("You flirt with your SO")
        
    def print_menu(self):
        
        game.city.time_for_menu()
        print()
        print("Current beer price is",game.bank.symbol+str(self.beer_price),"and relieves",self.beer_stress,"of stress.")
        print("This is a game.bar. Buy booze, or flirt with your SO who works here.")
        print("[B]uy Booze for $ | [F]lirt with your SO")
        print("Or e[x]it to the game.city.")
        print()
        
    def menu(self):
        desc = config.get_text(self.prefix+game.city.time_of_day())
        if game.city.available_time <= 0:
            print("The bar is closed. GO HOME!")
            game.city.menu()
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
                game.city.menu()
            elif choice == 'f':
                self.flirt()
            elif choice == 'b':
                self.buy_booze()
            else:
                print("Not a valid option")
                
class EventManager:
    def __init__(self,game):
        '''job table here temporarily. Will be moved to seperate events file at some point.'''
        '''then it would be self.job_event_table = imported thing from other file'''
        prefix = "event_"
        import events
        
        self.job_event_table = events.job
        self.job_keys = list(self.job_event_table.keys())
        
        self.bar_event_table = events.bar
        self.bar_keys = list(self.bar_event_table.keys())
        
    def bar_event(self):
        '''bar event handler, 15-20 on d20 for event'''
        if randint(1,20) < 15:
            game.bar.event_interrupt = False
            return None
            
        event_key = self.bar_keys[randint(0,len(self.bar_keys)-1)]
        event = self.bar_event_table[event_key]   
        game.bar.event_interrupt = event['interrupt']
        print(config.get_text(event_key))
        #gets an event from the table, checks if it's an interrupt business event, prints event text, then handles based on event type
        
        if event['type'] == 'beer':
            game.bar.new_beer(event['value'])
        if event['type'] == 'cash':
            if game.character.cash_on_hand + event['value'] < 0:
                game.character.cash_on_hand = 0
            else:
                game.character.cash_on_hand += event['value']
        if event['type'] == 'stat':
            game.character.change_current_stat(event['key'],event['value'])
        
        
    
    def job_event(self):
        event_key = self.job_keys[randint(0,len(self.job_keys)-1)]
        event = self.job_event_table[event_key]
        #might actually be useful for a case|switch, value of lambdas, since everything is sorta standardized up to the impact.
        if event['type'] == 'skill_up':
            game.character.raise_skill_event(event['key'])
        if event['type'] == 'stat_mod_per_hour':
            game.job.modified_per_hour_stat_cost[event['key']] += event['value']
        if event['type'] == 'pay_mod':
            game.job.modified_pay += event['value']
        if event['type'] == 'time_mod':
            game.job.modified_hours += event['value']
        game.job.event_string = config.get_text(event_key)
        

        
        
        
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
    
    def work(self):
        '''formula for work is 9.00 + game.character.skill[mechanics]. At Mechanics 1 rate is 10.00/hour, Mechanics 2 is 11.00/hour, 5 is 14 etc.'''
        '''10 hours work max, but will auto-consume all availble hours if less. Final pay will be told after Event, and autodeposits in game.bank.'''
        '''Work Event adds Stress and reduces Stamina'''
        self.reset_modified()
        game.city.available_time -= self.hours
        self.modified_pay = self.base_pay + game.character.skills['mechanics']['mod']
        print(self.modified_pay, self.base_pay, game.character.skills['mechanics']['mod'])
        self.modified_hours = self.hours
        game.event_manager.job_event()
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
        print("After",self.hours,"of hard labor in the mechanic shop, with a total Mechanics Skill of ",game.character.skills['mechanics']['mod'],"you have earned",game.bank.symbol+str(self.earned)+"!")
        
        print("It gets automatically deposited into your bank account.")
        print("Work also took out of you",self.total_stat_cost['stamina'],"points of stamina",self.total_stat_cost['stress'],"stress control",self.total_stat_cost['health'],"health.")
        print("Also you pretty much get kicked out of the shop when your shift is over")
        x = input("Press Enter to Continue")
        print()
        
    
        
    def print_menu(self):
        
        game.city.time_for_menu()
        print()
        print("You can [W]ork for",self.hours,"hours, or you can ['L']eave.")
        print()
        
    def menu(self):
        desc = config.get_text(self.prefix+game.city.time_of_day())
        if game.city.available_time >= 10:
            self.hours = 10
        else:
            self.hours = game.city.available_time
        print()
        print(desc)
        while desc != '':
            if game.city.available_time == 0:
                desc = ''
                print("The shop is shut down for the day. You need to go game.home.")
                game.city.menu()
            elif not self.can_work:
                desc = ''
                print("The shop might still be open, but you can't work any more hours. No overtime allowed!")
                game.city.menu()
            else:
                self.print_menu()
                choice = input("Will you do?: ").lower()
                if choice == 'l':
                    desc = ''
                    print()
                    print("You leave your workplace.")
                    print()
                    game.city.menu()
                elif choice == 'w':
                    desc = ''
                    self.work()
                    game.city.menu()
                else:
                    print("Not a valid option")
        
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
        
    def end_night(self):
        '''ends the day. consumes all remaining hours, restores stamina and reduces stress via base rate per hour + modifiers. Can cause event that instead raises stress if Health threshhold is breached; the SO doesn't like seeing you hurt and will argue with you over the Heists'''
        hours = game.city.available_time
        if randint(1,100) >60 and game.character.stats['health']['penalty']:
            '''if I had a proper event system, this is where a spawn_event(home) would go!'''
            '''instead you just get a 40% chance of no stress healing and additional penalty if you're at or below Health threshold.'''
            stamina_regained = (self.bonus_stam + self.base_stamina_restoration) * hours
            game.character.stats['stamina']['current'] += stamina_regained
            stress_lost = randint(1,2)
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
        game.city.advance_day()
        game.character.nights_not_home = 0
        #kicks you back to game.hideout.menu()
        
    def print_menu(self):
            
        game.city.time_for_menu()
        print()
        print(" 'A'dd Upgrade | 'U'ninstall Upgrade ")
        print(" 'R'est        |  'L'eave ")
        print()
        
    def win(self):
        print(config.get_text('win1'))
        x = input("...")
        print(config.get_text('win2'))
        x = input("...")
        print(config.get_text('win3'))
        x = input("...")
        print(config.get_text('intro1'))
        x = input("...")
        print(config.get_text('win4'))
        x = input("...")
        print(config.get_text('win5'))
        x = input("...")
        print(config.get_text('win6'))
        x = input("...")
        print(config.get_text('title'))
        x = input("...")
        print(config.get_text('title2'))
        x = input("Press Enter to End")
        
        
    def menu(self):
        if game.character.inventory['papers'] >0:
            self.win()
            return "Thank you for playing!"
            
        desc = config.get_text(self.prefix+game.city.time_of_day())
        print()
        print(desc)
        while desc != '':
            self.print_menu()
            choice = input("Will you do?: ").lower()
            if choice == 'l':
                desc = ''
                print()
                print("You leave your game.home.")
                print()
                game.city.menu()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            elif choice == 'r':
                self.end_night()
            else:
                print("Not a valid option")
        
class Hideout:
    def __init__(self,game):
        self.prefix = "hide_"
        self.base_stamina_restoration = 1
        self.base_health_restoration = 1
        self.upgrades = {}
        self.health_modifier = 0
        self.stamina_modifier = 0
        self.level_up_options = { '1': ('health','stat'), '2': ('stamina','stat'), '3': ('stress','stat'), '4': ('shoot','skill'), '5': ('sneak','skill'), '6': ('mechanics','skill',), }
        
    
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to game.bank.expenses'''
        print("Adds an installed upgrade, will pay full weekly cost at end of week.")
        
    def remove_upgrade(self):
        '''removes from self.upgrades and places in inventory, reduces bonus. Bank removes from list after processing the week'''
        print("Removes an installed upgrade. Will still need to pay weekly bill for it. Submenu")
        
    def spend_xp_menu(self):
        '''allows character to spend xp to increase skills and max stats by +1, cost is current level.'''
        print("This is main XP spending loop")
        run_menu = True
        while run_menu:
            self.print_menu_xp()
            option = str(input("Your decision: "))
            if option == 'x':
                run_menu = False
                print("Going back to the Hideout menu")
                print()
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
            
        
    def print_menu_xp(self):
        '''called by spend_xp_menu to do the needful'''
        print()
        print("Put in the number of the one you want")
        print("1: Max Health",game.character.stats['health']['max'],":",str(game.character.stats['health']['level'])+"xp for +1  |  4: Shoot",str(game.character.skills['shoot']['skill']),":",str(game.character.skills['shoot']['skill'])+"xp for +1") 
        print("2: Max Stamina",game.character.stats['stamina']['max'],":",str(game.character.stats['stamina']['level'])+"xp for +1 |  5: Sneak",str(game.character.skills['sneak']['skill']),":",str(game.character.skills['sneak']['skill'])+"xp for +1") 
        print("3: Max Stress",game.character.stats['stress']['max'],":",str(game.character.stats['stress']['level'])+"xp for +1  |  6: Mechanics",str(game.character.skills['mechanics']['skill']),":",str(game.character.skills['mechanics']['skill'])+"xp for +1")
        print("Can build static form for this")
        print("or choose 'x' to exit")
        print()
        
        
    def end_night(self):
        '''ends the day. Consumes remaining hours. Restores health and stamina as per base, plus mods. Can cause event that raises stress for not being Home'''
        hours = game.city.available_time
        stamina_regained = (self.stamina_modifier + self.base_stamina_restoration) * hours
        health_regained = (self.health_modifier + self.base_health_restoration) * hours
        game.character.stats['health']['current'] += health_regained
        game.character.stats['stamina']['current'] += stamina_regained
        if game.character.nights_not_home > 1 and randint(1,100)+game.character.nights_not_home >80:
            '''if I had a proper event system, this is where a spawn_event(hideout) would go!'''
            '''instead you just get a 20% chance of more stress.'''
            stress_lost = randint(1,2)
            game.character.stats['stress']['current'] -= stress_lost
            print("You miss your SO, and the thoughts of being without them has decreased your stress handling by",stress_lost)
            
        print("Resting in the hideout for",hours,"hours gets you up to",stamina_regained,"stamina and",health_regained,"health back.")
        print("But not more than your max!")
        game.city.advance_day()
        game.character.nights_not_home += 1
        #kicks you back to game.hideout.menu()
        
    def end_night_penalty(self):
        '''ends the day. Called by HeistDirector if the heist used up the next day's hours, too'''
        #there's 24 hours in a day. minimum of 4 for sleep, so normally just 20. But since there was no sleep, we'll count that 4.
        time_lost = game.city.available_time + 4
        if time_lost > 0:
            time_lost = 0
        #this checks if you were 4 or fewer hours in time-debt, and puts you to 0 instead of a negative. No gaining hours this way!      
        game.character.stats['stamina'] -= 1
        game.character.stats['stress'] += 1
        game.city.advance_day(penalty=time_lost)
        #calls advance_day function for game.city. Passes penalty along.
        print("Blurb about getting no sleep or arriving back mid-day with no rest.")
        game.character.nights_not_home += 1
        game.hideout.menu()
        #end_night doesn't need this since it was called from the menu already, but this is called from the HeistManager run_heist method.
        
        
    def heist(self):
        '''goes on a heist. May list multiple options with differing difficulty and reward levels. Seperate module'''
        '''requires certain threshold of health AND stamina to attempt'''
        print("Awww shit bro!.")
        self.director.menu()
        
    def print_menu(self):
        
        game.city.time_for_menu()
        print()
        print(" You can look in the 'M'irror")
        print(" Your 'I'nventory is messy right now")
        print(" 'T'rain | 'P'lan Heist ")
        print(" 'A'dd or 'U'ninstall Upgrade")
        print(" 'R'est  | 'L'eave Hideout")
        print()
        
    def menu(self):
        
        desc = config.get_text(self.prefix+game.city.time_of_day())
        print()
        print(desc)
        while desc != '':
            self.print_menu()
            choice = input("What will you do?: ").lower()
            print()
            if choice == 'l':
                desc = ''
                print()
                print("Well, seeya!")
                print()
                game.city.menu()
            elif choice == 't':
                self.spend_xp_menu()
            elif choice == "m":
                game.character.mirror()
            elif choice == 'p':
                self.heist()
            elif choice == 'r':
                self.end_night()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            elif choice == 'i':
                game.character.print_inventory()
            else:
                print("Not a valid option")
                print()

##---Heist System Begin ---##
class Director:
    def __init__(self,game):
        
        import heist_storage
        self.scene_data = heist_storage.scene_data_list
        self.scene_types = heist_storage.scene_type_list
        
        import option_storage
        self.option_data = option_storage.option_list
        
        
        self.possible_heists = {}
        #dict with heists when chosing from menu
        
        self.xp = config.minimum_heist_xp
        self.results = {}
        #displays results of heist
        self.run_menu = True
        
        self.loot_table = {
            'loot': {
                '1':1,
                '2':2,
                '3':4,
                '4':8,
                '5':16,
            },
            'cash': {
                '1':10,
                '2':25,
                '3':50,
                '4':100,
                '5':200,
            },
            'item': {
                '1':None,
                '2':None,
                '3':None,
                '4':None,
                '5':None,
            }
        }
        
    def generate_heist_options(self):
        '''clears out possible_heists and generates new ones'''
        self.possible_heists = {}
        #clears any prior heists.
        for heist in range(config.heist_count):
            self.possible_heists[str(len(self.possible_heists)+1)] = self.heist_generator()
            #first would be possible_heists[1], etc.
            
    def heist_generator(self):
        '''generates data for to choose heists'''
        heist = {}
        
        '''get difficulty and scene count'''
        heist['difficulty'] = game.character.xp_stage + randint(-2,2)
        if heist['difficulty'] >= 4:
            heist['difficulty'] = 4
            heist['scene_count'] = config.scene_max
        elif heist['difficulty'] <= 0:
            heist['difficulty'] = 0
            heist['scene_count'] = config.scene_min
        else:
            heist['scene_count'] = randint(config.scene_min,config.scene_max)
            
            
        '''get type and blurb_id'''
        heist['type'] = list(self.scene_types.keys())[randint(0,len(self.scene_types)-1)]
        type_data = self.scene_types[heist['type']]
        heist['blurb_id'] = type_data[0]+str(randint(1,type_data[1]))
#        heist_foe = foes[type][randint(0,len(foes[type])-1)]
        
        heist['scene_list'] = []
        scenes_of_type = list(self.scene_data[heist['type']].keys())
        for scene in range(heist['scene_count']):
            heist['scene_list'].append(scenes_of_type[randint(0,len(scenes_of_type)-1)])
               
        
        heist['hours_cost'] = randint(config.scene_min_time_roll,config.scene_max_time_roll)+(config.scene_time_mod_per_scene*heist['scene_count']) 
        #defaults to 2-8 + 2 per scene, min 5, max 18.
        #variable. Needs work. Uses configs. Subtracts total from time_available when  heist ends
        
        #heist has 'difficulty', 'scene_count', 'type', 'blurb_id', 'scene_list'(list), and 'hours_cost'
        #stored by director and formatted for menu, and passed to run_heist()
        return heist
        
            
    def run_heist(self, heist):
        self.results = {}
        self.xp = config.minimum_heist_xp
        #clearing prior heists, adding initial value for XP
        self.scene_list = heist['scene_list']
        for key in self.scene_list:
            print()
            print()
            scene = Scene(heist['type'],key,heist['difficulty'])
            scene.menu()
        self.handle_results(heist['hours_cost'])
        self.end_heist(heist['hours_cost'])
        
    def handle_results(self,hours):
        
        size = len(self.results)
        self.results['cash'] = 0
        self.results['loot'] = 0
        self.results['items'] = []
        for i in range(0,size):
            x = self.results[str(i)]
            if x[1][0]:
                self.results['loot'] += x[1][1][0]
                self.results['cash'] += x[1][1][1]
                if x[1][1][2] != None:
                    self.results['items'].append(x[1][1][2])
        game.character.cash_on_hand = self.results['cash']
        game.character.inventory['loot']['qty'] += self.results['loot']
        ##assumes (item,qty,val) tupple result
        for item in self.results['items']:
            if item[0] in game.character.inventory:
                game.character.inventory[item[0]]['qty'] += item[1]
            else:
                game.character.inventory[item[0]] = {'qty':item[1],'value':item[2]}
        game.character.add_xp(self.xp)
        print("Here's the results of your run:")
        print("You gained",self.xp,"experience points.")
        print("You earned "+game.bank.symbol+str(self.results['cash'])+", and "+str(self.results['loot'])+" pieces of loot!")
        if self.results['items']:
            print("You also earned ",self.results['items'])
        print("Not bad for ",hours,"hours of work, eh?")
        pause_x()
        

    
    def end_heist(self, cost):
        self.run_menu = False
        game.city.available_time -= cost
        if game.city.available_time == 0:
            game.hideout.end_day()
            game.hideout.menu()
        elif game.city.available_time < 0:
            game.hideout.end_night_penalty()
            game.hideout.menu()
            ##you've got 20 hours in the day available; if you do anything in the morning and then heist you'll be back the next day instead.
            ##do not gain any health or stamina regen when this occurs.
        else:
            game.hideout.menu()
            
    def print_menu(self):
        '''Lists Heist options and back to Hideout'''
        for i in self.possible_heists:
            print(i, self.possible_heists[i])
        print("Or x to go back to the Hideout")
    
    def menu(self):
        self.run_menu = True
        print("Planning blurb from hideout temp string")
        self.generate_heist_options()
        while self.run_menu:
            self.print_menu()
            choice = str(input("What'll it be? :")).lower()
            if choice in self.possible_heists:
                self.run_heist(self.possible_heists[choice])
            elif choice == 'x':
                self.run_menu = False
                game.hideout.menu()
            else:
                print("Didn't catch that...")
        #run_heist will directly back to the game.hideout.

class Scene:
    '''A heist is comprised of multiple Scenes'''
    
    def __init__(self,type,scene_id,difficulty,game):
        #heist has 'difficulty', 'scene_count', 'type', 'blurb_id', 'scene_list'(list), and 'hours_cost'
        self.scene_id = scene_id
        self.scene_data = self.director.scene_data[type][scene_id]
        
        self.option_list = [("1",'shoot'),("2",'sneak'),("3",'mechanics'),("4","stamina"),]
        self.options = {"1": {}, "2": {}, "3": {}, "4":{},}
        #always shoot, sneak, mechanics, stamina.
        if self.scene_data['options']['item'] != None:
            self.option_list.append(("5","item"))
            self.options["5"] = {}
            #check if there's an item option. Pre-reqs later
        for option in self.option_list:
            id = self.scene_data['options'][option[1]][randint(0,len(self.scene_data['options'][option[1]])-1)]
            self.options[option[0]]['id'] = id
            self.options[option[0]]['data'] = self.director.option_data[id]
            self.options[option[0]]['data']['difficulty'] += difficulty
            #automates grabbing all that.
            self.options[option[0]]['hidden'] = self.req_check(self.options[option[0]]['data']['requirement'])
            if self.options[option[0]]['data']['attribute'] == "stamina":
                self.options[option[0]]['data']['versus'] = game.character.stats['stamina']['level'] + game.character.total_penalty
            elif self.options[option[0]]['data']['attribute'] == 'item':
                self.options[option[0]]['data']['versus'] = 2
                #stick in an item quality bonus/penalty?
            else:
                attribute = self.options[option[0]]['data']['attribute']
                self.options[option[0]]['data']['versus']= game.character.skills[attribute]['mod'] + game.character.total_penalty
                    
    def req_check(self,req):
        '''checks against requirements, either False, or tupple of skill/stat/item,key,value.'''
        ''' used for building the option list hidden tag.'''
        if req is None:
            return False
        elif req[0] == 'skill':
            return game.character.skills[req[1]] >= req[2]
        elif req[0] == 'stat':
            return game.character.stats[req[1]] >= req[2]
        elif req[0] == 'item':
            return game.character.has_item(req[1],req[2],)
        else:
            return False
            
        
        
        '''Format strings for self.scene_data for flavoring and foe.'''
        '''Format strings for self.options[all] for flavoring, foe, and final difficulty'''
        '''self.choice_list = {} / for option in self.options: self.choice_list[len(self.choice_list)]= (option, self.options['blurb'])'''
        
    def print_menu(self):
        for number in range(1,len(self.options)):
            option = self.options[str(number)]
            attribute = option['data']['attribute']
            if attribute == 'item':
                qty = game.character.inventory[option['data']['item']]['qty']
                print(number+": ",config.get_text(option[id]+"menu"),": ("+option['data']['item'],qty,"Difficulty: ",option['data']['difficulty'])
            else:
                print(str(number)+": ",config.get_text(option['id']+"menu"),": ("+attribute,str(option['data']['versus']),"Difficulty: ",option['data']['difficulty'])
        '''prints option strings and option_choice_list for them'''
        '''for choice in self.choice_list: / print(choice,choice_list[choice][2])'''
        '''the above would be formatted nicer, yeah.'''
        
    def menu(self):
        print(config.get_text(self.scene_id+"start") )
        run_menu = True
        print()
        while run_menu:
            self.print_menu()
            choice = input("Make your decision: ")
            '''format choice so it matches properly'''
            print()
            if choice in self.options:
                results = self.test(self.options[choice]['id'],self.options[choice]['data'])
                if results[0]:
                    print(config.get_text(self.options[choice]['id']+"success"))
                    print(config.get_text(self.scene_id+"success"))
                    self.director.xp += 1
                    run_menu = False
                    self.director.results[str(len(self.director.results))] = (self.scene_id,results)
                    #should collapse back to director control
                else:
                    run_menu = False
                    print(config.get_text(self.options[choice]['id']+"fail"))
                    self.director.results[str(len(self.director.results))] = (self.scene_id,results)
                    #should collapse back to director control
                print(config.get_text(self.scene_id+"end"))
                pause_x()
            else:
                print("That isn't an option here!")
                
        
    def test(self,id,data):
        '''unpack option data'''
        if data['versus'] + randint(1,10) >= randint(1,5) + data['difficulty']:
            stat_cost = data['suc_cost']
            item_cost = data['suc_item']
            if stat_cost != None:
                for each in stat_cost:
                    self.game.character.stats[each[0]] += each[1]
                    game.character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    game.character.inventory[item[0]]['qty'] - item[1]
            return (True, self.grant_reward(data['difficulty']),stat_cost,item_cost)
        else:
            stat_cost = data['fail_cost']
            item_cost = data['fail_item']
            for each in stat_cost:
                game.character.stats[each[0]] += each[1]
                game.character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    game.character.inventory[item[0]]['qty'] - item[1]
            return (False, (0,0,0),stat_cost,item_cost)
            
        
    def grant_reward(self,data):
        '''grabs reward per data'''
        mod = data - game.character.xp_stage
        temp = {}
        for treasure in self.director.loot_table:
            roll = randint(1,5) + mod
            if roll <=1:
                temp[treasure] = self.director.loot_table[treasure]["1"]
            elif roll >=5:
                temp[treasure] = self.director.loot_table[treasure]["5"]
            else:
                temp[treasure] = self.director.loot_table[treasure][str(roll)]
        return (temp['loot'], temp['cash'], temp['item'])
        #note: Above defaults to None if None

##---Heist System End ---##            
        


##---Loading Game Objects ---##
class Game:
    '''NOT IMPLIMENTED'''
    def __init__(self):
        self.loaded = False
#        from settings import GameConfiguration
#        self.config = GameConfiguration()
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
        
        
        from player import Character
        self.city = City(self)
        self.bank = Bank(self)
        self.market = Market(self)
        self.bar = Bar(self)
        self.home = Home(self)
        self.hideout = Hideout(self)
        self.character = Character(self)
        self.event_manager = EventManager(self)
        self.job = Job(self)
        self.loaded = False
        


    
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
                self.city.menu()
                self.loaded = True
            elif choice == 'r' and not self.loaded:
                print("Starting a new game")
                intro()
                run_menu = False
                self.loaded = True
                self.city.menu()
            elif choice == 's':
                self.save_menu()
            elif choice == 'l':
                self.load_menu()
            else:
                print("Not a valid option")
                
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
                        
                        

import pickle
from settings import GameConfiguration
config = GameConfiguration()

game = Game()


                    
if __name__ == '__main__':
    #intro()
    #game.city.menu()
    game.main_menu()
    #game.market.menu()
    