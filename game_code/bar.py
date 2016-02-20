class Bar:
    def __init__(self,game):
        self.beer_base = 4
        self.beer_price = 10
        self.beer_stress = 3
        self.event_interrupt = False
        self.so_stress = 1
        self.prefix = "bar_"
        self.symbol = game.config.symbol
        self.get_text = game.config.get_text
        
    def new_beer(self,value):
        self.beer_stress += value
        if self.beer_stress < 1:
            self.beer_stress = 1
            print(self.get_text('beer1'))
        elif self.beer_stress > 5:
            self.beer_stress = 5
            print(self.get_text('beer2'))           
        self.beer_price = self.beer_stress*2 + self.beer_base
        

        
        
    def buy_booze(self,game):
        '''reduces cash on hand, reduces stress'''
        
        game.event_manager.bar_event(game)
        if self.event_interrupt:
            self.event_interrupt = False
            '''this is in case the event says no beer or something'''
        elif game.character.cash_on_hand >= self.beer_price:
            game.character.cash_on_hand -= self.beer_price
            game.character.stats['stress']['current'] += self.beer_stress
            game.available_time -= 1
            print("You buy some beer and spend an hour drinking it. You regain",self.beer_stress,"points of stress.")
        else:
            print("You need money to buy beer!")
        
            
        
        
    def flirt(self,game):
        '''possible chance of ability to flirt with SO, reduces stress for free'''
        game.event_manager.bar_event(game)
        if self.event_interrupt:
            self.event_interrupt = False
        else:
            game.available_time -= 1
            game.character.stats['stress']['current'] += self.so_stress
            print("You flirt with your SO")
        
    def print_menu(self):
        
        print()
        print("Current beer price is",self.symbol+str(self.beer_price),"and relieves",self.beer_stress,"of stress.")
        print("This is a game.bar. Buy booze, or flirt with your SO who works here.")
        print("[B]uy Booze for $ | [F]lirt with your SO")
        print("Or e[x]it to the game.city.")
        print()
        
    def menu(self,game):
        desc = self.get_text(self.prefix+game.time_of_day())
        run_menu = True
        if game.available_time <= 0:
            print("The bar is closed. GO HOME!")
            run_menu = False
            
        print()
        print(desc)
        
        while run_menu:
            game.time_for_menu()
            self.print_menu()
            choice = input("What'll it be? ").lower()
            if choice == 'x':
                run_menu = False
                print()
                print("Well, seeya!")
                print()
                game.city_menu()
            elif choice == 'f':
                self.flirt(game)
            elif choice == 'b':
                self.buy_booze(game)
            else:
                print("Not a valid option")
        game.city_menu()