import sys, os, time
from smartBlinds.controller.code.screen import *
SCREEN = Screen(False, False)
SCREEN.startScreen(30)
os.system('git -C smartBlinds pull')
os.system('python3 ~/smartBlinds/controller/code/main.py & python3 ~/smartBlinds/controller/code/webhooklisten.py')
