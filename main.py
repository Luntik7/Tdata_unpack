from create_telegrams import start_creating
from open_telegrams import start_opening
import os

while True:
    os.system('cls')
    print('1-start to UNPACK TData')
    print('2-start to OPEN unpack tg accounts')
    print('q-exit')
    choise = input('')
    if choise == 'q':
        break
    elif choise == '1':
        start_creating()
    elif choise == '2':
        start_opening()
input()