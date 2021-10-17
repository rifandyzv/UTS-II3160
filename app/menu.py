import json

# Menus
with open('menu.json', 'r') as read_file:
    data = json.load(read_file)


def saveJson(data):
    with open('menu.json', 'w') as dumpFile:
        json.dump(data, dumpFile)

menu = data['menu']