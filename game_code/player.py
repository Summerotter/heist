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
                'equipment': 'gun0',
                'mod' : 1,
                },
            'sneak': {
                'skill':1,
                'string': "Sneaking",
                'equipment': 'cloth0',
                'mod':1,
                },
            'mechanics': {
                'skill': 1,
                'string': "Mechanics",
                'equipment': 'tool0',
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
        self.inventory = {'loot': {'qty':0,'cost':0,'sell':0,'type':"loot",'attr':None,'value':0,'key':'loot',},}
        #inventory is all the items non-equipped that the character owns.
        #itemid: quantity
        
        self.equipment = {
            'tool0':{'qty':0,'cost':0,'sell':1,'type':"equip",'attr':'mechanics','value':0,'key':'tool0',},
            'gun0':{'qty':0,'cost':0,'sell':1,'type':"equip",'attr':'shoot','value':0,'key':'gun0',},
            'cloth0':{'qty':0,'cost':0,'sell':1,'type':"equip",'attr':'sneak','value':0,'key':'cloth0',},
            }
        
        
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
        self.skills[skill]['mod'] = self.skills[skill]['skill'] + self.equipment[self.skills[skill]['equipment']]['value']
            
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
            
    def change_equipment(self,skill,new_key):
        '''called by wheverer I put the equipment change to.'''
        '''Equipment in inventory should be qty of unequiped '''
        self.equipment[self.skills[skill]['equipment']]['qty'] += 1
        self.equipment[new_key]['qty'] -= 1
        self.skills[skill]['equipment'] = new_key
        
    def add_equipment(self, key, data):
        '''called by market/store/wherever to add new equipment'''
        if not key in self.equipment:
            self.equipment[key] = data
            self.equipment[key]['qty'] = 1
        else:
            self.equipment[key]['qty'] += 1
        for item in self.equipment:
            print(item, self.equipment[item])
            
    def remove_equipment(self,key,qty=1):
        '''called to remove equipment from inventory
        checks to see if the item exists. If it does and has a qty greater than 0, it removes the qty value. Only if the qty was higher than zero and is now <= 0, does it remove. There are legit reasons for items that have no qty to be in the self.equipment dict, and they should not be removed.
        '''
        if not key in self.equipment:
            '''its not here'''
        elif self.equipment[key]['qty'] > 0:
            self.equipment[key]['qty'] -= qty
            if self.equipment[key]['qty'] <= 0:
                del self.equipment[key]
        

        
    def add_item(self,key,data,game):
        '''called by market when an item is purchased'''
        print()
        print("This is item qty after moving to player.add_item", data['qty'])
        print()
        if data['type'] == 'equip':
            self.add_equipment(key,data)
        else:
            if not key in self.inventory:
                self.inventory[key] = data
                self.inventory[key]['qty'] = 1
            else:
                self.inventory[key]['qty'] += 1
        print()
        print("This is item qty after moving player.add_item is done", data['qty'])
        print()
            
    def remove_item(self,key,qty=1):
        if not key in self.inventory:
            '''okay, its already gone.'''
        elif key in self.inventory:
            if self.inventory[key] > qty:
                self.inventory[key] -= qty
                # Assumes that whatever calls remove_item would check if there's enough for their qty.
            elif key != 'loot':
                del self.inventory[key]
            
    def print_inventory(self,game):
        '''displays inventory'''
        for item in self.inventory:
            print(game.config.get_text(item),"Qty:",self.inventory[item]['qty'])
        for item in self.equipment:
            if self.equipment[item]['qty'] > 0:
                print(game.config.get_text(item),"+"+str(self.equipment[item]['value']),"to",self.equipment[item]['attr'])
            
    def mirror(self, game):
        '''displays stats, called by any mirror object'''
        print(self.first_name,'"'+self.nickname+"'",self.last_name+": ",str(self.available_xp)+"/"+str(self.total_xp)+" xp available/total")
        print("Not a bad looking",self.gender[1],self.race[1].lower()+"!")
        print("-----------")
        print("Stats")
        for stat in self.stats:
            print(self.stats[stat]['string']+" Current: "+str(self.stats[stat]['current'])+"| Max: "+str(self.stats[stat]['max'])+"| Penalty Threshold: "+str(self.stats[stat]['threshhold'])+"| Penalty: "+str(self.stats[stat]['penalty'])+"|")
        print("-----------")
        skill_line = ""
        equipment_line = ""
        for skill in self.skills:
            skill_line += self.skills[skill]['string']+": +"+str(self.skills[skill]['skill'])+"  "
            equipment_line += game.config.get_text(self.skills[skill]['equipment'])+": +"+str(self.equipment[self.skills[skill]['equipment']]['value'])+"  "
        print("Skill Levels:")
        print(skill_line)
        print("-----------")
        print("Equipped:")
        print(equipment_line)
        print("-----------")
        x = input("Hit Enter to continue")


        