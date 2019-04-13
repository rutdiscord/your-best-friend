from random import choice

from ybf.configs import settings

async def command(client, message, command):
    if message.author.id == settings.self['owner_id']:
        await message.channel.send(
            embed=client.embed_builder(
                'error',
                choice([
                    'I don\'t die THAT easily!',
                    'I can help... I can help... Please don\'t kill me...',
                    'You might *think* I\'m dead...',
                    '* Retreats into soil *'
                    ]),
                title=None))
        return await client.logout()
    return await message.channel.send(
        embed=client.embed_builder(
            'error',
            'You do not have permission to shut down this bot.'))

aliases = [
    'shutdown',
    'exit',
    'die'
]
