import inspect
import discord

from ..configs import settings

async def command(client, message, command):
    if message.author.id != settings.self['owner_id']:
        return await message.reply(
            embed=client.embed_builder(
                'error',
                'You do not have permission to perform debug operations.'
            ),
            allowed_mentions=discord.AllowedMentions(replied_user=False)
        )

    output = eval(command.split(None, 1)[1])

    if inspect.isawaitable(output):
        output = await output

    await message.reply(
        embed=client.embed_builder(
            'default',
            f'```py\n{output}```',
            title='Output:'
        ),
        allowed_mentions=discord.AllowedMentions(replied_user=False)
    )

aliases = [
    'debug',
    'do'
]
