import os
from typing import List

from subtitle_converter import SubtitleConverter


def delete_temp_audio_and_video(path: str):
    if os.path.exists(path):
        os.remove(path)
        # print(f'{path}删除成功！')
    else:
        print("The file does not exist")


def rename_merged_video(old_path: str, new_path: str):
    if os.path.exists(old_path):
        os.replace(old_path, new_path)
        # print(f'文件*{old_path}*重名成功，重命名后的文件名为*{new_path}8')
    else:
        print("The file does not exist")


def change_json_subtitle_to_srt(path: str):
    all_json_subtitle_file: list = []
    all_file: list = os.listdir(path)
    file: str
    for file in all_file:
        file_name_list: list = file.split('.')
        file_type = file_name_list[-1]
        if file_type == 'json':
            all_json_subtitle_file.append(file)
    print(all_json_subtitle_file)
    for json_file in all_json_subtitle_file:
        file_name = path + '\\' + json_file
        sc = SubtitleConverter(file_name)
        sc.convert_subtitle()


def delete_subtitle_with_string_in_title(path: str = './', string_in_title: str = '') -> None:
    file_names_list: List[str] = os.listdir(path)
    # print(file_names_list)
    for file_name in file_names_list:
        if string_in_title in file_name:
            full_name: str = path + '\\' + file_name
            os.remove(full_name)
            print('成功删除文件：', file_name)


def delete_subtitle_with_string_in_title_list(path: str, str_list: List[str]) -> None:
    file_names_list: List[str] = os.listdir(path)
    for str_name in str_list:
        for file_name in file_names_list:
            if str_name in file_name:
                full_name: str = path + '\\' + file_name
                os.remove(full_name)
                print('成功删除文件：', file_name)


if __name__ == '__main__':
    # delete_subtitle_with_string_in_title(
    #     'D:\VIDEO\【Udemy付费课程】Microservices with Node JS and React\【Udemy付费课程】Microservices with Node JS and React（P3）',
    #     # '.ai-zh'
    #     '.zh-CN'
    #     # '.zh-Hans'
    #     # '.ai-en'
    # )
    path: str = r'D:\VIDEO\Udemy - Building Modern Web Applications with Go (Golang) 2022-7\Udemy - Building Modern Web Applications with Go (Golang) 2022-7（16-21）完结'
    str_list: List[str] = ['.ai-zh', '.zh-CN', '.zh-Hans', '.ai-en']
    delete_subtitle_with_string_in_title_list(path, str_list)
