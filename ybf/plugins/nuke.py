import re
import shlex
import discord
import asyncio

from ..configs import settings

class ParameterException(Exception):
    '''Raise this when a parameter fails in nuke.'''
    pass

def membercheck(client, message, context, data):
    member = None
    # find by mention
    mention = re.match(r'\<\@\!?([0-9]+?)\>', context[1])
    # find by ID
    user_id = re.match(r'[0-9]+', context[1])

    if mention:
        member = message.guild.get_member(mention.group(1))

    elif user_id:
        member = message.guild.get_member(user_id.group(0))

    else:
        member = message.guild.get_member_named(context[1])

    # couldnt find any member with that id or name
    if member is None:
        raise ParameterException(
            'No member found with given ID, name, or name/discriminator combo.'
        )

    # add that member to the list
    data['member'].append(member)

    # delete "member <whatever>" from the context list
    del context[:2]

def channelcheck(client, message, context, data):
    # basically the same as the above
    channel = None
    mention = re.match(r'\<\#([0-9]+?)\>', context[1])
    channel_id = re.match(r'[0-9]+', context[1])

    if mention:
        channel = message.guild.get_channel(mention.group(1))
    elif channel_id:
        channel = message.guild.get_channel(id.group(0))
    else:
        channel = discord.utils.find(
            lambda x: x.name == context[1],
            message.guild.text_channels
        )

    if channel is None:
        raise ParameterException('No channel found with given ID or mention.')

    del context[:2]

    data['channel'] = channel

def contentcheck(client, message, context, data):
    data['content'].append(context[1].lower())
    del context[:2]
    # easy peasy pizzaaaa cheesy

def regexcheck(client, message, context, data):
    try:
        data['regex'].append(re.compile(context[1]))
        del context[:2]
    except re.error as error:
        raise ParameterException(
            'Unable to compile regex.\n'
            '```fix\n' + str(error) + '\n```'
        )

def switch_this_parameter_on(client, message, context, data):
    # correct aliases
    if context[0] == 'bot': context[0] = 'bots'
    if context[0] == 'embeds': context[0] = 'embed'

    if data[context[0]] == True:
        data[context[0]] == False
    else:
        data[context[0]] = True
    # that should cover all the switches

    context.pop(0)

valid_commands = {
    'in' : channelcheck,
    'channel' : channelcheck,
    'from' : membercheck,
    'member' : membercheck,
    'with' : contentcheck,
    'regex' : regexcheck,
    'embed' : switch_this_parameter_on,
    'embeds' : switch_this_parameter_on,
    'system' : switch_this_parameter_on,
    'bots' : switch_this_parameter_on,
    'bot' : switch_this_parameter_on,
    # 'reactions' : reactioncheck,
    'matchall' : switch_this_parameter_on
}

# def reactioncheck(client, message, context, data):
#     for emoji in context[1]:
#         data['reactions'].append(
# I'll finish this when i want to sift through differentiating between
# custom emoji and regular ones

