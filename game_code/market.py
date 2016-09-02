class Market:
    #single object for both Company Store and Black Market, since they're nearly the same thing.
    def __init__(self,game):
        '''imports white and black from items.py for internal item list
        actual stock in store_stock and market_stock
        initialized as empty dicts, refresh method fixes that.
        '''
        from game_data.items import white,black
        self.store_items = white
        self.market_items = black
        self.store_prefix = "store_"
        self.market_prefix = "market_"
        self.market_stock = {'keys':{}}
        self.store_stock = {'keys':{}}
        self.store_keys = list(self.store_items.keys())
        self.market_keys = list(self.market_items.keys())
        self.market_price_mod = game.config.market_cost
        self.market_sale_mod = game.config.market_sale
        self.transaction = False
        
        self.refresh(game)
        
    def refresh(self,game):
        '''loads up a new week's worth of stock for both markets.'''
        
        #Company Store
        self.store_stock = {'keys':{}}
        #clearing out old data
        
        for item in self.store_keys:
            qty = game.randint(-1,3)
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
        self.blackmarket_refresh(self.store_keys,self.store_items,game)
        self.blackmarket_refresh(self.market_keys,self.market_items,game,store=False)
        self.market_stock['keys'][len( self.market_stock['keys'] ) +1] = 'papers'
        
    def blackmarket_refresh(self,keys,items,game,store=True):
        '''handles adding items for the black market, called twice'''
        if store:
            qty = (1,2)
            count = (2,3)
            price_mod = self.market_price_mod
        else:
            qty = (0,1)
            count = (3,4) 
            price_mod = 1
        for item in range(game.randint(count[0],count[1])):
            item_key = keys[game.randint(0,len(keys)-1)]
            if items[item_key]['value'] > 0:
                if not item_key in self.market_stock:
                    self.market_stock['keys'][len( self.market_stock['keys'] ) +1] = item_key
                    self.market_stock[item_key] = items[item_key]
                    self.market_stock[item_key]['qty'] += game.randint(qty[0],qty[1])
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
        
    def buy(self, stock, item,game):
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

            
    def sell(self, item,game):
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

        
    def print_menu(self,game,market=True):
        '''on exit, if self.transaction == True, set to False, game.city.time_available -= 1'''
        game.time_for_menu()
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
            
                
    def buy_menu(self,stock,game):
        run_menu = True
        while run_menu:
            self.print_buy_menu(stock)
            
            choice = input("What are ya buying? ")
            if game.config.is_int(choice):
                choice = int(choice)
            if str(choice).lower() == "x":
                run_menu = False
            elif choice in stock['keys']:
                if stock[stock['keys'][choice]]['qty'] < 1:
                    print("We're out of stock of that item")
                else:
                    self.buy(stock,stock['keys'][choice],game)
            else:
                print("didn't catch that.")
        '''lists all the stock options for purchasing'''
        
    def print_buy_menu(self,stock):
        for i in range(1,len(stock['keys'])+1):
            if i in stock['keys']:
                item = stock[stock['keys'][i]]
                if item['qty'] > 0:
                    print(str(i)+":",item['key']+":"+str(item['value']), "Cost: $"+str(item['cost'])," ",item['qty'],"available."  )
        print("Or 'x' to back out of this menu")
            
    def sell_menu(self,game):
        items = self.get_sellable_items(game)
        run_menu = True
        while run_menu:
            if len(items) == 0:
                print("You don't have anything for sale!")
                run_menu = False
            else:
                self.print_sell_menu(items)
                choice = input("What is your choice: ").lower()
                if game.config.is_int(choice):
                    choice = int(choice)
                if choice == 'x':
                    run_menu = False
                elif choice in items:
                    self.sell(items[choice],game)
                    items = self.get_sellable_items(game)
                else:
                    print("Did not get a valid option")
                
    def get_sellable_items(self,game):
        items = {}
        for item in game.character.inventory:
            if item in self.market_items and game.character.inventory[item] > 0: 
                items[len(items)+1]= (item,game.character.inventory[item],self.market_items[item]['sell'])
            elif item in self.store_items and game.character.inventory[item] > 0:
                items[len(items)+1]= (item,game.character.inventory[item],self.store_items[item]['sell'])
            elif item == 'loot' and game.character.inventory['loot'] > 0:
                items[len(items)+1]= (item,game.character.inventory[item],game.character.loot_value)
        return items        
        
    def print_sell_menu(self,items):
        
        print()
        for i in range(len(items)+1):
            if i in items:
                print(i, "Item: ",items[i][0], "Qty: ",items[i][1], "Sale Price: ",items[i][2])
        print("And 'x' to leave this menu.")
        print()
        
        
    
        
    def menu(self,game,market=True):
        print()
        if market:
            desc = game.config.get_text(self.market_prefix+game.time_of_day())
            stock = self.market_stock
            keys = self.market_keys
        else:
            desc = game.config.get_text(self.store_prefix+game.time_of_day())
            stock = self.store_stock
            keys = self.store_keys
        print(desc)
        while desc != '':
            self.print_menu(game,market)
            choice = input("What's your option: ")
            if choice == 'x':
                desc = ''
                game.city_menu()
            elif choice == 's' and market:
                self.sell_menu(game)
            elif choice == 'b':
                print("You begin to brows some wares.")
                self.buy_menu(stock,game)
            elif choice == "rich":
                game.character.cash_on_hand += 1000000
                print("And you've now got a million dollars!")
                x = input("Enter to continue")
            elif choice == "looty":
                game.character.inventory['loot'] = 100
                print("And some Heinikan")
                x = input("enter to continue")
            elif choice == "flashy":
                print("Flashy flashy!")
                game.character.inventory['flashbang'] = 1
                x = input("enter to continue")
            else:
                print("Didn't recognize that option")