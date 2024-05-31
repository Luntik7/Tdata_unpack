import os 
from dotenv import load_dotenv, find_dotenv
from loguru import logger
import subprocess



load_dotenv(find_dotenv())

BASE_PATH = os.getenv('BASE_PATH')
ALL_PATHES_FILENAME = os.getenv('ALL_PATHES_FILENAME')
FILEPATH = os.path.join(BASE_PATH, ALL_PATHES_FILENAME)


def start_opening():
    if not os.path.exists(FILEPATH):
        logger.error('files not exist')
        input()
        return 0
    with open(FILEPATH, 'r', encoding='utf-8') as fileobj:
        all_tg_pathes = fileobj.readlines()

    os.system('cls')
    print(f'Found {len(all_tg_pathes)} telegrams:')
    print('-press [ENTER] to open next telegram')
    print(f'-enter number to go to certain tg (0-{len(all_tg_pathes)-1})')
    print('-enter [q] to exit')

    num = 0
    already_open = False

    while True:
        choise = input('')

        if choise == 'q':
            break

        if choise.isdigit():
            num = int(choise)
            if 0 <= num < len(all_tg_pathes):
                tmp_path = all_tg_pathes[num].strip()
                logger.info(f'{tmp_path}')
                subprocess.Popen(tmp_path)
                already_open = True
            else:
                logger.error('wrong number')

        if choise == '':
            
                if already_open:
                    num += 1
                    already_open = False
                if 0 <= num < len(all_tg_pathes):
                    tmp_path = all_tg_pathes[num].strip()
                    logger.info(f'{tmp_path}')
                    subprocess.Popen(tmp_path)
                    num += 1
            

            

