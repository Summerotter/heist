'''
items.py
contains two dictionaries; white and black.
Company Store uses the entire white list.
Black Market uses some of the white, and some of the black randomly, determined by randint and market.refresh.
 '''
 
white = { 
    'health1': {'qty':3,'cost':5,'sell':2,'type':"rest",'attr':'health','value':2,'key':'health1',},
    'health2': {'qty':2,'cost':9,'sell':2,'type':"rest",'attr':'health','value':3,'key':'health2',},
    'health3': {'qty':1,'cost':14,'sell':2,'type':"rest",'attr':'health','value':4,'key':'health3',},
    'stress1': {'qty':3,'cost':5,'sell':2,'type':"rest",'attr':'stress','value':2,'key':'stress1',},
    'stress2': {'qty':2,'cost':9,'sell':2,'type':"rest",'attr':'stress','value':3,'key':'stress2',},
    'stress3': {'qty':1,'cost':14,'sell':2,'type':"rest",'attr':'stress','value':4,'key':'stress3',},
    'stamina1': {'qty':3,'cost':5,'sell':2,'type':"rest",'attr':'stamina','value':2,'key':'stamina1',},
    'stamina2': {'qty':2,'cost':9,'sell':2,'type':"rest",'attr':'stamina','value':3,'key':'stamina2',},
    'stamina3': {'qty':1,'cost':14,'sell':2,'type':"rest",'attr':'stamina','value':4,'key':'stamina3',},
}

black = {
    'tool0':{'qty':0,'cost':0,'sell':2,'type':"equip",'attr':'mechanics','value':0,'key':'tool0',},
    'tool1': {'qty':1,'cost':500,'sell':2,'type':"equip",'attr':'mechanics','value':1,'key':'tool1',},
    'tool2': {'qty':1,'cost':1200,'sell':2,'type':"equip",'attr':'mechanics','value':2,'key':'tool2',},
    'gun0':{'qty':0,'cost':0,'sell':2,'type':"equip",'attr':'shoot','value':0,'key':'gun0',},
    'gun1': {'qty':1,'cost':500,'sell':2,'type':"equip",'attr':'shoot','value':1,'key':'gun1',},
    'gun2': {'qty':1,'cost':1200,'sell':2,'type':"equip",'attr':'shoot','value':2,'key':'gun2',},
    'cloth0':{'qty':0,'cost':0,'sell':2,'type':"equip",'attr':'sneak','value':0,'key':'cloth0',},
    'cloth1': {'qty':1,'cost':500,'sell':2,'type':"equip",'attr':'sneak','value':1,'key':'cloth1',},
    'cloth2': {'qty':1,'cost':1200,'sell':2,'type':"equip",'attr':'sneak','value':2,'key':'cloth2',},
    'flashbang': {'qty':1,'cost':20,'sell':2,'type':"flashbang",'attr':None,'value':5,'key':'flashbang',},
}