"""
*   main.py used as example script
"""
from Core.Renderable.Npcs import *
from Misc.Misc import *
import Banzai
import time

Banzai.init()

with Npcs(name='Banker') as n:
    print(n.get_animation())
Banzai.terminate()
