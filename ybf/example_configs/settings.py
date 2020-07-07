# Provide the message ID for your announcement channel here.
# Messages posted in this channel will be reported in the respective server's announcement channel
announcement_channels = [000000000000000000]

# Options relating to the bot itself
self = {
    'stable': 0000000000000, # Provide the User ID of your bot here (dev options: right-click, copy ID)
    'owner_id': 191872034706292737 #Replace with your User ID
}

# Delete Police options
purge = {
    'ignored_channels': [], # Channel IDs in this list will be ignored by delete police
    'ignored_users': [], # User IDs in this list will be ignored by delete police
    # Normally, you do not need to modify those two options, as they are manipulated by YBF when a user is banned to ignore them for delete police.
    # You can, however, include things like your admin bot spam channel.
    'exceptions': ['f!report'] # Provide a list of strings. Any messages beginning with these strings will be ignored by delete police.
}

# Options relating to your server(s)
guild = {  # Presently all servers YBF will operate in MUST be hardcoded.
    120330239996854274 : { #Place your Server ID here
        'name': 'rundertale', # Internal name for server (so you can recognize it in f!set)
        'channels': {
            'announcement': 120330239996854274, # When an announcement is made, this is the ID of the channel that will recieve a notification about the announcement.
            'bot_spam': 000000000000000000,     # Admin bot spam channel ID
            'roleban': 000000000000000000,      # Roleban channel ID
            'report': 000000000000000000        # Where reports from f!report will go
        },
        'categories': {
                # Staff channel category ID (used to determine if some commands should be allowed)
                'staff': 360563735363000000
        },
        'role_ids': [
            ['staff', 244328249801000000], # ID of the role for people on your staff (you might need a bot to get this)
            ['rolebanned', 122150407806000000] # ID of the role for people currently rolebanned (all bot commands from people with this role will be ignored.)
        ]
    }
}

# Invokers determine what text must be typed before a command.
# i.e. an invoker of "f!" means commands must be written like "f!help"
invokers = ['f!', 'flowey!']

# Options for automatic re-pinning
pin_channels = {
    324642291044057099: [ # when a message is sent in a channel with this ID...
        324643159818764308, # ...find and re-pin a message with this ID in that channel.
        325056031480872960
    ],
    524161173659189268: [
        524161625356501013
    ]
}
# re-pinned messages will always be at the top of the pinned messages, making them
# useful for rules posts and important posts.

# Warning: if you use f!set at any time, or any of these options are updated
# by another YBF command, all of these comments will be deleted.
