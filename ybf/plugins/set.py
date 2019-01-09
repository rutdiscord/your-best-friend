import shlex

from ..configs import settings

import discord

plus = (
    '+',
    'add',
    'new',
    'plus'
)

minus = (
    '-',
    'remove',
    'delete',
    'del'
)

settings_items = {
    'announcement_channels',
    'self',
    'guild',
    'pin_channels',
    'invokers',
    'purge'
}

export = False

def export_it():
    globals()["export"] = True

async def finisher(destination, content, type='error', title='Error'):
    color = discord.Color(0xFF0000)

    if type == 'default':
        color = discord.Color(0xBF4DFF)

    # i didn't wanna type this footer every time
    return await destination.send(
        embed=discord.Embed(
            description=content,
            title=title,
            color=color
        ).set_footer(
            text='These commands are rarely checked for consistency. Take care '
            'when modifying these settings.'
        )
    )

async def command(client, message, command):
    if client.stored_roles[message.guild.id]['staff'] not in message.author.roles:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'You are not allowed to modify settings.'
            )
        )

    context = shlex.split(command)
    context.pop(0) # get rid of "set"

    if len(context) == 0:
        # just set
        return await finisher(
            message.channel,
            str(settings_items),
            type='default',
            title='Available Settings'
        )

    if context[0] not in settings_items:
        # couldnt find that setting
        return await finisher(
            message.channel,
            f'{context[0]} is not an available setting.\n'
            'Simply type `set` to see all available options.'
        )

    thing_to_check = getattr(settings, context[0])

    while context:
        name_of_thing_to_check = context[0]
        context.pop(0)
        if len(context) == 0:
            # if we're at the end print a list or value
            if isinstance(thing_to_check, str) or isinstance(thing_to_check, int):
                return await finisher(
                    message.channel,
                    str(thing_to_check),
                    type='default',
                    title=f'Current setting for {name_of_thing_to_check}'
                )
            return await finisher(
                message.channel,
                str(list(thing_to_check)),
                type='default',
                title=f'Available Settings for {name_of_thing_to_check}'
            )

        if isinstance(thing_to_check, dict):
            # try to cast response to whatever that dictionary expects.
            context[0] = type(list(thing_to_check)[0])(context[0])

            if context[0] not in thing_to_check:
                return await finisher(
                    message.channel,
                    f'Couldn\'t find `{context[0]}` in `{name_of_thing_to_check}`.\n'
                    '\nAdding additional items to dictionaries is not supported yet.'
                )
                # im going to hope i dont need to add shit to dictionaries yet

            # is it settable?
            if (
                isinstance(thing_to_check[context[0]], int) or
                isinstance(thing_to_check[context[0]], str)
            ):
                # try setting it
                try:
                    thing_to_check[context[0]] = context[1]
                    export_it()
                    return await finisher(
                        message.channel,
                        f'Successfully changed `{name_of_thing_to_check}`\'s `{context[0]}` to `{context[1]}`',
                        type='default',
                        title='Success'
                    )
                except IndexError:
                    # no context[1]? just move on to set it as thingtocheck
                    pass

            thing_to_check = thing_to_check[context[0]]

        elif isinstance(thing_to_check, list):
            # lists are almost always the bottom-most item in our stack so we
            # don't need to "crawl up" anymore once we hit one
            try:
                if isinstance(thing_to_check[0], list):
                    # the only exception: role_ids are lists of two items because
                    # it lets me do a lazier check on boot
                    # This could probably be more modular but fuck it

                    # make sure item is formatted as a list
                    if not (
                        context[1].startswith('[') and
                        context[1].endswith(']')
                    ):
                        return await finisher(
                            message.channel,
                            f'`{name_of_thing_to_check}` needs to be formatted '
                            'like a list (ex: `["one", 2]`).'
                        )

                    # shlex to get a list, removing the braces
                    split_string = shlex.shlex(context[1][1:-1])
                    split_string.whitespace += ','
                    split_string.whitespace_split = True
                    # i could probably figure out how to get this to work with
                    # punctuation_chars but fuck it

                    context[1] = list(split_string)
                    # This does mean you'll need to do something like this:
                    # `set guild 12345 role_ids remove "['staff', 12345]"` or
                    # `set guild 12345 role_ids remove "[\"staff\", 12345]"`

                    if len(context[1]) != 2: # too many cooks!
                        return await finisher(
                            message.channel,
                            f'`{name_of_thing_to_check}` requires a two-object list.'
                        )

                # try to cast input to whatever the list expects
                # this probably won't break
                context[0] = type(thing_to_check[0])(context[0])
                if context[0] in plus:
                    thing_to_check.append(context[1])
                    export_it()
                    return await finisher(
                        message.channel,
                        f'Successfully added that to the list `{name_of_thing_to_check}`',
                        type='default',
                        title='Success'
                    )
                if context[0] in minus:
                    thing_to_check.remove(context[1])
                    export_it()
                    return await finisher(
                        message.channel,
                        f'Successfully removed that from the list `{name_of_thing_to_check}`',
                        type='default',
                        title='Success'
                    )
            except IndexError:
                # context[0] exists but context[1] doesn't
                return await finisher(
                    message.channel,
                    'You did not specify something to add or remove from the list'
                )
            except ValueError as e:
                if str(e).startswith('ValueError: invalid literal'):
                    # tried to put a string in a list of ints
                    return await finisher(
                        message.channel,
                        'Couldn\'t convert your input to an integer. Maybe you mispelled it?'
                    )

                # tried to remove something that wasn't there
                return await finisher(
                    message.channel,
                    f'Couldn\'t find that item in `{name_of_thing_to_check}`'
                )

            # didn't say add or remove (we fell through the try)
            return await finisher(
                message.channel,
                'When editing a list, specify whether you are `add`ing or '
                '`delete`ing an item before the item in question.\n\n'
                'Example: `set invokers remove r!`'
            )

    return await finisher(
        message.channel,
        'An unexpected error occurred.`'
    )

async def close(client):
    if export:
        # write new options file
        x = ''
        for item in settings_items:
            x += '{} = {}\n\n'.format(
                item,
                getattr(settings, item)
            )
        with open('./ybf/configs/settings.py', 'w') as config:
            config.write(x)

aliases = ['set']
