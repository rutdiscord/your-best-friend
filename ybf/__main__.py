import your-best-friend # import base necessities

print('Starting up...')

YBF = ybf.Client()

KEY = None
with open('./your-best-friend/configs/token.key') as keyfile:
    KEY = keyfile.read().strip()

YBF.run(KEY)
