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
    print(config.get_text("intro1"))
    x=input("...")
    print(config.get_text("intro2"))
    x=input("...")
    print(config.get_text("intro3"))
    x=input("...")
    print(config.get_text("intro4"))
    x=input("...")
    print(config.get_text("title"))
    x=input("...")
    print(config.get_text("title2"))
    x=input("Enter the Game")
    
class City:
    def __init__(self):
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
        job.can_work = True
        character.update_everything()
        if self.current_day < 7:
            self.current_day += 1
        else:
            self.current_day = 1
            self.weeks += 1
            bank.deductions()
            '''market.refresh() here'''
            
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
        city.time_for_menu()
        print("L for Load | S for Save")
        print("B for Bank | J for Job ")
        print("M for Market | C for Store")
        print("H for Hideout | O for Home")
        print("A for Bar | X for Exit")
        print()
            
    def menu(self):
        print()
        desc = config.get_text(self.prefix+city.time_of_day())
        #results in city_morning, from prefix "city_" and time_of_day "morning"
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
            character.stats['stress']['current'] -= 1
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
        
        city.time_for_menu()
        print()
        print(" You have",self.symbol+str(self.account),"in your account, and",self.symbol+str(character.cash_on_hand),"on you.")
        print(" Your expenses are",self.symbol+str(self.expense_sum),"a week.")
        print(" Make a 'D'eposit | Make a 'W'ithdrawl")
        print(" Or you can 'L'eave. ")
        print()
            
    def menu(self):
        '''prints the menu. Options for withdrawl, deposit, viewing accounting sheet, and depart. On Exit, self.transaction set to False, and city.available_time -= 1 '''
        desc = config.get_text(self.prefix+city.time_of_day())
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
        elif character.cash_on_hand >= stock[item]['cost']:
            print("This item costs $"+str(stock[item]['cost'])+", and you have $"+str(character.cash_on_hand))
            choice = input("Enter 'y' to confirm purchase: ").lower()
            if choice == 'y':
                character.add_item(item,stock[item])
                character.cash_on_hand -= stock[item]['cost']
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
            character.inventory['loot'] = 0
            character.cash_on_hand += item[1]*item[2]
            print("You just sold",item[1],"pieces of loot for $"+str(item[1]*item[2])+"!")
            print()
            x = input("Enter to continue.")
            print()
        else:
            character.remove_item(item[0])
            character.cash_on_hand += item[2]
            print("You just sold a",item[0],"for $"+str(item[2])+"!")
            print()
            x = input("Enter to continue.")
            print()

        
    def print_menu(self,market=True):
        '''on exit, if self.transaction == True, set to False, city.time_available -= 1'''
        city.time_for_menu()
        print()
        if market:
            '''prints market specific menu'''
            print("This is the Black Market Menu!")
            print("You can see what you can [b]uy, and what you can [s]ell.")
        else:
            '''prints store specific menu'''
            print("This is the Company Store Menu!")
            print("You can check out what goods we have to [b]uy.")
        print("Or e[x]it out to the city.")
            
                
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
        for item in character.inventory:
            if item in self.market_items and character.inventory[item] > 0: 
                items[len(items)+1]= (item,character.inventory[item],self.market_items[item]['sell'])
            elif item in self.store_items and character.inventory[item] > 0:
                items[len(items)+1]= (item,character.inventory[item],self.store_items[item]['sell'])
            elif item == 'loot' and character.inventory['loot'] > 0:
                items[len(items)+1]= (item,character.inventory[item],character.loot_value)
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
            desc = config.get_text(self.market_prefix+city.time_of_day())
            stock = self.market_stock
            keys = self.market_keys
        else:
            desc = config.get_text(self.store_prefix+city.time_of_day())
            stock = self.store_stock
            keys = self.store_keys
        print(desc)
        while desc != '':
            self.print_menu(market)
            choice = input("What's your option: ")
            if choice == 'x':
                desc = ''
                city.menu()
            elif choice == 's' and market:
                self.sell_menu()
            elif choice == 'b':
                print("You begin to brows some wares.")
                self.buy_menu(stock)
            elif choice == "rich":
                character.cash_on_hand += 1000000
                print("And you've now got a million dollars!")
                x = input("Enter to continue")
            elif choice == "looty":
                character.inventory['loot'] = 100
                print("And some Heinikan")
                x = input("enter to continue")
            else:
                print("Didn't recognize that option")
                
            
