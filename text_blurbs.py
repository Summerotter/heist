#pattern is key, returning a dict by language. Other stuff would have to be done as well...
'''
skeleton: 'key': {'eng': "string",},

---
Scene Skeleton: add sceneid (d1, f2, etc) to key (d1start, f2end).
        'start': {'eng':"string",},
        'success': {'eng': "string",},
        'end': {'eng': "string",},
----
Option Skeleton: add optionid (sh1, me2) to key (sh1menu, me2fail)
         'menu': {'eng': "string",},
         'success': {'eng': "string",},
         'fail': {'eng': "string",},

'''
text = { 'text_key': {'eng' : 'this is the full text, in english', 'spa' : "no hablo espanol but prebuilding for multilingual options"},

        #location descriptions, location_timeofday
         'city_morning': {'eng': "This is the city in the morning",},
         'city_afternoon': {'eng': "This is the city in the afternoon",},
         'city_evening': {'eng': "This is the city in evening.",},
         'city_night': {'eng': "This is the city at night.",},
         
         'bank_morning': {'eng': "This is the bank in the morning.",},
         'bank_afternoon': {'eng': "This is the bank in the afternoon.",},
         'bank_evening': {'eng': "This is the bank in the evening",},
         'bank_night': {'eng': "This is the bank at night.",},
         
         'store_morning': {'eng': "This is the Company Store in the morning.",},
         'store_afternoon': {'eng': "This is the Company Store in the afternoon.",},
         'store_evening': {'eng': "This is the Company Store in the evening",},
         'store_night': {'eng': "This is the Company Store at night.",},
         
         'market_morning': {'eng': "This is the Black Market in the morning.",},
         'market_afternoon': {'eng': "This is the Black Market in the afternoon.",},
         'market_evening': {'eng': "This is the Black Market in the evening",},
         'market_night': {'eng': "This is the Black Market at night.",},
         
         'bar_morning': {'eng': "This is the bar where your SO works in the morning.",},
         'bar_afternoon': {'eng': "This is the bar where your SO works in the afternoon.",},
         'bar_evening': {'eng': "This is the bar where your SO works in the evening",},
         'bar_night': {'eng': "This is the bar where your SO works at night.",},
         
         'job_morning': {'eng': "This is the workshop that employs you in the morning.",},
         'job_afternoon': {'eng': "This is the workshop that employs you in the afternoon.",},
         'job_evening': {'eng': "This is the workshop that employs you in the evening",},
         'job_night': {'eng': "This is the workshop that employs you at night.",},
         
         'home_morning': {'eng': "This is you and your SO's home in the morning.",},
         'home_afternoon': {'eng': "This is you and your SO's home in the afternoon.",},
         'home_evening': {'eng': "This is you and your SO's home in the evening",},
         'home_night': {'eng': "This is you and your SO's home at night.",},
         
         'hide_morning': {'eng': "This is your hideout in the morning.",},
         'hide_afternoon': {'eng': "This is your hideout in the afternoon.",},
         'hide_evening': {'eng': "This is your hideout in the evening",},
         'hide_night': {'eng': "This is your hideout at night.",},
         
        #new_beer, bar events
        'beer1': {'eng': "Although really, it couldn't get worse than it already is.",},
        'beer2': {'eng': "No, the beer couldn't get better - not at the prices the bar's customers can afford, at least.",},
        'beer3': {'eng': "Yeah, you can taste the difference. Your wallet does, too.",},
        #bar events
        'bar_1': {'eng': "A bar fight breaks out. You get hurt, and bar cleared out for a bit.",},
        'bar_2': {'eng': "Your SO grabs you to help wish a rush. You pocket the tips.",},
        'bar_3': {'eng': "New cheap beer up. Tastes like it, too.",},
        'bar_4': {'eng': "You've bumped into someone, and realize your pouch is lighter some money. Damn pickpocets.",},
        'bar_5': {'eng': "The new beer tastes better. The price matches, though",},
        #job events
        'job_1': {'eng': "You seemed to understand mechanics better! +1 to your skill.",},
        'job_2': {'eng': "Work was tiring today, and drained you an extra 1 stamina per hour.",},
        'job_3': {'eng': "You got shifted to doing some dangerous stuff, but it has a +$1 an hour pay bonus.",},
        'job_4': {'eng': "There was a problem with a shipment, and you were idle for an hour, which your boss says he aint paying you. -1 hours of work.",},

         
         #scene descriptions, prefix type_letter + scene_number.
         'd1start': {'eng':"You've gotten a good look at how to get into the ship you want. There's a few ways in.",},
         'd1success': {'eng': "Bingo. That did the trick, and the loot in the cargo is yours.",},
         'd1end': {'eng': "Without anything else that can be done, you leave the ship.",},
         
         'd2start': {'eng':"The portsmaster's office might have some good info.",},
         'd2success': {'eng': "Information and some good loot, too.",},
         'd2end': {'eng': "It doesn't look like you're able to get into the office, though.",},
         
         'd3start': {'eng':"Your contact said this pier is where that contraband was stashed.",},
         'd3success': {'eng': "And there it is, like your contact said it would be.",},
         'd3end': {'eng': "Not being able to get at the stash, you move on lest you get caught.",},
         
         #shoot options, prefix sh
         'sh1menu': {'eng': "With a good shot or two, the guards might become a non-factor.",},
         'sh1success': {'eng': "You can get past the guards now, since they're not in play.",},
         'sh1fail': {'eng': "The guards start firing back, and you scramble to get away.",},
         
         #stamina options, prefix st
         'st1menu': {'eng': "A few large crates seem to be blocking a side door. Perhaps they can be moved.",},
         'st1success': {'eng': "It takes some work, but the way is now clear.",},
         'st1fail': {'eng': "The boxes are just too heavy, and you're too winded to attempt something else here.",},
         
         #sneak options, prefix sn
         'sn1menu': {'eng': "The guards don't seem to be paying much attention. Maybe they'll not notice you sneak by.",},
         'sn1success': {'eng': "The guards continue paying attention elsewhere, and you've slipped past.",},
         'sn1fail': {'eng': "The guards were more attentative than you thought!",},
         
         #item options, prefix it
         'it1menu': {'eng': "You've got a flash grenade that might help here.",},
         'it1success': {'eng': "You lob the grenade. It lands between the guards, who look at it - and are promptly blinded.",},
         'it1fail': {'eng': "You mistimed the throw, and were as blinded as the guards were.",},
         
         #mechanic options, prefix me
         'me1menu': {'eng': "These valves connect to machinery all around you. Perhaps you can remotely draw the guards away.",},
         'me1success': {'eng': "You twist the last valve, and an ungodly shrieking noise erupts from another part of the ship, drawing the guards attention.",},
         'me1fail': {'eng': "You open a valve, and thick black smoke pours forth all over you.",},
         
         #heist blurbs, type+number
         'd1': {'eng': "There's a new shipment coming in. Might be worth our time."},
         'd2': {'eng': "Guards down at the docks are tense. They're hiding something good."},
         'd3': {'eng': "One of your rivals got his ticket punched. His hideout was down at the docks..."},
         
         #heist location
         'dock': {'eng': "The Dockyard",},
         #win
         'win1': {'eng': '''With the new identity papers in hand, you have arrived home with a light heart and a joy you've not felt in a long while. You see your SO standing in the kitchen, and you pounce them happily, holding them tightly. They let out a soft sound of surprise as you stand there, just holding them.''',},
         'win2': {'eng': '''Eventually your SO speaks, 'What's going on hun? Did something happen?" You just nod, and show them the papers. They stand there speechless. "I managed to buy these," you say. "And they're pretty legitimate. You, me. A new life away from here. We'd still have to work, but... not here. Just us."''',},
         'win3': {'eng': '''Your SO nods, and you hold each other tightly again.''',},
         'win4': {'eng': '''It is here that you lived, and here that you fell in love. It is here that you thought you would end your days, but now one of those very airships you once labored to fix just to stay afload is now taking you away. To a better life. ''',},
         'win5': {'eng': '''             The End''',},
         'win6': {'eng': '''             Thank you for playing.''',},
         
         #intro
         'intro1': {'eng': '''This is the Capitol of the Empire. Tall towers stand arrogantly, reaching for the clear sky, a thick miasmic cloud at their base, the noxious fumes of the industry that powers the wealth, opulance, and decadance of the upper class choking those that support them. The great towers and builds abound with airdocks, and the great zepplines and airships criss-cross through the air.''',},
         'intro2': {'eng': '''It is here that you live, and is here that you know you will end your days, laboring in an Imperial airship repair shop, earning just enough in your 60 hours of work a week to pay your bills, dreaming without hope of a life in a better place. ''',},
         'intro3': {'eng': '''But a curious event has happened that will change your destiny: You have fallen in love, and they have fallen in love with you as well. Your SO also has dreams of living life in a beter place, but earns not much more than you do working as a bartender - although with you, they say they have found a better place.''',},
         'intro4': {'eng': '''But you want better for your SO - better for both of you. And so, taking up a dangerous offer, you have begun practicing with your guns, improving your enginering, and developing your sneaking. There's wealth out there for the taking, young SteamRunner, and with it a better future for you both.''',},
         'title': {'eng': "SteamRunner",},
         'title2': {'eng': "Designed and Developed by Henry J. Thiel",},
         
}
        