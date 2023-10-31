from datetime import datetime, timedelta

async def join(client, member):
    if datetime.now(tz=member.created_at.tzinfo) - member.created_at > timedelta(days=1):
        await member.edit(roles=[client.stored_roles['antiraid']])
        if 'bot_spam' in settings.guild[member.guild.id]['channels']:
            channel = member.guild.get_channel(settings.guild[member.guild.id]['channels']['bot_spam'])
            await channel.send(f'**Added antiraid role to** <@{member.id}>.')