class Bar:
    def __init__(self):
        self.beer_price = 10
        self.beer_stress = 3
        self.event_interrupt = False
        self.so_stress = 1
        self.prefix = "bar_"
        
        
    def buy_booze(self):
        '''reduces cash on hand, reduces stress'''
        
        event_manager.bar_event()
        if self.event_interrupt:
            self.event_interrupt = False
            '''this is in case the event says no beer or something'''
        elif character.cash_on_hand >= self.beer_price:
            character.cash_on_hand -= self.beer_price
            character.stats['stress']['current'] += self.beer_stress
            city.available_time -= 1
            print("You buy some beer and spend an hour drinking it. You regain",self.beer_stress,"points of stress.")
        else:
            print("You need money to buy beer!")
        
            
        
        
    def flirt(self):
        '''possible chance of ability to flirt with SO, reduces stress for free'''
        event_manager.bar_event()
        if self.event_interrupt:
            self.event_interrupt = False
        else:
            city.available_time -= 1
            character.stats['stress']['current'] += self.so_stress
            print("You flirt with your SO")
        
    def print_menu(self):
        
        city.time_for_menu()
        print()
        print("Current beer price is",bank.symbol+str(self.beer_price),"and relieves",self.beer_stress,"of stress.")
        print("This is a bar. Buy booze, or flirt with your SO who works here.")
        print("[B]uy Booze for $ | [F]lirt with your SO")
        print("Or e[x]it to the city.")
        print()
        
    def menu(self):
        desc = config.get_text(self.prefix+city.time_of_day())
        if city.available_time <= 0:
            print("The bar is closed. GO HOME!")
            city.menu()
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
                
