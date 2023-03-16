import disnake
import typing
from ybf.configs import settings


async def command(client: disnake.Client, message: disnake.Message, _):
    """
    Inverts everyone write permissions for a channel if a given user is staff.
    If your mod bots don't have your staff role set the "mod_bot" server role key in settings.py
    """
    try:
        safe_assert(type(message.guild) == disnake.guild.Guild)
        safe_assert(type(message.author) == disnake.Member)
    except:
        return await message.channel.send("Unable to identify caller/You tried to use this in a DM.")

    # (Asserted above)
    caller = typing.cast(disnake.Member, message.author)
    msg_guild = typing.cast(disnake.guild.Guild, message.guild)

    # (Client is mutated)
    server_roles = client.stored_roles[message.guild.id]  # type:ignore

    staff = server_roles['staff']
    if staff not in caller.roles:
        return  # No response if not staff

    if not type(message.channel) == disnake.TextChannel:
        return await message.channel.send("I can't lock down this channel type.")

    # (Asserted above)
    msg_channel: disnake.TextChannel = message.channel  # type: ignore

    everyone = msg_guild.default_role
    permissions = message.channel.permissions_for(everyone)
    await msg_channel.set_permissions(
        everyone,
        send_messages=not permissions.send_messages)
    await msg_channel.set_permissions(
        staff,
        send_messages=True)  # Staff can always talk
    if 'mod_bots' in server_roles:
        await msg_channel.set_permissions(
            server_roles['mod_bots'],
            send_messages=True)  # Mod bots can always talk
    return await message.channel.send(f"{'Un-' if not permissions.send_messages else ''}Lockdowned channel.")
aliases = ["lockdown"]

def safe_assert(expr: bool):
    '''
        https://snyk.io/blog/the-dangers-of-assert-in-python/
    '''
    if expr == False:
        raise AssertionError("Assertion failed.")