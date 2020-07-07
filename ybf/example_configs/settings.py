# Provide the message ID for your announcement channel here.
announcement_channels = [000000000000000000]
# Provide the User ID of your bot here (dev options: right-click, copy ID)
self = {'stable': 0000000000000}
purge = {
    'ignored_channels': [],
    'exceptions': [],
    'ignored_users': []
}
owner_id = 191872034706292737 #Replace with your User ID
guild = {  # Presently all servers YBF will operate in MUST be hardcoded.
    120330239996854274: #Server ID
    {'name': 'rundertale', 'channels': { #Internal name for server, special channel list
        'announcement': 120330239996854274,
        'bot_spam': 000000000000000000,  # Admin bot spam channel
        'roleban': 000000000000000000,  # Roleban channel ID
        'report': 000000000000000000},  # channel reports go to
        'categories': {
            # Staff channel category ID (used to determine if some commands should be allowed)
            'staff': 360563735363000000
    },
        'role_ids': [
            ['staff', 244328249801000000],
            ['rolebanned', 122150407806000000]
    ]
    }
}

invokers = ['f!', 'flowey!']

# Messages to auto-repin when a pin happens in a given channel.
pin_channels = {
    324642291044057099: [
        324643159818764308,
        325056031480872960
    ],
    524161173659189268: [
        524161625356501013
    ]
}
