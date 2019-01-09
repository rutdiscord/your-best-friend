import ybf # import base necessities

print('Starting up...')

YBF = ybf.Client()

KEY = None
with open('./ybf/configs/token.key') as keyfile:
    KEY = keyfile.read().strip()

YBF.run(KEY)
