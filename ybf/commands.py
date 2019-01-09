import importlib
import os

# print('Working in ' + os.getcwd())

list = {}
iterable = []

print('Importing plugins...')

# add all plugins in plugin folder
for plugin in os.scandir('./your-best-friend/plugins'):
    if plugin.name.endswith('.py'):
        package = importlib.import_module('your-best-friend.plugins.' + plugin.name[:-3])

        iterable.append(package)

        for alias in package.aliases:
            list[alias] = package.command
