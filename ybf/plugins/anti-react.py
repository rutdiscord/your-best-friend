import datetime
from asyncio import sleep

reactions = {
    
}

warned = []

async def react(client, payload):
    token = f'{payload.message_id}|{payload.user_id}'
    now = datetime.now(tz=message.created_at.tzinfo)
    reactions[token] = now
    await sleep(5)
    if token in reactions:
        del reactions[token]

async def reactRemove(client, payload):
    if (
        payload.guild_id not in settings.guild or # guild not found (DM?)
        payload.message_id not in reactions
    ):
        return

    now = datetime.now(tz=message.created_at.tzinfo)

    token = '{payload.message_id}|{payload.user_id}'

    delta = now - reactions[token] # just to make sure we don't bug out

    channel = await client.get_channel(payload.channel_id)
    staff_id = client.stored_roles[channel.guild.id]['staff']

    if delta > 3:
        if payload.user_id not in warned:
            warned.append(payload.user_id)
            await channel.send(
                content=f'***WARNING:*** <@{payload.user_id}> has triggered '
                         'reaction quickdelete.\n'
                         'Please allow a 3 second breadth between reactions.\n'
                         '*You will be automatically muted on the second '
                         'infraction.*\n'
                        f'<@{staff_id}>'
                )
        else:
            member = await channel.guild.get_member(payload.user_id)
            await member.edit(
                roles=[
                    client.stored_roles[channel.guild.id]['rolebanned']
                ]
            )
            await channel.send(f'<@{payload.user_id} has been rolebanned for '
                                'multiple reaction quick-deletes.'
                               f'<@{staff_id}>')