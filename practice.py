import requests
import os
import subprocess
from bs4 import BeautifulSoup

# Задание
# Необходимо расширить функцию переводчика так, чтобы она принимала следующие параметры:
#
# Путь к файлу с текстом;
# Путь к файлу с результатом;
# Язык с которого перевести;
# Язык на который перевести (по-умолчанию русский).
# У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком. Функция должна взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.
# Для переводов можно пользоваться API Yandex.Переводчик.

# Алгоритм решения
# 1.0 Получить список файлов с расширением .txt в папке Original
#  1.1 Для каждого файла построить путь до него + методом среза получить язык, с которого будет произведен перевод.
# 2.0 Для каждого файла из списка файлов запустить функцию переводчика, в которую передать: путь к файлу,
# путь с файлу с результатам, оригинальный язык, язык перевода ("RU")
#  2.1 При отсутствии папки Result создать ее и положить туда созданный файл с переводом.

def read_text(path_to_file):
    with open(path_to_file) as f:
        return f.read() # получили текст из файла



def translate_it(path_start, path_end, original_lang, res_lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    text = read_text(path_start) # переводимый текст
    translate_line = '{0}-{1}'.format(original_lang, res_lang) # направление перевода
    params = {
        'key': key,
        'lang': translate_line,
        'text': text
    }
    response = requests.post(url, params=params).json()

    with open (path_end, 'w') as f:
         f.write(response['text'][0])



def get_path(folder_name):
    """Функция получает на вход название папки и строит до нее путь,
    с условием, что эта папка лежит в той же директории, что
    и запускаемый файл.
    """

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name)


if __name__ == '__main__':
    print('********** START PROGRAMM **********')
    migrations_path = get_path('Original')  # Получили путь до фото в папке Original
    result_path = get_path('Result')  # Получили путь до папки с результатами, где сохраним переведенные файлы
    subprocess.call(['mkdir', 'Result']) # Создали папку для результатов перевода
    all_files_in_dir = os.listdir(migrations_path)  # Получили список всех фалйлов в директории migrations_path
    for file in all_files_in_dir:
        file_path = os.path.join(migrations_path, file) #  получить полный путь до файла
        file_path_end = os.path.join(result_path, file) # получить путь к файлу с результатом
        origin_lang = file[:-4].lower() # Получить язык, с которого будет осуществлен перевод методом среза
        translate_it(file_path, file_path_end, origin_lang, 'ru')
    print('Программа перевела {0} файла.'.format(len(all_files_in_dir)))
    print('********** END PROGRAMM **********')