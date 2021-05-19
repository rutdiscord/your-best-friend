import inspect

from ..configs import settings

async def command(client, message, command):
    if message.author.id != settings.self['owner_id']:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'You do not have permission to perform debug operations.'
            )
        )

    output = eval(command.split(None, 1)[1])

    if inspect.isawaitable(output):
        output = await output

    await message.channel.send(
        embed=client.embed_builder(
            'default',
            f'```py\n{output}```',
            title='Output:'
        )
    )

aliases = [
    'debug',
    'do'
]
