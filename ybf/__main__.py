import disnake
import ybf # import base necessities

print('Starting up...')

YBF = ybf.Client(intents=disnake.Intents.all())

KEY = None
with open('./ybf/configs/token.key', encoding='utf-8') as keyfile:
    KEY = keyfile.read().strip()

YBF.run(KEY)
