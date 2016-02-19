class GameConfiguration:
    def __init__(self):
        self.minimum_heist_xp = 1
        self.heist_count = 3
        self.scene_min = 3
        self.scene_max = 5
        self.scene_min_time_roll = 2
        self.scene_max_time_roll = 8
        self.scene_time_mod_per_scene = 2
        self.language = 'eng'
        
        #would be able to edit this later via config options
        #expand this for Difficulty options later?
        #things like Black Market and Company Store stock/qty, basic_living_costs, bank fee, job wage.
        self.market_cost = 1.5
        self.market_sale = .5
        self.symbol = "$"
        
        from text_blurbs import text
        self.text = text
        
    def get_text(self, key):
        #Used to better handle multilanguage
        #checks if key passed exists. If it doesn't, passes the key back.
        #checks to see if there's an entry for the language, and if isn't, defaults to english
        if key in self.text:
            if self.language in self.text[key]:
                return self.text[key][self.language]
            else:
                return self.text[key]['eng']
        else:
            return key
        
    def is_int(self,val):
        try:
            int(val)
            return True
        except:
            return False
        