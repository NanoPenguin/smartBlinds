import sys, os
os.system('git -C smartBlinds pull')
os.system('python3 ~/smartBlinds/controller/code/main.py & python3 ~/smartBlinds/controller/code/webhooklisten.py')
