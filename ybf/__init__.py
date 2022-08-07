# errors
import traceback
import sys

# sleep
import asyncio

# regex (filter invites)
import re

from .configs import settings
from . import commands

#delete police
from datetime import datetime, timedelta
from .utilities import police

import disnake as discord

class Client(discord.Client):
    def __init__(self):
        # perform discord.py startup
        self.colors = {
            'default' : discord.Color(0xBF4DFF),
            'error' : discord.Color(0xD52626),
            'warning' : discord.Color(0xFF8800)
        }
        self.stored_roles = {}
        self.beta = False
        self.url_regex = re.compile(r'(https?:\/\/)?[a-zA-Z0-9-]+?\.[a-zA-Z]{1,3}\/?[^\n ]*')
        self.invite_regex = re.compile(r'(https?:\/\/)?discord(app)?\.com\/(invite\/)?[a-zA-Z0-9-]+')
        super().__init__()

    async def on_ready(self):
        # cache ids to usable roles
        for guild in settings.guild:
            if guild in [guild.id for guild in self.guilds]:
                self.stored_roles[guild] = {}
                for id in settings.guild[guild]['role_ids']:
                    self.stored_roles[guild][id[0]] = self.get_guild(guild).get_role(id[1])

        # activate any commands that need to cache stuff
        for plugin in commands.iterable:
            try:
                await plugin.ready(self)
            except AttributeError:
                pass

        # are we on the beta branch? if so, ignore the stable bot
        if self.user.id == settings.self['beta']:
            self.beta = True
        
        # cache the owner
        self.owner = await self.fetch_user(settings.self['owner_id'])
        
        print('[Ready]')

    async def check_for_mentions(self, message):
        '''
        checks to see if this user is mentioned in a given message, and then
        alerts the staff if it is.
        '''
        if f'<@{self.user.id}>' in message.content and \
          'bot_spam' in settings.guild[message.guild.id]['channels']:
            channel = message.guild.get_channel(
                settings.guild[message.guild.id]['channels']['bot_spam'])
            await channel.send(
                f'**Mention Alert** in <#{message.channel.id}>.')

    def check_for_banned_messages(self, message):
        '''
        checks to see if a given message contains banned strings
        '''
        for exception in settings.purge['ignored_content']:
            if exception in message.content.lower():
                return True
        
        # bot commands
        if message.content.lower().startswith(
            tuple(
                settings.purge['exceptions']
                )
            ):
                return True
        
        # box drawing characters
        for x in range(0x002500, 0x0025FF):
            if chr(x) in message.content:
                return True
        
        for x in range(0x002800, 0x0028FF):
            if chr(x) in message.content:
                return True
        
        # wingdings
        exceptions = {
            # zodiac
            '\u264B\uFE0E',
            '\u264C\uFE0E',
            '\u264D\uFE0E',
            '\u264E\uFE0E',
            '\u264F\uFE0E',
            '\u2650\uFE0E',
            '\u2651\uFE0E',
            '\u2652\uFE0E',
            '\u2653\uFE0E',
            '\u264A\uFE0E',
            '\u2648\uFE0E',
            '\u2649\uFE0E',

            '\U0001F670', # SCRIPT LIGATURE ET ORNAMENT
            '\U0001F675', # Swash Ampersand Ornament
            '\u25CF\uFE0E', # Black Circle
            '\u274D\uFE0E', # Shadowed White Circle
            '\u25A0\uFE0E', # BLACK SQUARE FOR STOP
            '\u25A1\uFE0E', # White Square
            '\u25FB\uFE0E', # White Medium Square
            '\u2751\uFE0E', # Lower Right Shadowed Square
            '\u2752\uFE0E', # Upper Right Shadowed Square
            '\u2B27\uFE0E', # Black Medium Lozenge
            '\u29EB\uFE0E', # Black Lozenge
            '\u25C6\uFE0E', # Black Diamond 
            '\u2756\uFE0E', # Black Diamond Minus White X
            '\u2B25\uFE0E', # Black Medium Diamond
            '\u2327\uFE0E', # X In A Rectangle Box
            '\u2353\uFE0E', # APL Functional Symbol Quad Up Caret
            '\u2318\uFE0E', # Place of Interest Sign
            '\u270C\uFE0E', # V for Victory 
            '\U0001F44C\uFE0E', # OK Hand
            '\U0001F44D\uFE0E', # Thumbs Up Sign
            '\U0001F44E\uFE0E', # Thumbs Down Sign
            '\u261C\uFE0E', # 'White Left Pointing Index
            '\u261E\uFE0E', # White Right Pointing Index
            '\u261D\uFE0E', # White Up Pointing Index
            '\u261F\uFE0E', # White Down Pointing Index
            '\u270B\uFE0E', # Raised Hand Emoji
            '\u263A\uFE0E', # Smiling Face
            '\U0001F610\uFE0E', # Neutral Face
            '\u2639\uFE0E', # White Frowning Face
            '\U0001F4A3\uFE0E', # Bomb
            '\u2620\uFE0E', # Skull and Crossbones
            '\u2690\uFE0E', # White Flag
            '\U0001F3F1\uFE0E', # White Pennant
            '\u2708\uFE0E', # Airplane
            '\u263C\uFE0E', # White Sun with Rays
            '\U0001F4A7\uFE0E', # Droplet
            '\u2744\uFE0E', # Snowflake
            '\U0001F546\uFE0E', # White Latin Cross
            '\u271E\uFE0E', # Shadowed White Latin Cross
            '\U0001F548\uFE0E', # Celtic Cross
            '\u2720\uFE0E', # Maltese Cross
            '\u2721\uFE0E', # Star of David
            '\u262A\uFE0E', # Star and Crescent
            '\U0001F4C2\uFE0E', # Open File Folder
            '\U0001F4C4\uFE0E', # Page Facing Up
            '\U0001F5CF\uFE0E', # Page
            '\U0001F5D0\uFE0E', # Pages
            '\U0001F5C4\uFE0E', # File Cabinet
            '\u231B\uFE0E', # Hourglass
            '\U0001F5AE\uFE0E', # Wired Keyboard
            '\U0001F5B0\uFE0E', # Two Button Mouse
            '\U0001F5B2\uFE0E', # Trackball
            '\U0001F4C1\uFE0E', # File Folder
            '\u275E\uFE0E', # Heavy Double Comma Quotation Mark Ornament
            '\u275D\uFE0E', # Heavy Double Turned Comma Quotation Mark Ornament
            '\u270F\uFE0E', # Pencil
            '\u200B', # Zero-width space
            '\u2701\uFE0E', # Upper Blade Scissors
            '\U0001F453\uFE0E', # Eyeglasses
            '\U0001F56D\uFE0E', # Ringing Bell
            '\U0001F56E\uFE0E', # Open Book
            '\U0001F582\uFE0E', # Back of Envelope
            '\U0001F57F\uFE0E', # Black Telephone
            '\u2706\uFE0E', # Black Touchtone Telephone
            '\U0001F4EB\uFE0E', # Closed Mailbox with Raised Flag
            '\U0001F5AC\uFE0E', # Soft Shell Floppy Disk
            '\U0001F583\uFE0E', # Stamped Envelope
            '\U0001F5AB\uFE0E', # White Hard Shell Floppy Disk
            '\u2707\uFE0E', # Tape Drive
            '\U0001F4EA\uFE0E', # Closed Mailbox with Lowered Flag
            '\U0001F4EC\uFE0E', # Open Mailbox with Raised Flag
            '\U0001F4ED\uFE0E', # Open Mailbox with Lowered Flag
            '\u270D\uFE0E', # Writing Hand Emoji
            '\U0001F5B4\uFE0E', # Hard Disk
            '\U0001F5B3\uFE0E', # Old Personal Computer
            '\U0001F56F\uFE0E', # Candle
            '\u2702\uFE0E', # Black Scissors
            '\u262F\uFE0E', # Yin Yang
            '\u2740\uFE0E', # White Florette
            '\u2638\uFE0E', # Wheel of Dharma
            '\u0950\uFE0E', # Devanagari Om
            '\u273F\uFE0E', # Black Florette
            '\U0001F58E', # Left Writing Hand
        }

        for character in exceptions:
            if character in message.content:
                return True

    #### EVENTS ####

    async def on_message(self, message):
        if (
                message.author.id == self.user.id or # ignore myself
                message.author.bot # ignore bots
        ):
            return

        # did this message come from a DM?
        direct_message = isinstance(message.channel, discord.channel.DMChannel)

        if not direct_message:
            # special checks for guilds
            if (
                    # role directory not cached
                    'stored_roles' not in dir(self) or
                    # this guild not cached
                    message.guild.id not in self.stored_roles or
                    # roleban role not cached
                    'rolebanned' not in self.stored_roles[message.guild.id]
            ):
                return

            # announce mttnews
            if message.channel.id in settings.announcement_channels:
                channel = message.guild.get_channel(
                    settings.guild[message.guild.id]['channels']['announcement'])

                return await channel.send(
                    '__***IMPORTANT***__\n'\
                    f'*New post in <#{message.channel.id}>!!!*')

        if not message.content: # empty message or attachment
            return

        try:
            if not direct_message and (
                    'roles' not in dir(message.author) or # user not cached yet
                    self.stored_roles[
                        message.guild.id
                    ]['rolebanned'] in message.author.roles # ignore rolebanned users
            ):
                await self.check_for_mentions(message)
                return
                # TODO: This exact code shows up thrice. Maybe squish it all into one func?
        except AttributeError:
            pass

        # detect invocation
        invocation = None

        for invoker in settings.invokers:
            if (
              message.content.lower().startswith(invoker) and # invokation matches
              message.content.lower() != invoker # don't fire if ONLY the invocation is typed
              ):
                invocation = invoker

        if not invocation: # not a command
            if not direct_message: # message in this server
                await self.check_for_mentions(message)
                    
            return # don't continue to check for a command

        command = message.content[len(invocation):].split()[0].lower()

        # run command
        if command in commands.list:
            return await commands.list[command](self, message, message.content[len(invocation):])

        if direct_message:
            return

        await self.check_for_mentions(message)

    async def on_member_ban(self, guild, user):
        settings.purge['ignored_users'].append(user.id)
        # Presumably, we don't have to ever stop ignoring a banned user because
        # they'll never come back, but also-presumably keeping the list small
        # will also keep memory free.
        await asyncio.sleep(5)
        settings.purge['ignored_users'].remove(user.id)

    async def on_message_delete(self, message):
        if self.beta and message.guild.get_member(settings.self['stable']):
            # is stable me in this server? then no dp
            return
        
        now = datetime.now(tz=message.created_at.tzinfo)

        if (
          isinstance(message.channel, discord.channel.DMChannel) or # ignore deletes in dms
          message.author.bot or # ignore bots
          message.channel.id in settings.purge['ignored_channels'] or # ignore channels being purged
          message.author.id in settings.purge['ignored_users'] or # ignore members being banned
          message.guild.id == 256926147827335170 or # no DP in oneshot
          self.check_for_banned_messages(message)
        ):
            return

        # did a mod delete the message?
        deleted = await message.guild.audit_logs(
            action=discord.AuditLogAction.message_delete,
            after=(now - timedelta(seconds=1))
          ).find(lambda m: m.target==message.author)
        # messages only appear in the audit log if someone else deleted them
        if deleted is not None:
            return

        # Delete Police
        delta = now - message.created_at

        if police.solve(delta):
            msg = message.clean_content
            
            if self.invite_regex.search(msg):
                return

            msg = self.url_regex.sub(
                '[Hyperlink Blocked]',
                msg)

            mbd = discord.Embed(
                color=message.author.color,
                description=msg)

            mbd.set_author(
                name=f'{message.author.display_name} said...',
                icon_url=message.author.display_avatar.url)

            mbd.set_footer(
                text='This message was automatically re-sent because it was '\
                     'deleted too recently after it was sent.')

            if message.attachments:
                mbd.add_field(
                    name='Attachments:',
                    value=str(len(message.attachments)))

            await message.channel.send(embed=mbd)

    async def on_raw_message_edit(self, payload):
        channel_id = int(payload.data['channel_id'])
        # rehoist after pins
        if channel_id not in settings.pin_channels:
            return

        channel = self.get_channel(channel_id)
        message = await channel.fetch_message(int(payload.message_id))

        if message.id in settings.pin_channels[channel_id]:
            return

        if not message.pinned:
            return  # pin was removed or no pin

        # actually unpinning an already unpinned message shouldn't raise any
        # errors but I'm not taking any chances
        for pin in settings.pin_channels[channel_id]:
            message = await channel.fetch_message(pin)
            await message.unpin()

        await asyncio.sleep(0.1)

        for pin in settings.pin_channels[channel_id]:
            message = await channel.fetch_message(pin)
            await message.pin()

    async def on_raw_reaction_add(self, payload):
        for plugin in commands.iterable:
            if 'react' in dir(plugin):
                await plugin.react(self, payload)

    def embed_builder(self, kind, desc, title="Error"):
        if kind in self.colors:
            return discord.Embed(
                color=self.colors[kind],
                title=title,
                description=desc
            )
        else:
            return discord.Embed(
                color=kind,
                title=title,
                description=desc
            )

    async def on_error(self, event_method, *args, **kwargs):
        # pylint: disable=misplaced-bare-raise
        # pylinting this out because this *is* an except statement
        # args[0] is the message that was recieved prior to the error. At least,
        # it should be. We check it first in case the cause of the error wasn't a
        # message.
        if args and isinstance(args[0], discord.Message):
            if isinstance(sys.exc_info()[0], discord.errors.NotFound):
                # fail silently if message was deleted
                return

            await self.owner.send(
                f'{args[0].jump_url}\n\n{traceback.format_exc()}')

            # uncomment if you want ybf to post errors in chat
            # if isinstance(sys.exc_info()[0], discord.Forbidden):
            #     return # don't announce missing permissions
            # await args[0].channel.send(
            #     embed=self.embed_builder('error', sys.exc_info()[0].__name__))
        else:
            raise

    async def close(self):
        print('Closing')

        # allow commands to save before close
        for plugin in commands.iterable:
            # print(f'running {plugin.__name__}.close')
            if 'close' in dir(plugin):
                await plugin.close(self)
            # except NameError:
            #     print(f'{plugin.__name__} has no close')
            #     pass

        await super().close()

# if __name__ == '__main__':
#     # Only start the bot if it is being run directly
#     YBF = Client()
#
#     KEY = None
#     with open('./configs/token.key', encoding='utf-8') as keyfile:
#         KEY = keyfile.read().strip()
#
#     YBF.run(KEY)
