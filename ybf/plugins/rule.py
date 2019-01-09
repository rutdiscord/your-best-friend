import json
import shlex
import discord

rules = {}

export = False

async def ready(client):
    try:
        with open('./ybf/configs/rules.json') as data:
            globals()['rules'] = json.load(data)

    except FileNotFoundError:
        print('Writing new rules file: one wasn\'t found')
        rules = {
            'start_at' : 1,
            'simple' : [
                'Be excellent to each other!',
                'Party on, dudes!'
            ],
            'extended' : {
                '1' : '__***Rule 1: Be excellent to each other!***__',
                '2' : '__***Rule 2: Party on, dudes!***__'
            }
        }
        globals()["export"] = True

async def command(client, message, command):
    context = command.split(None, 1)

    if len(context) == 1:
        helpmsg = discord.Embed(
            title='List of Rules:',
            description = '',
            color=client.colors['default']
        )

        for i,rule in enumerate(rules['simple']):
            index = i + rules['start_at']
            helpmsg.description += f'{index}: {rule}\n'

        helpmsg.set_footer(text='More information about these rules can be accessed with "rule #".')

        return await message.channel.send(embed=helpmsg)

    if context[1].startswith('set '):
        if client.stored_roles[message.guild.id]['staff'] not in message.author.roles:
            return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    'You are not allowed to modify rules.'
                )
            )

        setting = shlex.split(context[1])
        if len(setting) < 2 or (
            len(setting) < 3 and setting[1] != 'list'
        ):
            return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    '`set` requires 2 additional parameters to work. '
                    '(`rule set "name" "value"`)'
                )
            )

        if setting[1] == 'list':
            return await message.channel.send(
                embed=client.embed_builder(
                    'default',
                    [rule_name for rule_name in rules['extended']],
                    title='List of Rules'
                )
            )

        if setting[1] == 'simple':
            command = None

            if len(setting) < 4:
                return await message.channel.send(
                    embed=client.embed_builder(
                        'error',
                        '`set simple` requires 1 additional parameter to work. '
                        '(`rule set simple "name" "value"`)'
                    )
                )

            try:
                command = int(setting[2]) - rules['start_at']
            except ValueError:
                return await message.channel.send(
                    embed=client.embed_builder(
                        'error',
                        'Only numbered rules can have simple descriptions.'
                    )
                )

            rules['simple'][command] = setting[3]
            globals()["export"] = True
            return await message.channel.send(
                embed=client.embed_builder(
                    'default',
                    f'Successfully set rule {setting[1]}\'s simple description.',
                    title='Done'
                )
            )

        if setting[1] == 'start_at':
            try:
                rules['start_at'] = int(setting[2])
            except ValueError:
                return await message.channel.send(
                    embed=client.embed_builder(
                        'error',
                        'You can only use numbers to order rules.'
                    )
                )

        try:
            command = int(setting[1]) - rules['start_at']
            interval = command - len(rules['simple'])
            if interval == 1:
                g.append(setting[2])
                await message.channel.send(
                    embed=client.embed_builder(
                        'warning',
                        'Adding a new simple rule description to accomodate the '
                        'new rule.',
                        title='Warning'
                    )
                )
            elif command - len(rules['simple']) > 1:
                return await message.channel.send(
                    embed=client.embed_builder(
                        'error',
                        'You cannot skip a number in numbered rules.'
                    )
                )
        except ValueError:
            # named rule
            pass

        rules['extended'][setting[1]] = setting[2]
        globals()["export"] = True
        return await message.channel.send(
            embed=client.embed_builder(
                'default',
                f'Successfully set rule {setting[1]}.',
                title='Done'
            ).set_footer(text='You may also want to change the simple description too.')
        )

    if context[1] not in rules['extended']:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'No information found on that rule.',
                title='Not Found'
            )
        )

    return await message.channel.send(
        embed=discord.Embed(
            description=rules['extended'][context[1]],
            color=client.colors['default']
        )
    )


async def close(client):
    if export:
        with open('./ybf/configs/rules.json', 'w') as data:
            json.dump(rules, data)

aliases = [
    'rules',
    'rule'
]
