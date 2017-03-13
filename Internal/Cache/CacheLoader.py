import json


class CacheLoader:
    def __init__(self):
        self.items, self.npcs, self.objects = [], [], []
        with open('Internal\Cache\ItemDefs.txt') as item:
            for line in item:
                self.items.append(line)

        with open('Internal\Cache/NpcDefs.txt') as item:
            for line in item:
                self.npcs.append(line)

        with open('Internal\Cache\ObjectDefs.txt') as item:
            for line in item:
                self.objects.append(line)


cache = CacheLoader()
