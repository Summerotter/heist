
'''
scene_storage_example = {
    'type': {
        'blurbs': 4,
        'scene_id': {
            'start': 'scene_id_start_text_key',
            'success': 'scene_id_succes_text_key',
            'end': 'scene_id_end_text_key',
            'options': {'shoot': [optkey,optkey,],'sneak': [optkey,optkey,],'mechanics': [optkey,optkey,], 'stamina': [optkey,optkey,], 'item': [optkey,]},
        },
    },
}

'type' refers to the heist types, mainly to keep dock or warehouse scenes from popping up when raiding an airship.
'scene_id' is the type prefix ('d' for docks) and a number, usually in order of creation. The first dock scene is thus 'd1'
'blurbs moved to generation, will be in text_blurbs.py as d1start, dsuccess, d1end
'options is another dict. keys are skills, stamina, and item. Results are a list of option_keys for the option_data_storage.
Options are //not// scence specific.
If item is none, does not get displayed.

'''

scene_data_list = {
    'dock': {
        'd1': {
            'options': {'shoot': ["sh1",],'sneak': ["sn1",],'mechanics': ["me1",], 'stamina': ['st1',], 'item': ['it1',]},
        },
        'd2': {
            'options': {'shoot': ["sh1",],'sneak': ["sn1",],'mechanics': ["me1",], 'stamina': ['st1',], 'item': ['it1',]},
        },
        'd3': {
            'options': {'shoot': ["sh1",],'sneak': ["sn1",],'mechanics': ["me1",], 'stamina': ['st1',], 'item': ['it1',]},
        },
    },
}

scene_type_list = {'dock': ('d',3),}
'''key, id_prefix, number of blurbs'''