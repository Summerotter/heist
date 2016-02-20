class Scene:
    '''A heist is comprised of multiple Scenes'''
    
    def __init__(self,type,scene_id,difficulty,game):
        #heist has 'difficulty', 'scene_count', 'type', 'blurb_id', 'scene_list'(list), and 'hours_cost'
        self.scene_id = scene_id
        self.scene_data = game.director.scene_data[type][scene_id]
        self.heist_difficulty = difficulty
        self.option_list = ('shoot','sneak','mechanics',"stamina",'item')
        self.options = {}
        #always shoot, sneak, mechanics, stamina.

        for option in self.option_list:
            if self.scene_data['options'][option] != None:
                self.generate_option(option,self.scene_data['options'][option],game,self.heist_difficulty)
                
    def generate_option(self,option, scene_data,game,heist_difficulty):
        '''Picks an option for the slot, loads data, builds self.options and generates the srings.'''
        id = scene_data[game.randint(0,len(scene_data)-1)]
        data = game.director.option_data[id]
        x = self.req_check(data['requirement'],game)
        if x:
            key = str(len(self.options)+1)
            self.options[key] = {}
            self.options[key]['id'] = id
            self.options[key]['data'] = data
            self.options[key]['data']['mod_difficulty'] = heist_difficulty + self.options[key]['data']['difficulty']
            #automates grabbing all that.
            #Returns True if needs to be hidden.
            if self.options[key]['data']['attribute'] == "stamina":
                self.options[key]['data']['versus'] = game.character.stats['stamina']['level'] + game.character.total_penalty
            elif self.options[key]['data']['attribute']=="item":
                self.options[key]['data']['versus'] = 2
            else:
                attribute = self.options[key]['data']['attribute']
                self.options[key]['data']['versus']= game.character.skills[attribute]['mod'] + game.character.total_penalty
            
            opt = self.options[key]['data']
            if opt['attribute']=="item":
                qty = game.character.inventory[opt['item']]
                strng = key+": +"
                strng += game.config.get_text(id+"menu")
                strng += ": ("+str(opt['item'])+str(qty)
                strng += " Difficulty: "+str(opt['mod_difficulty'])+")"
                self.options[key]['string'] = strng
            else:

                self.options[key]['string'] = key+": "+game.config.get_text(id+"menu")+": ("+opt['attribute']+str(opt['versus'])+" Difficulty: "+str(opt['mod_difficulty'])+")"
            
            
        
                    
    def req_check(self,req,game):
        
        '''checks against requirements, either False, or tupple of skill/stat/item,key,value.'''
        ''' used for building the option list hidden tag.'''
        if req is None:
            return True
        else:
            if req[0] == 'skill':
                if game.character.skills[req[1]] >= req[2]:
                    return True
            elif req[0] == 'stat':
                if game.character.stats[req[1]] >= req[2]:
                    return True
            elif req[0] == 'item':
                if game.character.has_item(req[1],req[2]):
                    return True
            else:
                return False
            
        
        
        '''Format strings for self.scene_data for flavoring and foe.'''
        '''Format strings for self.options[all] for flavoring, foe, and final difficulty'''
        '''self.choice_list = {} / for option in self.options: self.choice_list[len(self.choice_list)]= (option, self.options['blurb'])'''
        
        
    def print_menu(self):
        '''Prints the strings for the options. ranged iterator based on len of options'''
        for each in range(1,len(self.options)+1):
            if str(each) in self.options:
                print(self.options[str(each)]['string'])
                print()
        
        
    def menu(self,game):
        print(game.config.get_text(self.scene_id+"start") )
        run_menu = True
        print()
        while run_menu:
            self.print_menu()
            choice = input("Make your decision: ").lower()
            print()
            if choice in self.options:
                results = self.test(self.options[choice]['id'],self.options[choice]['data'],game)
                if results[0]:
                    print(game.config.get_text(self.options[choice]['id']+"success"))
                    print(game.config.get_text(self.scene_id+"success"))
                    game.director.xp += 1
                    run_menu = False
                    game.director.results[str(len(game.director.results))] = (self.scene_id,results)
                    #should collapse back to director control
                else:
                    run_menu = False
                    print(game.config.get_text(self.options[choice]['id']+"fail"))
                    print(game.config.get_text(self.scene_id+"end"))
                    game.director.results[str(len(game.director.results))] = (self.scene_id,results)
                    #should collapse back to director control
                
            else:
                print("That isn't an option here!")
                
        
    def test(self,id,data,game):
        '''unpack option data'''
        if data['versus'] + game.randint(1,10) >= game.randint(1,5) + data['mod_difficulty']:
            stat_cost = data['suc_cost']
            item_cost = data['suc_item']
            if stat_cost != None:
                for each in stat_cost:
                    game.character.stats[each[0]]['current'] += each[1]
                    game.character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    game.character.inventory[item[0]] -= item[1]
            return (True, self.grant_reward(data['mod_difficulty'],game),stat_cost,item_cost)
        else:
            stat_cost = data['fail_cost']
            item_cost = data['fail_item']
            for each in stat_cost:
                game.character.stats[each[0]]['current'] += each[1]
                game.character.update_stat(each[0])
            if item_cost != None:
                for item in item_cost:
                    game.character.inventory[item[0]] -= item[1]
            return (False, (0,0,0),stat_cost,item_cost)
            
        
    def grant_reward(self,data,game):
        '''grabs reward per data'''
        mod = data - game.character.xp_stage
        temp = {}
        for treasure in game.director.loot_table:
            roll = game.randint(1,5) + mod
            if roll <=1:
                temp[treasure] = game.director.loot_table[treasure]["1"]
            elif roll >=5:
                temp[treasure] = game.director.loot_table[treasure]["5"]
            else:
                temp[treasure] = game.director.loot_table[treasure][str(roll)]
        return (temp['loot'], temp['cash'], temp['item'])
        #note: Above defaults to None if None
        #Move reward to Director later?