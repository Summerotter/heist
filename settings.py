class GameConfiguration:
    def __init__(self):
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
        
        from text_blurbs import text
        self.text = text
        
    def get_text(self, key):
        #Used to better handle multilanguage
        if key in self.text:
            return self.text[key][self.language]
        else:
            return key
        