class EventManager:
    def __init__(self):
        '''job table here temporarily. Will be moved to seperate events file at some point.'''
        '''then it would be self.job_event_table = imported thing from other file'''
        prefix = "event_"
        self.job_event_table = {
        'job_1': {
            'text': "You seemed to understand mechanics better! +1 to your skill.",
            'type': 'skill_up',
            'key': 'mechanics',
            'value': 1,
            },
        'job_2': {
            'text': "Work was tiring today, and drained you an extra 1 stamina per hour.",
            'type': 'stat_mod_per_hour',
            'key': 'stamina',
            'value': 1,
            },
        'job_3': {
            'text': "You got shifted to doing some dangerous stuff, but it has a +"+bank.symbol+"1 an hour pay bonus.",
            'type': 'pay_mod',
            'key': None,
            'value': 1,
            },
        'job_4': {
            'text': "There was a problem with a shipment, and you were idle for an hour. Boss says he aint paying you. -1 hours of work.",
            'type': 'time_mod',
            'key': None,
            'value': -1,
            },
        }
        self.job_keys = list(self.job_event_table.keys())
        
        self.bar_event_table = {
        'bar_1': {
            'text': "A bar fight breaks out.You get hurt, and bar cleared out for a bit.",
            'interrupt': True,
            'type': 'stat',
            'key': 'health',
            'value': -1,
            },
        'bar_2': {
            'text': "SO grabs you to help wish a rush. You pocket the tips.",
            'interrupt': True,
            'type': 'cash',
            'key': None,
            'value': 50,
            },
        'bar_3': {
            'text': "New cheap beer up. Tastes like it, too.",
            'interrupt': False,
            'type': 'beer',
            'key': None,
            'value': -1,
            },
        'bar_4':{
            'text': "You've bumped into someone, and realize your pouch is lighter some money. Damn pickpocets.",
            'interrupt': False,
            'type': 'cash',
            'key': None,
            'value': -20,
            },
        'bar_5': {
            'text': "The new beer tastes better. The price matches, though",
            'interrupt': False,
            'type': 'beer',
            'key': None,
            'value': 1,
            },
        }
        self.bar_keys = list(self.bar_event_table.keys())
        
    def bar_event(self):
        if randint(1,20) < 15:
            bar.event_interrupt = False
            return None
        event = self.bar_event_table[self.bar_keys[randint(0,len(self.bar_keys)-1)]]   
        bar.event_interrupt = event['interrupt']
        print(event['text'])
        if event['type'] == 'beer':
            if bar.beer_stress + event['value'] < 1:
                print("Although really, it couldn't get worse than it already is.")
            elif bar.beer_stress + event['value'] > 5:
                print("No, the beer couldn't get better - not at the prices the bar's customers can afford, at least.")
            else:
                bar.beer_stress += event['value']
                bar.beer_price += (event['value']*2)
                print("Yeah, you can taste the difference. Your wallet does, too.")
            
        if event['type'] == 'cash':
            if character.cash_on_hand + event['value'] < 0:
                character.cash_on_hand = 0
            else:
                character.cash_on_hand += event['value']
                
        if event['type'] == 'stat':
            temp = character.stats[event['key']]['current'] + event['value']
            if temp > character.stats[event['key']]['max']:
                character.stats[event['key']]['current'] = character.stats[event['key']]['max']
            elif temp < 0:
                ccharacter.stats[event['key']]['current'] = 0
            else:
                character.stats[event['key']]['current'] = temp
        
        
    
    def job_event(self):
        event = self.job_event_table[self.job_keys[randint(0,len(self.job_keys)-1)]]
        #might actually be useful for a case|switch, value of lambdas, since everything is sorta standardized up to the impact.
        if event['type'] == 'skill_up':
            character.skills[event['key']]['skill'] += event['value']
        if event['type'] == 'stat_mod_per_hour':
            job.modified_per_hour_stat_cost[event['key']] += event['value']
        if event['type'] == 'pay_mod':
            job.modified_pay += event['value']
        if event['type'] == 'time_mod':
            job.modified_hours += event['value']
        job.event_string = event['text']
        

        
        
        
