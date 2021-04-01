from random import choice
from random import randint

import json

async def command(client, message, command):
    if len(command.split()) <= 1:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'No news ID provided.'
            )
        )

    context = command.split(None, 1)

    if context[1].lower() == 'force':
        if len(client.af21_data['message_queue']) > 0:
            news = {}
            try:
                with open('./ybf/configs/news.json', encoding='utf-8') as data:
                    news = json.load(data)

            except(FileNotFoundError, json.decoder.JSONDecodeError):
                pass

            msg = client.af21_data['message_queue'].pop(0)

            headline = msg['headline']
            link = msg['link']
            attachment_msg = ''
            if 'attachments' in msg:
                ach = msg['attachment']
                attachment_msg = f'\n\nMessage has an attachment: {ach}'

            await client.af21_data['postch'].send(f'Generated from {link}\n\n{headline}\nApprove it with `f!news {len(news)}`{attachment_msg}')

            news[str(len(news))] = msg

            with open('./ybf/configs/news.json', 'w', encoding='utf-8') as data:
                json.dump(news, data)

            return True
        return await message.channel.send(
                embed=client.embed_builder(
                    'error',
                    'The message queue is empty.',
                    title='Unable to pop from queue.'
                )
            )
    
    if context[1].lower() == 'queue':
        queuestat = len(client.af21_data["message_queue"])
        reminder = ''
        if queuestat > 0:
            reminder = '\n\nForce these messages from the queue with `f!news force`.'
        return await message.channel.send(
                embed=client.embed_builder(
                    'default',
                    f'There are {queuestat} messages in the queue.{reminder}',
                    title='Queue status:'
                ).set_footer(text='News posts not showing up in #event-planning? "f!news force" them, then do "f!die" to reboot the bot.')
            )

    headline = None
    link = None
    name = None
    attachment = None

    with open('./ybf/configs/news.json', encoding='utf-8') as data:
        news = json.load(data)
        headline = news[context[1]]['headline']
        link = news[context[1]]['link']
        name = news[context[1]]['user']
        if 'attachment' in news[context[1]]:
            attachment = news[context1]['attachment']

    clickbaitery = choice([
        'All we can say is "yaas queen."',
        'Is this what finally cancels them?',
        'Take that, patriarchy!',
        'Literally ruining our childhoods.',
        'This time, for real. We swear.',
        f'I guess we know why they\'re called {name} now huh?',
        'Girl, I am shook.',
        f'I can\'t believe {name} has done this.',
        'The controversy that is shaking the world!',
        'And we couldn\'t be more upset.',
        'I\'m shaking and crying.',
        'Number 3 will shock you.',
        'Real! Not clickbait!',
        'Certified as "Not Fake News".',
        'Great, something else to worry about besides my crippling student debt.',
        'Part of our "Feel better about yourself by laughing at the expense of someone else" line of quizzes.',
        'Here\'s why it\'s so adorable.',
        'Something to care about while waiting for the next *WandaVision* episode.',
        'Quite frankly? It\'s about time someone said it.',
        'We demonstrated the issue with cat photos. (Slideshow - 6 Images)',
        'It was probably the libertarians\' idea.',
        'Why I\'m still waiting for an apology and—more importantly—why I\'ll refuse to accept it when they do.',
        'There goes my faith in humanity. *Again.*',
        'Finally, something to restore your faith in humanity. *Again.*',
        f'With a name like {name} it was only a matter of time.'
    ])
    
    if attachment:
        thumb = attachment
    else:
        thumb = choice(client.af21_data['thumbs'])

    color = randint(0x000000, 0xFFFFFF)

    newmsg = await client.af21_data['newsch'].send(
        embed=client.embed_builder(
            color,
            f'[{clickbaitery}]({link})',
            title=headline)
                .set_author(name="BREAKING NEWS")
                .set_thumbnail(url=thumb))
    
    await message.channel.send(
        embed=client.embed_builder(
            color,
            f'[Jump to news post](https://discord.com/channels/{newmsg.guild.id}/{newmsg.channel.id}/{newmsg.id})',
            title='Sent'
        )
    )

aliases = [
    'news'
]
