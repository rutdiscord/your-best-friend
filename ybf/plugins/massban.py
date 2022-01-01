import disnake
from shlex import split

async def command(client, message, command):
    if message.author.id != 88401933936640000 and \
      client.stored_roles[message.guild.id]['staff'] not in message.author.roles:
        return

    ban_reason = "Mass Ban: No reason provided."
    bans = split(command)
    bans.pop(0)
    
    try:
        int(bans[0])
    except ValueError:
        ban_reason = bans.pop(0)
    
    ban_reason = f'[Ban by {message.author.name}#{message.author.discriminator}] {ban_reason}'

    banamt = len(bans)

    msg = await message.reply(
        content=f'Banning {banamt} users...',
        mention_author=False
    )

    for i,dumb in enumerate(bans):
        try:
            await message.guild.ban(
                disnake.Object(id=int(dumb)),
                reason=ban_reason
            )
            await msg.edit(
                content=f'Banned <@{dumb}> from the server.\n\n{banamt - i+1} bans remaining...'
            )
        except disnake.HTTPException:
            await msg.edit(
                content=f'Couldn\'t ban <@{dumb}> from the server. (Are they already banned?)\n\n{banamt - i+1} bans remaining...'
            )
    
    await msg.edit(
        content='All users banned.'
    )

aliases = [
    'ban',
    'massban'
]
