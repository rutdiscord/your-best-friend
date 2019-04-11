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

import discord

class Client(discord.Client):
    def __init__(self):
        # perform discord.py startup
        self.colors = {
            'default' : discord.Color(0xBF4DFF),
            'error' : discord.Color(0xD52626),
            'warning' : discord.Color(0xFF8800)
        }
        self.stored_roles = {}
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

    async def check_for_banned_messages(self, message):
        '''
        checks to see if a given message contains banned strings
        '''
        if (
            'www.latlmes.com/' in message.content or
            'd-BCRCuXR6U' in message.content
          ):
          return True

    #### EVENTS ####

    async def on_message(self, message):
        if (
          message.author.id == self.user.id or # ignore myself
          message.author.bot # ignore bots
        ):
            return

        if not isinstance(message.channel, discord.abc.PrivateChannel) and ( # message is in a server
          'stored_roles' not in dir(self) or # not ready yet
          message.guild.id not in self.stored_roles or # not ready yet
          'rolebanned' not in self.stored_roles[message.guild.id] # not ready yet
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

        if (
            isinstance(message.channel, discord.abc.PrivateChannel) or # ignore most things in dms
            'roles' not in dir(message.author) or # user not cached yet
            self.stored_roles[message.guild.id]['rolebanned'] in message.author.roles # ignore rolebanned users
        ):
            await self.check_for_mentions(message)
            banned_msg = await self.check_for_banned_messages(message)
            if(banned_msg):
                await message.delete()
            return

        # detect invocation
        invocation = None

        for invoker in settings.invokers:
            if (
              message.content.lower().startswith(invoker) and # invokation matches
              message.content.lower() != invoker # don't fire if ONLY the invocation is typed
              ):
                invocation = invoker
        if not invocation and not isinstance(message.channel, discord.abc.PrivateChannel):
            await self.check_for_mentions(message)
            banned_msg = await self.check_for_banned_messages(message)
            if(banned_msg):
                await message.delete()
            return # don't continue to check for a command

        command = message.content[len(invocation):].split()[0].lower()

        # run command
        if command in commands.list:
            return await commands.list[command](self, message, message.content[len(invocation):])

        if isinstance(message.channel, discord.abc.PrivateChannel): return
        await self.check_for_mentions(message)
        banned_msg = await self.check_for_banned_messages(message)
        if(banned_msg):
            await message.delete()

    async def on_member_ban(self, guild, user):
        settings.purge['ignored_users'].append(user.id)
        # Presumably, we don't have to ever stop ignoring a banned user because
        # they'll never come back, but also-presumably keeping the list small
        # will also keep memory free.
        await asyncio.sleep(5)
        settings.purge['ignored_users'].remove(user.id)

    async def on_message_delete(self, message):
        now = datetime.utcnow()

        banned_msg = await self.check_for_banned_messages(message)

        if (
          isinstance(message.channel, discord.abc.PrivateChannel) or # ignore deletes in dms
          message.author.bot or # ignore bots
          message.channel.id in settings.purge['ignored_channels'] or # ignore channels being purged
          message.author.id in settings.purge['ignored_users'] or # ignore members being banned
          message.content.lower().startswith(tuple(settings.purge['exceptions'])) or # ignore exceptions
          banned_msg # message has banned content
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
        if (
          'roleban' in settings.guild[message.guild.id]['channels'] and
          message.channel.id == settings.guild[message.guild.id]['channels']['roleban']
        ):
            # plaintext DP in roleban channel
            if len(message.content) > 1950:
                # Send huge messages in 2 messages
                await message.channel.send(f'___***DELETED MESSAGE BY {message.author.display_name}:***___')
                await message.channel.send(message.clean_content)
            else:
                await message.channel.send(f'___***DELETED MESSAGE BY {message.author.display_name}:***___\n{message.clean_content}')
            if message.attachments:
                # add on number of attachments too
                await message.channel.send(f'*Message had {len(message.attachments)} attachments.*')
            return

        delta = now - message.created_at

        if police.solve(delta):
            msg = message.clean_content

            msg = re.sub(
                r'(https?:\/\/)?discord\.gg\/[a-zA-Z0-9-]*',
                '[Invite Redacted]',
                msg)
            msg = re.sub(
                r'(https?:\/\/)?discordapp\.com\/invite\/[a-zA-Z0-9-]*',
                '[Invite Redacted]',
                msg)

            mbd = discord.Embed(
                color=message.author.color,
                description=msg)

            mbd.set_author(
                name=f'{message.author.display_name} said...',
                icon_url=message.author.avatar_url)

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

    def embed_builder(self, type, desc, title="Error"):
        return discord.Embed(
            color=self.colors[type],
            title=title,
            description=desc
        )

    async def on_error(self, event_method, *args, **kwargs):
        # args[0] is the message that was recieved prior to the error. At least,
        # it should be. We check it first in case the cause of the error wasn't a
        # message.
        if args and isinstance(args[0], discord.Message):
            await self.get_user(settings.self['owner_id']).send(
                f'{args[0].jump_url}\n\n{traceback.format_exc()}')

            if isinstance(sys.exc_info()[0], discord.Forbidden):
                return # don't announce missing permissions
            await args[0].channel.send(
                embed=self.embed_builder('error', sys.exc_info()[0].__name__))
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
#     with open('./configs/token.key') as keyfile:
#         KEY = keyfile.read().strip()
#
#     YBF.run(KEY)