class Job:
    def __init__(self):
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
        '''formula for work is 9.00 + character.skill[mechanics]. At Mechanics 1 rate is 10.00/hour, Mechanics 2 is 11.00/hour, 5 is 14 etc.'''
        '''10 hours work max, but will auto-consume all availble hours if less. Final pay will be told after Event, and autodeposits in Bank.'''
        '''Work Event adds Stress and reduces Stamina'''
        self.reset_modified()
        city.available_time -= self.hours
        self.modified_pay = self.base_pay + character.skills['mechanics']['mod']
        print(self.modified_pay, self.base_pay, character.skills['mechanics']['mod'])
        self.modified_hours = self.hours
        event_manager.job_event()
        '''job events can cause unpaid hours, extra pay hours, bonus or penalty to wages, or a skill or stat boost'''
        self.earned = self.modified_pay * self.modified_hours
        for stat in self.modified_per_hour_stat_cost:
            self.total_stat_cost[stat] = self.modified_hours * self.modified_per_hour_stat_cost[stat]
            character.stats[stat]['current'] -= self.total_stat_cost[stat]
        bank.account += self.earned
        character.add_xp(1)
        self.can_work = False
        
        if self.event_string != '':
            print(self.event_string)
        print("After",self.hours,"of hard labor in hte mechanic shop, with a total Mechanics Skill of ",character.skills['mechanics']['mod'],"you have earned",bank.symbol+str(self.earned)+"!")
        
        print("It gets automatically deposited into your bank account.")
        print("Work also took out of you",self.total_stat_cost['stamina'],"points of stamina",self.total_stat_cost['stress'],"stress control",self.total_stat_cost['health'],"health.")
        print("Also you pretty much get kicked out of the shop when your shift is over")
        x = input("Press Enter to Continue")
        print()
        
    
        
    def print_menu(self):
        
        city.time_for_menu()
        print()
        print("You can [W]ork for",self.hours,"hours, or you can ['L']eave.")
        print()
        
    def menu(self):
        desc = config.get_text(self.prefix+city.time_of_day())
        if city.available_time >= 10:
            self.hours = 10
        else:
            self.hours = city.available_time
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
        self.prefix = "home_"
        self.base_stamina_restoration = 1
        self.base_stress_restoration = 1
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
        hours = city.available_time
        if randint(1,100) >60 and character.stats['health']['penalty']:
            '''if I had a proper event system, this is where a spawn_event(home) would go!'''
            '''instead you just get a 40% chance of no stress healing and additional penalty if you're at or below Health threshold.'''
            stamina_regained = (self.bonus_stam + self.base_stamina_restoration) * hours
            character.stats['stamina']['current'] += stamina_regained
            stress_lost = randint(1,2)
            character.stats['stress']['current'] -= stress_lost 
            print("You had a fight with your SO over your escapades. They're worried you might not come back one day, but you know its the only way for a better life for you two. You've lost",stress_lost,"points worth of stress handling.")
            print("You did recover some stamina, up to",stamina_regained,"points worth.")
        else:
            stamina_regained = (self.bonus_stam + self.base_stamina_restoration) * hours
            stress_regained = (self.bonus_stress + self.base_stress_restoration) * hours
            character.stats['stress']['current'] += stress_regained
            character.stats['stamina']['current'] += stamina_regained
            print("Resting in your home for",hours,"hours gets you up to",stamina_regained,"stamina and",stress_regained,"stress hanlding back.")
            print("But not more than your max!")
        city.advance_day()
        character.nights_not_home = 0
        #kicks you back to hideout.menu()
        
    def print_menu(self):
            
        city.time_for_menu()
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
        if character.inventory['papers'] >0:
            self.win()
            return "Thank you for playing!"
            
        desc = config.get_text(self.prefix+city.time_of_day())
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
        self.prefix = "hide_"
        self.base_stamina_restoration = 1
        self.base_health_restoration = 1
        self.upgrades = {}
        self.health_modifier = 0
        self.stamina_modifier = 0
        self.level_up_options = { '1': ('health','stat'), '2': ('stamina','stat'), '3': ('stress','stat'), '4': ('shoot','skill'), '5': ('sneak','skill'), '6': ('mechanics','skill',), }
        
    
    def add_upgrade(self):
        '''removes upgrade from inventory and adds it. Checks 'type' and adds value to the bonus'''
        '''added to bank.expenses'''
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
                    run_menu = character.raise_stat(self.level_up_options[option][0])
                elif self.level_up_options[option][1] == 'skill':
                    run_menu = character.raise_skill(self.level_up_options[option][0])
                else:
                    pass
            elif option == "cheat":
                character.add_xp(100)
                print("Cheater!")
                print()
            else:
                print("Not a valid option, that.")
            
        
    def print_menu_xp(self):
        '''called by spend_xp_menu to do the needful'''
        print()
        print("Put in the number of the one you want")
        print("1: Max Health",character.stats['health']['max'],":",str(character.stats['health']['level'])+"xp for +1  |  4: Shoot",str(character.skills['shoot']['skill']),":",str(character.skills['shoot']['skill'])+"xp for +1") 
        print("2: Max Stamina",character.stats['stamina']['max'],":",str(character.stats['stamina']['level'])+"xp for +1 |  5: Sneak",str(character.skills['sneak']['skill']),":",str(character.skills['sneak']['skill'])+"xp for +1") 
        print("3: Max Stress",character.stats['stress']['max'],":",str(character.stats['stress']['level'])+"xp for +1  |  6: Mechanics",str(character.skills['mechanics']['skill']),":",str(character.skills['mechanics']['skill'])+"xp for +1")
        print("Can build static form for this")
        print("or choose 'x' to exit")
        print()
        
        
    def end_night(self):
        '''ends the day. Consumes remaining hours. Restores health and stamina as per base, plus mods. Can cause event that raises stress for not being Home'''
        hours = city.available_time
        stamina_regained = (self.stamina_modifier + self.base_stamina_restoration) * hours
        health_regained = (self.health_modifier + self.base_health_restoration) * hours
        character.stats['health']['current'] += health_regained
        character.stats['stamina']['current'] += stamina_regained
        if character.nights_not_home > 1 and randint(1,100)+character.nights_not_home >80:
            '''if I had a proper event system, this is where a spawn_event(hideout) would go!'''
            '''instead you just get a 20% chance of more stress.'''
            stress_lost = randint(1,2)
            character.stats['stress']['current'] -= stress_lost
            print("You miss your SO, and the thoughts of being without them has decreased your stress handling by",stress_lost)
            
        print("Resting in the hideout for",hours,"hours gets you up to",stamina_regained,"stamina and",health_regained,"health back.")
        print("But not more than your max!")
        city.advance_day()
        character.nights_not_home += 1
        #kicks you back to hideout.menu()
        
    def end_night_penalty(self):
        '''ends the day. Called by HeistDirector if the heist used up the next day's hours, too'''
        #there's 24 hours in a day. minimum of 4 for sleep, so normally just 20. But since there was no sleep, we'll count that 4.
        time_lost = city.available_time + 4
        if time_lost > 0:
            time_lost = 0
        #this checks if you were 4 or fewer hours in time-debt, and puts you to 0 instead of a negative. No gaining hours this way!      
        character.stats['stamina'] -= 1
        character.stats['stress'] += 1
        city.advance_day(penalty=time_lost)
        #calls advance_day function for city. Passes penalty along.
        print("Blurb about getting no sleep or arriving back mid-day with no rest.")
        character.nights_not_home += 1
        hideout.menu()
        #end_night doesn't need this since it was called from the menu already, but this is called from the HeistManager run_heist method.
        
        
    def heist(self):
        '''goes on a heist. May list multiple options with differing difficulty and reward levels. Seperate module'''
        '''requires certain threshold of health AND stamina to attempt'''
        print("Awww shit bro!.")
        director.menu()
        
    def print_menu(self):
        
        city.time_for_menu()
        print()
        print(" You can look in the 'M'irror")
        print(" Your 'I'nventory is messy right now")
        print(" 'T'rain | 'P'lan Heist ")
        print(" 'A'dd or 'U'ninstall Upgrade")
        print(" 'R'est  | 'L'eave Hideout")
        print()
        
    def menu(self):
        
        desc = config.get_text(self.prefix+city.time_of_day())
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
                city.menu()
            elif choice == 't':
                self.spend_xp_menu()
            elif choice == "m":
                character.mirror()
            elif choice == 'p':
                self.heist()
            elif choice == 'r':
                self.end_night()
            elif choice == 'a':
                self.add_upgrade()
            elif choice == 'u':
                self.remove_upgrade()
            elif choice == 'i':
                character.print_inventory()
            else:
                print("Not a valid option")
                print()
        
