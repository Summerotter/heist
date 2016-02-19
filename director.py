class Director:
    def __init__(self,game):
        
        import heist_storage
        self.scene_data = heist_storage.scene_data_list
        self.scene_types = heist_storage.scene_type_list
        
        import option_storage
        self.option_data = option_storage.option_list
        
        
        self.possible_heists = {}
        #dict with heists when chosing from menu
        
        self.xp = game.config.minimum_heist_xp
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
        
    def generate_heist_options(self,game):
        '''clears out possible_heists and generates new ones'''
        self.possible_heists = {}
        #clears any prior heists.
        for heist in range(game.config.heist_count):
            self.possible_heists[str(len(self.possible_heists)+1)] = self.heist_generator(game)
            #first would be possible_heists[1], etc.
            
    def heist_generator(self,game):
        '''generates data for to choose heists'''
        heist = {}
        
        '''get difficulty and scene count'''
        heist['difficulty'] = game.character.xp_stage + game.randint(-2,2)
        if heist['difficulty'] >= 4:
            heist['difficulty'] = 4
            heist['scene_count'] = game.config.scene_max
        elif heist['difficulty'] <= 0:
            heist['difficulty'] = 0
            heist['scene_count'] = game.config.scene_min
        else:
            heist['scene_count'] = game.randint(game.config.scene_min,game.config.scene_max)
            
            
        '''get type and blurb_id'''
        heist['type'] = list(self.scene_types.keys())[game.randint(0,len(self.scene_types)-1)]
        type_data = self.scene_types[heist['type']]
        heist['blurb_id'] = type_data[0]+str(game.randint(1,type_data[1]))
#        heist_foe = foes[type][game.randint(0,len(foes[type])-1)]
        
        heist['scene_list'] = []
        scenes_of_type = list(self.scene_data[heist['type']].keys())
        for scene in range(heist['scene_count']):
            heist['scene_list'].append(scenes_of_type[game.randint(0,len(scenes_of_type)-1)])
               
        
        heist['hours_cost'] = game.randint(game.config.scene_min_time_roll,game.config.scene_max_time_roll)+(game.config.scene_time_mod_per_scene*heist['scene_count']) 
        #defaults to 2-8 + 2 per scene, min 5, max 18.
        #variable. Needs work. Uses configs. Subtracts total from time_available when  heist ends
        
        #heist has 'difficulty', 'scene_count', 'type', 'blurb_id', 'scene_list'(list), and 'hours_cost'
        #stored by director and formatted for menu, and passed to run_heist()
        return heist
        
            
    def run_heist(self, heist,game):
        from scene import Scene
        self.results = {}
        self.xp = game.config.minimum_heist_xp
        #clearing prior heists, adding initial value for XP
        self.scene_list = heist['scene_list']
        for key in self.scene_list:
            print()
            print()
            active_scene = Scene(heist['type'],key,heist['difficulty'],game)
            active_scene.menu(game)
        self.handle_results(heist['hours_cost'],game)
        self.end_heist(heist['hours_cost'],game)
        
    def handle_results(self,hours,game):
        
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
        game.character.inventory['loot'] += self.results['loot']
        ##assumes (item,qty,val) tupple result
        for item in self.results['items']:
            if item[0] in game.character.inventory:
                game.character.inventory[item[0]] += item[1]
            else:
                game.character.inventory[item[0]] = item[1]
        game.character.add_xp(self.xp)
        print("Here's the results of your run:")
        print("You gained",self.xp,"experience points.")
        print("You earned "+game.config.symbol+str(self.results['cash'])+", and "+str(self.results['loot'])+" pieces of loot!")
        if self.results['items']:
            print("You also earned ",self.results['items'])
        print("Not bad for ",hours,"hours of work, eh?")
        

    
    def end_heist(self, cost,game):
        self.run_menu = False
        game.available_time -= cost
        if game.available_time == 0:
            game.hideout.end_night(game)
        elif game.available_time < 0:
            game.hideout.end_night_penalty(game)
            ##you've got 20 hours in the day available; if you do anything in the morning and then heist you'll be back the next day instead.
            ##do not gain any health or stamina regen when this occurs.
        else:
            game.hideout.menu(game)
            
    def print_menu(self,game):
        '''Lists Heist options and back to Hideout'''
        for i in range(1,len(self.possible_heists)+1):
            print()
            a = self.possible_heists[str(i)]
            print(i,"- Location:",game.config.get_text(a['type'])+". Difficulty: "+str(a['difficulty'])+". Time Needed:",a['hours_cost'],":",game.config.get_text(a['blurb_id']))
        print()
        print("Or x to go back to the Hideout")
    
    def menu(self,game):
        self.run_menu = True
        print("Planning blurb from hideout temp string")
        self.generate_heist_options(game)
        while self.run_menu:
            self.print_menu(game)
            choice = str(input("What'll it be? :")).lower()
            if choice in self.possible_heists:
                self.run_heist(self.possible_heists[choice],game)
            elif choice == 'x':
                self.run_menu = False
                game.hideout.menu(game)
            else:
                print("Didn't catch that...")
        #run_heist will directly back to the game.hideout.