from re import match

async def command(client, message, command):
    search_string = None

    try:
        search_string = command.split(None, 1)[1]
    except IndexError:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'Not enough parameters: Provide a name or mention to get the '
                'user\'s ID.'
            )
        )

    member = None

    mention = match(r'\<\@\!?([0-9]+?)\>', message.content.split(None, 1)[1])

    if mention:
        member = message.guild.get_member(mention.group(1))

    else:
        member = message.guild.get_member_named(search_string)

    if member is None:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'No member found with given mention, name, or '
                'name/discriminator combo.'
            )
        )

    return await message.channel.send(
        member.id,
        embed=client.embed_builder(
            'default',
            f'ID Displayed for user {member.name}',
            title='ID Found'
        ).set_footer(
            text='If this is not the right user, check to make sure '
                 'you provided the correct discriminator.',
            icon_url=member.avatar_url
        )
    )

aliases = [
    'getid',
    'id',
    'who',
    'whois'
]
