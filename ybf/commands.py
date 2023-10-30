import importlib
import os

# print('Working in ' + os.getcwd())

all_commands = {}
iterable = []

print('Importing plugins...')

# add all plugins in plugin folder
for plugin in os.scandir('./ybf/plugins'):
    if plugin.name.endswith('.py'):
        package = importlib.import_module('ybf.plugins.' + plugin.name[:-3])

        iterable.append(package)

        if 'aliases' in dir(package):
            for alias in package.aliases:
                all_commands[alias] = package.command
