from mega import Mega
import os
from loguru import logger
import rarfile
import zipfile
import shutil
import time
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BASE_PATH = os.getenv('BASE_PATH')
TELEGRAM_EXE_PATH = os.getenv('TELEGRAM_EXE_PATH')
MEGA_LINKS_PATH = os.getenv('MEGA_LINKS_PATH')
ALL_PATHES_FILENAME = os.getenv('ALL_PATHES_FILENAME')
ARCHIVE_TYPE = os.getenv('ARCHIVE_TYPE')

rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\UnRAR.exe"

def download_zip_from_mega(url, path):
    mega = Mega()
    rar_path = mega.download_url(url, dest_filename=path)
    return rar_path


def create_custom_dir(path, counter):
    counted_path = os.path.join(path, str(counter))
    if not os.path.exists(counted_path):
        os.makedirs(counted_path)
    return counted_path


def set_counter(path):
    if not os.path.exists(path):
        return 0
    items = os.listdir(path)
    folders = [int(item) for item in items if os.path.isdir(os.path.join(path, item)) 
               and item.isdigit()]
    if len(folders) > 0:
        return max(folders) + 1
    return 0


def unpack_rar_zip(archive_path, destination):
    if ARCHIVE_TYPE == '.rar':
        with rarfile.RarFile(archive_path, 'r') as rar_ref:
            rar_ref.extractall(destination)
            files = rar_ref.namelist()
    elif ARCHIVE_TYPE == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as rar_ref:
            rar_ref.extractall(destination)
            files = rar_ref.namelist()
    root_foolder = files[0][:files[0].index('/')]
    return os.path.join(destination, root_foolder)


def copy_tg_exe(tg_exe_path ,tg_folder_path):
    shutil.copy(tg_exe_path, tg_folder_path)
    return os.path.join(tg_folder_path, tg_exe_path)


def save_tg_ready_path(telegram_path, path):
    file_path = os.path.join(path, ALL_PATHES_FILENAME)
    tg_absolute_path = os.path.join(os.getcwd(),telegram_path)
    with open(file_path, 'a', encoding='utf-8') as fileobj:
        fileobj.write(tg_absolute_path + '\n')
    

def start_creating():
    logger.info("START")

    with open(MEGA_LINKS_PATH, 'r', encoding='utf-8') as fileobj:
        mega_links_list = fileobj.readlines()

    for i in mega_links_list:
        mega_link = i.strip()

        counter = set_counter(BASE_PATH)
        path = create_custom_dir(BASE_PATH, counter)
        archive_name = 'tdata' + ARCHIVE_TYPE
        file_path = os.path.join(path, 'tdata.rar')

        rar_path = download_zip_from_mega(mega_link, file_path)
        tg_folder_path = unpack_rar_zip(rar_path, path)
        tg_ready_path = copy_tg_exe(TELEGRAM_EXE_PATH, tg_folder_path)

        save_tg_ready_path(tg_ready_path, BASE_PATH)
        logger.info(f"Account {counter} creacted")
        time.sleep(1)
