from random import choice
from random import randint

async def command(client, message, command):
    if len(command.split()) <= 1:
        return await message.channel.send(
            embed=client.embed_builder(
                'error',
                'No news ID provided.'
            )
        )

    context = command.split(None, 1)

    headline = None
    link = None
    name = None

    with open('./ybf/configs/news.json', encoding='utf-8') as data:
        news = json.load(data)
        headline = news[context[1]]['headline']
        link = news[context[1]]['link']
        name = news[context[1]]['user']

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
        'Why I\'m still waiting for an apology and—more importantly—why I\'ll refuse to accept it when he does.',
        'There goes my faith in humanity. *Again.*',
        'Finally, something to restore your faith in humanity. *Again.*',
        f'With a name like {name} it was only a matter of time.'
    ])
    thumb = choice(client.af21_data['thumbs'])

    await client.af21_data['newsch'].send(
        embed=client.embed_builder(
            randint(0x000000, 0xFFFFFF),
            f'[{clickbaitery}]({link})',
            title=headline)
                .set_author(name="BREAKING NEWS")
                .set_thumbnail(url=thumb))

aliases = [
    'news'
]
