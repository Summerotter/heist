class Bank:
    def __init__(self,game):
        '''starts with 600 cash, and a $ symbol'''
        self.prefix = "bank_"
        self.account = 600
        self.symbol = game.config.symbol
        self.expense_list = {'ble':600,}
        self.expense_sum = 600
        #expense_list is a dict, can add more in or remove them. Basic Living Expenses is 600.
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
        
        
    def deductions(self,game):
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
            
    def deposit(self,game):
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
        
        
    def withdraw(self,game):
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
        
    def print_menu(self,game):
        
        game.time_for_menu()
        print()
        print(" You have",self.symbol+str(self.account),"in your account, and",self.symbol+str(game.character.cash_on_hand),"on you.")
        print(" Your expenses are",self.symbol+str(self.expense_sum),"a week.")
        print(" Make a 'D'eposit | Make a 'W'ithdrawl")
        print(" Or you can 'L'eave. ")
        print()
            
    def menu(self,game):
        '''prints the menu. Options for withdrawl, deposit, viewing accounting sheet, and depart. On Exit, self.transaction set to False, and game.available_time -= 1 '''
        desc = game.config.get_text(self.prefix+game.time_of_day())
        print()
        print(desc)
            
        while desc !='':
            if game.available_time == 0:
                print("The bank is closed, and it is time for you to go game.home.")
                desc = ''
                game.city_menu()
            self.print_menu(game)
            choice = input("Your option: ").lower()
            if choice == "l":
                print("You've left the game.bank.")
                desc = ''
                if self.transaction:
                    game.available_time -= 1
                game.city_menu()
            elif choice == 'd':
                self.deposit()
            elif choice == 'w':
                self.withdraw()
            else:
                print("That's not a valid option here.")
                print()