class Character:
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.nickname = "Johnny"
        self.description = "a vague placeholder description of the main character"
        self.so_first_name = "Jane"
        self.so_last_name = "Fawn"
        self.so_nickname = "Fawny"
        self.so_desc = "so desc"
        #names and desc. Awww!
        
        self.nights_not_home = 0
        #For keeping track of such for events. Incrimented by Hideout end-day, set to 0 by Home.
        
        self.stats = {
            'health': {
                'current':10,
                'max': 10,
                'threshhold': 5,
                'level': 1,
                'string': "Health",
                'penalty': 0,
                },
            'stamina': {
                'current':10,
                'max':10,
                'threshhold':5,
                'level': 1,
                'string': "Stamina",
                'penalty': 0,
                },
            #Stress is really Stress Handling, works like health. 
            'stress': {
                'current':10,
                'max': 10,
                'threshhold':5,
                'level': 1,
                'string': "Stress",
                'penalty': 0,
                },
            }
        
        self.skills = {
            'shoot': {
                'skill': 1,
                'string': "Shooting",
                'equipment': ('Basic Pistol',0),
                'mod' : 1,
                },
            'sneak': {
                'skill':1,
                'string': "Sneaking",
                'equipment': ('Normal Clothing',0),
                'mod':1,
                },
            'mechanics': {
                'skill': 1,
                'string': "Mechanics",
                'equipment': ('Simple Tools',0),
                'mod': 1,
                },
            }
        
        self.total_penalty = 0
        #stats and skills
        
        self.xp_stage = 0
        
        self.cash_on_hand = 0
        self.total_xp = 0
        self.available_xp = 0
        #xp and cash, obv. total xp is all XP ever owned, available xp is what can be spent
        self.loot_value = 25
        #base price for loot, maybe it'll go up?
        self.inventory = {'loot': 0,}
        #inventory is all the items non-equipped that the character owns.
        #itemid: quantity
        
        
       
        
    def update_stat(self,stat):
        '''for applying damage taken or healing events/items'''
        if self.stats[stat]['current'] > self.stats[stat]['max']:
            self.stats[stat]['current'] = self.stats[stat]['max']
        if self.stats[stat]['current'] <= self.stats[stat]['threshhold']:
            self.stats[stat]['penalty'] = 1
        if self.stats[stat]['current'] > self.stats[stat]['threshhold']:
            self.stats[stat]['penalty'] = 0
        if self.stats[stat]['current'] < 0:
            self.stats[stat]['current'] = 0
            
            
    def update_skill(self,skill):
        '''updating modifier when leveling up or changing equipment'''
        self.skills[skill]['mod'] = self.skills[skill]['skill'] + self.skills[skill]['equipment'][1]
            
    def update_everything(self):
        '''End of day function to force recalcs'''
        self.total_penalty = 0
        for stat in self.stats:
            self.update_stat(stat)
            self.total_penalty += self.stats[stat]['penalty']
        for skill in self.skills:
            self.update_skill(skill)
            
    def add_xp(self, xp):
        '''used by events or whatever to add xp to the character.'''
        self.total_xp += xp
        self.available_xp += xp
        self.xp_stage_check()
        
    def xp_stage_check(self):
        xp = self.total_xp -1
        if xp in range(0,20):
            self.xp_stage = 0
        elif xp in range(21,40):
            self.xp_stage = 1
        elif xp in range(41,60):
            self.xp_stage = 2
        else:
            self.xp_stage = 3
        
    def raise_skill(self,skill):
        run_menu = True
        if self.available_xp >= self.skills[skill]['skill']:
            self.available_xp -= self.skills[skill]['skill']
            self.skills[skill]['skill'] += 1
            print(self.skills[skill]['string'],"has been raised by 1, and is now at",self.skills[skill]['skill'])
            run_menu = False
        else:
            print("You do not have enough XP to raise your",self.skills[skill]['string'])
        print()
        x = input("Press Enter to Continue")
        return run_menu
            
    def raise_stat(self,stat):
        run_menu = True
        if self.available_xp >= self.stats[stat]['level']:
            self.available_xp -= self.stats[stat]['level']
            self.stats[stat]['max'] += 1
            self.stats[stat]['level'] += 1
            print(self.stats[stat]['string'],"has been raised by 1, and is now at Level",self.stats[stat]['level'],": ",self.stats[stat]['max'])
            run_menu = False
        else:
            print("You do not have enough XP to raise your",self.stats[stat]['string'])
        print()
        x = input("Press Enter to Continue")
        return run_menu
        
    def has_item(self, key, value=1):
        if not key in self.inventory:
            return False
        elif self.inventory[key]['qty'] < value:
            return False
        else:
            return True

        
    def add_item(self,key,data):
        '''called by market when an item is purchased'''
        '''No need to copy the entire item over, lets see if that helps'''
        if not key in self.inventory:
            self.inventory[key] = 1
        elif key in self.inventory:
            self.inventory[key] += 1
            
    def remove_item(self,key,qty=1):
        if not key in self.inventory:
            '''okay, its already gone.'''
        elif key in self.inventory:
            if self.inventory[key] > qty:
                self.inventory[key] -= qty
                # Assumes that whatever calls remove_item would check if there's enough for their qty.
            elif key != 'loot':
                del self.inventory[key]
            
    def print_inventory(self):
        '''displays inventory'''
        for item in self.inventory:
            print(item,self.inventory[item])
            
    def mirror(self):
        '''displays stats, called by any mirror object'''
        print(self.first_name,'"'+self.nickname+"'",self.last_name+": ",str(self.available_xp)+"/"+str(self.total_xp)+" xp available/total")
        print(self.description)
        print("-----------")
        print("Stats")
        for stat in self.stats:
            print(self.stats[stat]['string']+" Current: "+str(self.stats[stat]['current'])+"| Max: "+str(self.stats[stat]['max'])+"| Penalty Threshold: "+str(self.stats[stat]['threshhold'])+"| Penalty: "+str(self.stats[stat]['penalty'])+"|")
        print("-----------")
        skill_line = ""
        equipment_line = ""
        for skill in self.skills:
            skill_line += self.skills[skill]['string']+": +"+str(self.skills[skill]['skill'])+"  "
            equipment_line += self.skills[skill]['equipment'][0]+": +"+str(self.skills[skill]['equipment'][1])+"  "
        print("Skill Levels:")
        print(skill_line)
        print("-----------")
        print("Equipment:")
        print(equipment_line)
        print("-----------")
        print("Not a bad looking person!")
        print()
        x = input("Hit Enter to continue")


        