async def delete_from(client, context, data):
    # can't delete messages in private channels
    if isinstance(data['channel'], discord.abc.PrivateChannel):
        return await context.channel.send(
            embed=client.embed_builder(
                'error',
                'Deleting messages from private channels is '
                'unavailable. (Discord does not allow us to use the "purge" '
                'backend in private channels.)'
            )
        )

    # you or me can't delete messages there
    if (
      not data['channel'].permissions_for(context.author).manage_messages or
      not data['channel'].permissions_for(context.guild.me).manage_messages
    ):
        return await context.channel.send(
            embed=client.embed_builder(
                'error',
                'You or I do not have permission to delete messages in the targeted '
                'channel.'
            )
        )

    # don't delete that many messages
    if data['amount'] > 10001:
        return await context.channel.send(
            embed=client.embed_builder(
                'error',
                'I cannot delete more than 9999 messages at a time.'
            )
        )

    # delete invocation too
    if data['channel'] == context.channel:
        data['amount'] += 1

    def check(msg):
        # please help me make this concise i am bad at codery

        # When Matchall is on, a message will only trigger if every parameter
        # listed is found in the message
        # ex: `with garbage embed` will catch messages with the word "Garbage"
        # and any messages with images. `with garbage embed matchall` will only
        # catch messages that have images with text that include the word
        # "Garbage".

        for member in data['members']:
            if data['matchall']:
                if msg.author != member:
                    return False
            elif msg.author == member: return True

        for phrase in data['content']:
            result = (
                phrase.lower() in msg.content.lower() or
                phrase.lower() in msg.clean_content.lower()
            )
            if data['matchall']:
                if not result:
                    return False
            elif result:
                return True

        for pattern in data['regex']:
            patternA = pattern.search(msg.content.lower())
            patternB = pattern.search(msg.clean_content.lower())

            if data['matchall']:
                if not (patternA or patternB):
                    return False
            elif (patternA or patternB):
                return True

        # this should work fine but i don't catch reactions yet so i don't
        # wanna waste cycles checking empty lists

        # for emoji in data['reactions']:
        #     for reaction in message.reactions:
        #         if data['matchall']:
        #             if reaction.emoji != emoji:
        #                 return False
        #         else:
        #             if reaction.emoji == emoji:
        #                 return True

        if data['embed']:
            result = (msg.embeds or msg.attachments)
            if data['matchall']:
                if not result:
                    return False
            elif result:
                return True

        if data['system']:
            if data['matchall']:
                if msg.type == discord.MessageType.default:
                    return False
            elif msg.type != discord.MessageType.default:
                return True

        if data['bots']:
            if data['matchall']:
                if not msg.author.bot:
                    return False

                for prefix in data['prefixes']:
                    content = msg.clean_content.lower()

                    if content.startswith(('[', '{')) and \
                    content.endswith((']', '}')):
                        content = content[1:-1]

                    if msg.startswith(prefix.lower()):
                        return True
            else:
                if msg.author.bot:
                    return True

                for prefix in data['prefixes']:
                    content = msg.clean_content.lower()

                    if (
                        content.startswith(('[', '{')) and
                        content.endswith((']', '}'))
                    ):
                        content = content[1:-1]

                    if not msg.startswith(prefix.lower()):
                        return False

        if data['matchall']: return True
        return False

    settings.purge['ignored_channels'].append(data['channel'].id)

    # await context.delete();

    purged = await data['channel'].purge(limit=data['amount'], check=check)

    await context.channel.send(
        embed=discord.Embed(
            description='*Deleted {} messages.*'.format(len(purged)),
            title='Purge completed.',
            color=discord.Color(0xBF4DFF)
        ).set_footer(text='This message will delete itself in 5 seconds.'),
        delete_after=5
    )

    await asyncio.sleep(1)
    settings.purge['ignored_channels'].remove(data['channel'].id)

async def command(client, message, command):
    # defaults
    data = {
        'amount' : 100,
        'members' : [],
        'channel' : message.channel,
        'content' : [],
        'regex' : [],
        'embed' : False,
        'system' : False,
        'bots' : False,
        'prefixes' : [],
        # 'reactions' : [],
        'matchall' : True
    }

    context = shlex.split(command)

    if len(context) == 1: # just purge
        return await delete_from(client, message, data)

    context.pop(0) # remove "nuke"

    while context: # as long as there are still parameters
        if (
            context[0] not in valid_commands and # not a command
            re.match(r'[0-9]*',context[0]).group(0) != context[0] # not a number
        ):
            return await context.channel.send(
                embed=client.embed_builder(
                    'error',
                    f'Unknown option: {context[0]}')
                )

        try:
            # next item in the context is an option
            if context[0].lower() in valid_commands:
                valid_commands[context[0].lower()](
                    client,
                    message,
                    context,
                    data)
            else: # next item in the context is a number
                data['amount'] = int(context[0])
                context.pop(0)
            # Commands are responsible for popping their results from the
            # context list.
            # That's probably a bad idea but fuck it, I'm the only one writing
            # code here.

            # Except you're reading this comment right now and I'm taking the
            # time to write it.
            # Fuck.
        except IndexError:
            # this error lets checks do things like `context[1]` without
            # worrying about if it actually exists or not

            # so far it's never false-flagged so shrug
            return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    f'Option `{context[0]}` was given no parameters.'
                )
            )

        except ValueError:
            # Tried to cast a string to an int when setting amount
            return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    f'Unknown option: `{context[0]}`.'
                )
            )

        except ParameterException as e:
            # error happened, we're done here.
            return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    f'Error with option `{context[0]}`: {e}'
                )
            )

    purged = await delete_from(client, message, data)

aliases = [
    'nuke',
    'purge',
    'p',
    'n',
    '-'
]
