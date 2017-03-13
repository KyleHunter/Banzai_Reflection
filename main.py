from Core.Renderable.Npcs import *
import Banzai
import time
from Internal.Cache.CacheLoader import *
import json

Banzai.init()

with Npcs(name='Banker') as n:
    pass

Banzai.terminate()