##---Heist System Begin ---##
class Director:
    def __init__(self):
        
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
        heist['difficulty'] = character.xp_stage + randint(-2,2)
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
        character.cash_on_hand = self.results['cash']
        character.inventory['loot']['qty'] += self.results['loot']
        ##assumes (item,qty,val) tupple result
        for item in self.results['items']:
            if item[0] in character.inventory:
                character.inventory[item[0]]['qty'] += item[1]
            else:
                character.inventory[item[0]] = {'qty':item[1],'value':item[2]}
        character.add_xp(self.xp)
        print("Here's the results of your run:")
        print("You gained",self.xp,"experience points.")
        print("You earned "+bank.symbol+str(self.results['cash'])+", and "+str(self.results['loot'])+" pieces of loot!")
        if self.results['items']:
            print("You also earned ",self.results['items'])
        print("Not bad for ",hours,"hours of work, eh?")
        pause_x()
        

    
    def end_heist(self, cost):
        self.run_menu = False
        city.available_time -= cost
        if city.available_time == 0:
            hideout.end_day()
            hideout.menu()
        elif city.available_time < 0:
            hideout.end_night_penalty()
            hideout.menu()
            ##you've got 20 hours in the day available; if you do anything in the morning and then heist you'll be back the next day instead.
            ##do not gain any health or stamina regen when this occurs.
        else:
            hideout.menu()
            
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
                hideout.menu()
            else:
                print("Didn't catch that...")
        #run_heist will directly back to the hideout.

