'''
option_data_storage
-option_id
-option_skill/stat
-option_item None or ItemName
-option_difficulty
-option_success_cost ((stat_key,-int,False),) #may have multiples. If True, is an item.
-option_fail_cost ((stat_key,-int,False),) #may have multiples. If True, is an item.
-stat/skill/item_req: if not None: required second stat (Not attribute), and target.

Option blurbs stored in text_blurbs.py as id+menu, id+success, and id+fail.


option skeleton = {
    'option_id': {
        'attribute': 'shoot',
        'item': None,
        'difficulty': 1,
        'suc_cost': (('stat',-1),),
        'suc_item': ('item',-1),
        'fail_cost': (('stat',-2),('stat',-1),),
        'fail_item': ('item',-1),
        'requirement': (type,key, value),
        'requirement': None,
    },
}

option example = {
    'sh1': {
        'attribute': 'shoot',
        'item': None,
        'difficulty': 1,
        'suc_cost': (('stamina',-1),),
        'suc_item': None,
        'fail_cost': (('stamina',-2),('stress',-1),),
        'fail_item': None,
        'requirement': ('skill','sneak',2),
    },
}
For the example, the blurb_ids would be sh1menu, sh1success, and sh1fail

'''
option_list = {
    'sh1': {
        'attribute': 'shoot',
        'item': None,
        'difficulty': 1,
        'suc_cost': None,
        'suc_item': None,
        'fail_cost': (('health',-1),('stress',-1),),
        'fail_item': None,
        'requirement': None,
        
    },
    'sn1': {
        'attribute': 'sneak',
        'item': None,
        'difficulty': 1,
        'suc_cost': None,
        'suc_item': None,
        'fail_cost': (('stress',-2),('stamina',-1),),
        'fail_item': None,
        'requirement': None,
    },
    'me1': {
        'attribute': 'mechanics',
        'item': None,
        'difficulty': 1,
        'suc_cost': (('stamina',-1),),
        'suc_item': None,
        'fail_cost': (('stamina',-1),('stress',-1),),
        'fail_item': None,
        'requirement': None,
    },
    'st1': {
        'attribute': 'stamina',
        'item': None,
        'difficulty': 1,
        'suc_cost': (('stamina',-1),),
        'suc_item': None,
        'fail_cost': (('stamina',-2),),
        'fail_item': None,
        'requirement': None,
    },
    'it1': {
        'attribute': 'item',
        'item': 'Flashbang',
        'difficulty': 1,
        'suc_cost': None,
        'suc_item': ('Flashbang',1),
        'fail_cost': (('stress',-2),),
        'fail_item': ('Flashbang',1),
        'requirement': None,
    },
}