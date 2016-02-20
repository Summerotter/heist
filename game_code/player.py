''' character class. Perhaps rename it on init? '''


       
class Character:
    def __init__(self,game):
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
        
        
    def change_current_stat(self,stat,value):
        '''called when taking damage or given boost'''
        self.stats[stat]['current'] += value
        self.update_stat(stat)
        
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
        
    def raise_stat_event(self,stat):
        self.stats[stat]['max'] += 1
        self.stats[stat]['level'] += 1
        
    def raise_skill_event(self,skill):
        self.skills[skill]['skill'] += 1
            
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
        
    def has_item(self, key, value):
        if not key in self.inventory:
            return False
        elif self.inventory[key] < value:
            return False
        else:
            print("Has it.")
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


        