class Scene:
    '''A heist is comprised of multiple Scenes'''
    
    def __init__(self,type,scene_id,difficulty):
        #heist has 'difficulty', 'scene_count', 'type', 'blurb_id', 'scene_list'(list), and 'hours_cost'
        self.scene_id = scene_id
        self.scene_data = director.scene_data[type][scene_id]
        
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
            self.options[option[0]]['data'] = director.option_data[id]
            self.options[option[0]]['data']['difficulty'] += difficulty
            #automates grabbing all that.
            self.options[option[0]]['hidden'] = self.req_check(self.options[option[0]]['data']['requirement'])
            if self.options[option[0]]['data']['attribute'] == "stamina":
                self.options[option[0]]['data']['versus'] = character.stats['stamina']['level'] + character.total_penalty
            elif self.options[option[0]]['data']['attribute'] == 'item':
                self.options[option[0]]['data']['versus'] = 2
                #stick in an item quality bonus/penalty?
            else:
                attribute = self.options[option[0]]['data']['attribute']
                self.options[option[0]]['data']['versus']= character.skills[attribute]['mod'] + character.total_penalty
                    
    def req_check(self,req):
        '''checks against requirements, either False, or tupple of skill/stat/item,key,value.'''
        ''' used for building the option list hidden tag.'''
        if req is None:
            return False
        elif req[0] == 'skill':
            return character.skills[req[1]] >= req[2]
        elif req[0] == 'stat':
            return character.stats[req[1]] >= req[2]
        elif req[0] == 'item':
            return character.has_item(req[1],req[2],)
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
                qty = character.inventory[option['data']['item']]['qty']
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
                    director.xp += 1
                    run_menu = False
                    director.results[str(len(director.results))] = (self.scene_id,results)
                    #should collapse back to director control
                else:
                    run_menu = False
                    print(config.get_text(self.options[choice]['id']+"fail"))
                    director.results[str(len(director.results))] = (self.scene_id,results)
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
                    self.character.stats[each[0]] += each[1]
                    character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    character.inventory[item[0]]['qty'] - item[1]
            return (True, self.grant_reward(data['difficulty']),stat_cost,item_cost)
        else:
            stat_cost = data['fail_cost']
            item_cost = data['fail_item']
            for each in stat_cost:
                character.stats[each[0]] += each[1]
                character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    character.inventory[item[0]]['qty'] - item[1]
            return (False, (0,0,0),stat_cost,item_cost)
            
        
    def grant_reward(self,data):
        '''grabs reward per data'''
        mod = data - character.xp_stage
        temp = {}
        for treasure in director.loot_table:
            roll = randint(1,5) + mod
            if roll <=1:
                temp[treasure] = director.loot_table[treasure]["1"]
            elif roll >=5:
                temp[treasure] = director.loot_table[treasure]["5"]
            else:
                temp[treasure] = director.loot_table[treasure][str(roll)]
        return (temp['loot'], temp['cash'], temp['item'])
        #note: Above defaults to None if None

