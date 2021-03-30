from ..configs import settings

import discord
import asyncio
import json

reports = {}

export = False

valid_mojis = (
    '\U0001F4DD', # :memo: / :pencil:
    '\u21A9',     # :leftwards_arrow_with_hook:
    '\u270D',     # :writing_hand:
    '\U0001F4E7', # :e_mail:
    '\U0001F4AC', # :speech_balloon:
    '\U0001F5E8', # :speech_left:
    '\U0001F441\u200D\U0001F5E8' # :eye_in_speech_bubble: / :eye_am_a_witness:
)

async def ready(client):
    try:
        with open('./ybf/configs/reports.json', encoding='utf-8') as data:
            globals()['reports'] = json.load(data)

    except FileNotFoundError:
        print('Ignoring JSON: file wasn\'t found')
        # export = True

    except json.decoder.JSONDecodeError:
        print('Ignoring JSON: Corrupt or empty file was loaded.')

async def command(client, message, command):
    message_deleted = False

    if not isinstance(message.channel, discord.abc.PrivateChannel):
        msg = None

        try:
            settings.purge['ignored_channels'].append(message.channel.id)
            await message.delete()
            message_deleted = True
        except discord.Forbidden:
            msg = 'Unable to delete your message. Anonymity is not guaranteed.'
        except discord.NotFound:
            msg = 'Unable to find your message. Anonymity is not guaranteed.'

        if msg:
            await message.channel.send(
                embed=client.embed_builder(
                    'warning',
                    msg,
                    title='Warning'
                )
            )

    if message_deleted:
        settings.purge['ignored_channels'].remove(message.channel.id)

    context = command.split(None, 1)
    if len(context) < 2:
        try:
            await message.author.send(
                embed=client.embed_builder(
                    'error',
                    'You must provide something to report.'
                )
            )
        except discord.Forbidden:
            # We are blocked or the user has DMs closed.
            await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    'Nothing was sent to report.'
                )
            )
        return

    current_guild = None
    for guild in settings.guild.keys():
        # check if report channel exists
        if settings.guild[guild]['channels']['report'] != 0:
            this_guild = client.get_guild(guild)
            # make sure I'm in the guild and so are they
            this_member = await this_guild.fetch_member(message.author.id)
            if this_guild and this_member:
                # assume first guild I share with this user is the correct one
                current_guild = this_guild
                # pretty sure keys() goes in order so rundertale should be first
                break

    if not current_guild:
        raise Exception('Guild Not Found')
        # This shouldn't happen.

    report_id = None

    if message_deleted and len(message.attachments) > 0:
        # message was sent in a public channel and was instantly deleted, so
        # the images are now gone
        await message.author.send(
            embed=discord.Embed(
                color=client.colors['warning'],
                title='Please Re-Send Attachments',
                description='**Your report has not been sent yet.**\n'
                            'Your message included attachments that were '
                            'deleted alongside it. Please reupload the '
                            'attachment to this channel.'
            )
        )
        def check(m):
            return (
                isinstance(m.channel, discord.abc.PrivateChannel) and
                m.author.id == message.author.id and
                len(m.attachments) > 0
            )

        newmsg = await client.wait_for('message', check=check)

        report_id = await current_guild.get_channel(
            settings.guild[current_guild.id]['channels']['report']
        ).send(
            '\n'.join([attachment.url for attachment in newmsg.attachments]),
            embed=discord.Embed(
                color=client.colors['error'],
                title='A report has been recieved.',
                description=message.content.split(None, 1)[1]
            ).set_footer(text='Any attachments have been included as URLs.')
        )

    else:
        # send this if we're just good to go
        report_id = await current_guild.get_channel(
            settings.guild[current_guild.id]['channels']['report']
        ).send(
            '\n'.join([attachment.url for attachment in message.attachments]),
            embed=discord.Embed(
                color=client.colors['error'],
                title='A report has been recieved.',
                description=message.content.split(None, 1)[1]
            ).set_footer(text='Any attachments have been included as URLs.')
        )

    globals()['reports'][str(report_id.id)] = message.author.id

    globals()['export'] = True

    try:
        msg = await message.author.send(
            embed=discord.Embed(
                color=client.colors['default'],
                title='Success',
                description='Your report has been recieved. Would you like '
                            'a copy of the report, exactly how it appears to'
                            ' the staff, for your records?'
            )
        )
    except discord.Forbidden:
        # we are blocked
        return

    await msg.add_reaction('\u2705') # :white_check_mark:

    def check(reaction, user):
        return (
            isinstance(reaction.message.channel, discord.abc.PrivateChannel) and
            user == message.author and
            reaction.message.id == msg.id and
            str(reaction.emoji) == '\u2705'
        )

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await msg.remove_reaction('\u2705', client.user)
        return

    await message.author.send(
        report_id.content,
        embed=discord.Embed(
            color=client.colors['error'],
            title='A report has been recieved.',
            description=message.content.split(None, 1)[1]
        ).set_footer(text='Any attachments have been included as URLs.')
    )

async def react(client, payload):
    if (
        payload.guild_id not in settings.guild or # guild not found (DM?)
        payload.channel_id != settings.guild[payload.guild_id]['channels']['report'] or # didn't react in our report channel: ignore
        str(payload.message_id) not in reports or # not a report: ignore
        payload.emoji.is_custom_emoji() or # unicode emojis only
        payload.emoji.name not in valid_mojis # not a reply emoji
    ):
        return

    bot_spam_channel = client.get_guild(payload.guild_id).get_channel(
        settings.guild[payload.guild_id]['channels']['bot_spam']
    )

    reporter = await client.get_guild(payload.guild_id).fetch_member(reports[str(payload.message_id)])

    if not reporter:
        reports.pop(str(payload.message_id) )
        return await bot_spam_channel.send(
            embed=client.embed_builder(
                'error',
                'Unable to send report: User has left the server.'
            ).set_footer(text='This report has been deleted.')
        )

    editmsg = await bot_spam_channel.send(
        f'**<@{payload.user_id}> You have selected to reply to report '
        f'{payload.message_id}.**\n\nPlease enter your response in this '
        'channel.\nThis times out after 3 minutes. You can cancel it by sending'
        ' `cancel`'
    )

    def check(m):
        if (
            m.channel == bot_spam_channel and
            m.author.id == payload.user_id
        ):
            if m.content.lower() == 'cancel':
                raise NameError

            return True

    try:
        msg = await client.wait_for('message', timeout=180.0, check=check)
    except (asyncio.TimeoutError, NameError):
        return await editmsg.edit(content=f'~~{editmsg.content}~~\n\nCancelled.')

    await reporter.send(
        embed=client.embed_builder(
            'error',
            msg.content,
            title='You have received a reply from the staff regarding your report.'
        )
    )

    await bot_spam_channel.send('Reply sent successfully.')

    reports.pop(str(payload.message_id) )

async def close(client):
    if export:
        with open('./ybf/configs/reports.json', 'w', encoding='utf-8') as data:
            json.dump(reports, data)

aliases = [
    'report',
    'r'
]
