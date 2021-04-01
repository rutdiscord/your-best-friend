from random import choice
from random import randint

async def command(client, message, command):
    if len(command.split()) <= 1:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'Nothing to post provided.'
            )
        )

    context = command.split(None, 2)

    if not context[1].startswith('https://discord.com/channels/'):
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'No message link provided for headline.'
            )
        )

    clickbaitery = choice([
        'All we can say is "yaas queen."',
        'Is this what finally cancels them?',
        'Take that, patriarchy!',
        'Literally ruining our childhoods.',
        'This time, for real. We swear.',
        f'I guess we know why they\'re called that now huh?',
        'Girl, I am shook.',
        f'I can\'t believe they\'ve done this.',
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
        'Why I\'m still waiting for an apology and—more importantly—why I\'ll refuse to accept it when he does.',
        'There goes my faith in humanity. *Again.*',
        'Finally, something to restore your faith in humanity. *Again.*'
    ])
    thumb = choice(client.af21_data['thumbs'])

    await client.af21_data['newsch'].send(
        embed=client.embed_builder(
            randint(0x000000, 0xFFFFFF),
            f'[{clickbaitery}]({context[1]})',
            title=context[2])
                .set_author(name="BREAKING NEWS")
                .set_thumbnail(url=thumb))

aliases = [
    'news'
]
