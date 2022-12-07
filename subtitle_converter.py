import json
import os
from typing import List


def ms_to_hours(millis) -> str:
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000

    return ("%d:%d:%d.%d" % (hours, minutes, seconds, lay))


class SubtitleConverter(object):
    def __init__(self, file_dir: str = 'subtitle.json') -> None:
        print('开始转换，请耐心等候。。。')
        self.file_dir = file_dir

    def convert_subtitle(self) -> None:
        # content_body: list = []
        with open(self.file_dir, 'r', encoding='utf8') as file:
            json_content: str = file.read()
            dict_content: dict = json.loads(json_content)
            content_body = dict_content['body']

        srt_dir: list = self.file_dir.split('.')[:-1]
        # print('srt_dir:',srt_dir)
        srt_dir_str: str = '.'.join(srt_dir) + '.srt'   #此处关系到使用什么符号连接文件，比如P5-4. Environment Setup中间是用现在的.还是什么
        # print('srt_dir_str:',srt_dir_str)
        for item in content_body:
            from_time: float = item['from']
            int_from_ms: int = int(from_time * 1000)
            start_time: str = ms_to_hours(int_from_ms).replace('.', ',')

            to_time: float = item['to']
            int_to_ms: int = int(to_time * 1000)
            end_time: str = ms_to_hours(int_to_ms).replace('.', ',')

            content: str = item['content']
            index = content_body.index(item) + 1
            formed_time = start_time + '-->' + end_time

            with open(srt_dir_str, 'a', encoding='utf-8') as srt:
                srt.write(str(index) + '\n')
                srt.write(formed_time + '\n')
                srt.write(content + '\n')
        print(f'{srt_dir_str}转换完成。。。')
        print('---------------------------------------------------')


if __name__ == '__main__':
    path: str = 'D:\CODE\PYTHON\sub'
    files_list: List[str] = os.listdir(path)
    json_files_list: list = []
    for file in files_list:
        if file[-4:] == 'json':
            json_files_list.append(file)
    for file_name in json_files_list:
        full_file_name: str = path +'\\'+ file_name
        print(full_file_name)
        sc = SubtitleConverter(full_file_name)
        # print(full_file_name)
        sc.convert_subtitle()