##---Heist System End ---##            
        


##---Loading Game Objects ---##
class Game:
    '''NOT IMPLIMENTED'''
    def __init__(self):
        self.loaded = False
        from settings import GameConfiguration
        self.config = GameConfiguration()
        self.save_list = {"a": None, "b":None, "c":None, "d":None,}
        '''grab the save file master info here'''
        '''key = name, date last played, in-game date, earned xp, total wealth, filename'''
        
        
    def start_game(self):
        self.city = City()
        self.bank = Bank()
        self.market = Market()
        self.bar = Bar()
        self.home = Home()
        self.hideout = Hideout()
        self.character = Character()
        self.event_manager = EventManager()
        
    def print_main_menu(self):
        '''lists the options for the main menu'''
        print("Howdy! 'r' to run the game, 's' to save it, 'l' to load from save, and 'q' to quit")

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
            elif choice == 'r' and not self.loaded:
                print("Starting a new game")
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
                    go = self.overwrite_prot()
                if go:
                    self.save_game(option)
                else:
                    print("Saving canceled, returning to menu")
                    
    def save_game(self,option):
        '''this will set self.save_list[option] to the right info, then pickle the game object to the pointed file.'''
        
    def load_game(self,option):
        '''gets the filename from self.save_list[option], pickle loads it and sets game = loaded_game, and self.loaded to True'''
        
    def load_menu(self):
        '''load version of save game, includes check if self.loaded is true for overwriting loaded games'''
                        
                        


#game = Game()
    
from settings import GameConfiguration
config = GameConfiguration()                    
city = City()
bank = Bank()
market = Market()
bar = Bar()
job = Job()
home = Home()
hideout = Hideout()
character = Character()
event_manager = EventManager()
director = Director()



##---End Loading Game Objects ---##


    
                    
if __name__ == '__main__':
    intro()
    city.menu()
    #game.main_menu()
    #market.menu()
    