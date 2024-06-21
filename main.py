from create_telegrams import start_creating
from open_telegrams import start_opening
from ppx_creator import create_proxy_list
import os

while True:
    os.system('cls')
    print('1-start to UNPACK TData')
    print('2-start to OPEN unpack tg accounts')
    print('3-create PPX file(proxy)')
    print('q-exit')
    choise = input('')
    if choise == 'q':
        break
    elif choise == '1':
        start_creating()
    elif choise == '2':
        start_opening()
    elif choise == '3':
        create_proxy_list()
input()