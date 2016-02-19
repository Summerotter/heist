#disassemble event manager, have each class have their own? 

class EventManager:
    def __init__(self,game):
        '''job table here temporarily. Will be moved to seperate events file at some point.'''
        '''then it would be self.job_event_table = imported thing from other file'''
        prefix = "event_"
        from events import bar,job
        
        self.job_event_table = job
        self.job_keys = list(self.job_event_table.keys())
        
        self.bar_event_table = bar
        self.bar_keys = list(self.bar_event_table.keys())
        
    def bar_event(self,game):
        '''bar event handler, 15-20 on d20 for event'''
        if game.randint(1,20) < 15:
            game.bar.event_interrupt = False
            return None
            
        event_key = self.bar_keys[game.randint(0,len(self.bar_keys)-1)]
        event = self.bar_event_table[event_key]   
        game.bar.event_interrupt = event['interrupt']
        print(game.config.get_text(event_key))
        #gets an event from the table, checks if it's an interrupt business event, prints event text, then handles based on event type
        
        if event['type'] == 'beer':
            game.bar.new_beer(event['value'])
        if event['type'] == 'cash':
            if game.character.cash_on_hand + event['value'] < 0:
                game.character.cash_on_hand = 0
            else:
                game.character.cash_on_hand += event['value']
        if event['type'] == 'stat':
            game.character.change_current_stat(event['key'],event['value'])
        
        
    
    def job_event(self,game):
        event_key = self.job_keys[game.randint(0,len(self.job_keys)-1)]
        event = self.job_event_table[event_key]
        #might actually be useful for a case|switch, value of lambdas, since everything is sorta standardized up to the impact.
        if event['type'] == 'skill_up':
            game.character.raise_skill_event(event['key'])
        if event['type'] == 'stat_mod_per_hour':
            game.job.modified_per_hour_stat_cost[event['key']] += event['value']
        if event['type'] == 'pay_mod':
            game.job.modified_pay += event['value']
        if event['type'] == 'time_mod':
            game.job.modified_hours += event['value']
        game.job.event_string = game.config.get_text(event_key)