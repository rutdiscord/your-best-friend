# errors
import traceback
import sys

# sleep
import asyncio

# regex (filter invites)
import re

# random chance
from random import choice
from random import randint

from .configs import settings
from . import commands

#delete police
from datetime import datetime, timedelta
from .utilities import police

# nlp for AF21
from .utilities import nlp

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
        self.beta = False
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

    async def check_for_banned_messages(self, message):
        '''
        checks to see if a given message contains banned strings
        '''
        for exception in settings.purge['ignored_content']:
            if exception in message.content:
                return True

    #### EVENTS ####

    async def on_message(self, message):
        if (
                message.author.id == self.user.id or # ignore myself
                message.author.bot # ignore bots
        ):
            return

        # did this message come from a DM?
        direct_message = isinstance(message.channel, discord.abc.PrivateChannel)

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

        if not direct_message and (
                'roles' not in dir(message.author) or # user not cached yet
                self.stored_roles[
                    message.guild.id
                ]['rolebanned'] in message.author.roles # ignore rolebanned users
        ):
            await self.check_for_mentions(message)
            banned_msg = await self.check_for_banned_messages(message)
            if(banned_msg):
                await message.delete()
            return
            # TODO: This exact code shows up thrice. Maybe squish it all into one func?

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
                banned_msg = await self.check_for_banned_messages(message)
                if(banned_msg):
                    await message.delete()
                if message.guild.id == 120330239996854274 and randint(1,20) == 1:
                    headline = nlp.generate(message.author.display_name, message.clean_content)
                    if headline:
                        print(f'Sending headline: {headline}')
                        newsch = message.guild.get_channel(669077343482019870)
                        clickbaitery = choice([
                            'All we can say is "yaas queen."',
                            'Is this what finally cancels them?',
                            'Take that, patriarchy!',
                            'Literally ruining our childhoods.',
                            'This time, for real. We swear.',
                            f'I guess we know why he\'s called {message.author.display_name} now huh?',
                            'Girl, I am shook.',
                            f'I can\'t believe {message.author.display_name} has done this',
                            'The controversy that is shaking the world!',
                            'And we couldn\'t be more upset.'
                        ])
                        thumb = choice([
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654848602472478/cry-4381422_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654851685154816/baby-408262_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654854880559114/call-2946023_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654858861346836/cavalier-1444026_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654861809418271/hacker-3641937_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654864179200030/hacker-2883632_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654868075970611/people-2557494_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654869242380298/amiga-4321211_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654871905632286/iman-1459322_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654873336021013/people-315907_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654901375205466/coronavirus-5064371_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654906928201728/comic-1296117_640.png',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654904096391178/fear-1172407_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654908274049024/shocked-4625235_640.png',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654909351854140/portrayal-89189_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654911252660224/scared-2175161_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654912560496650/poses-1367416_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654914271772753/shocked-2681488_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654915598090250/lover-1822498_640.jpg',
                            'https://cdn.discordapp.com/attachments/258370851920019456/826654917233344523/dog-1951211_640.jpg'
                        ])
                        await newsch.send(
                            embed=self.embed_builder(
                                randint(0x000000, 0xFFFFFF),
                                headline,
                                title="BREAKING NEWS!")
                                    .set_author(
                                        name=clickbaitery,
                                        url="https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}")
                                        .set_thumbnail(url=thumb)
                                        )
                    
            return # don't continue to check for a command

        command = message.content[len(invocation):].split()[0].lower()

        # run command
        if command in commands.list:
            return await commands.list[command](self, message, message.content[len(invocation):])

        if direct_message:
            return

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
        if self.beta and message.guild.get_member(settings.self['stable']):
            # is stable me in this server? then no dp
            return
        
        if message.guild.id == 256926147827335170: # r/oneshot
            # no DP in oneshot
            return
        
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
