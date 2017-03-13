"""
*   main.py used as example script
"""
from Core.Renderable.Npcs import *
import Banzai

Banzai.init()

with Npcs(name='Banker') as n:
    print(n.get_name())

Banzai.terminate()
