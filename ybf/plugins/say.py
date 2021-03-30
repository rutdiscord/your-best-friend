from re import match

from ..configs import settings

async def command(client, message, command):
    if message.author.id != 120698901236809728 and \
      message.author.id != 88401933936640000 and \
      client.stored_roles[message.guild.id]['staff'] not in message.author.roles:
        return

    if len(command.split()) <= 1:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'Nothing to say provided.'
            )
        )

    channel = message.channel

    context = command.split(None, 2)
    chreg = match(r'\<\#([0-9]+?)\>', context[1])

    if chreg:
        channel = message.guild.get_channel(int(chreg.group(1)))
        content = context[2]
    else: # Basic repeat
        content = command.split(None, 1)[1]

    await channel.send(content)
    if channel != message.channel:
        await message.channel.send(f'{message.author.display_name}: \U0001f44c')


aliases = [
    'say',
    'xsay',
    'send',
    'fakesend'
]
