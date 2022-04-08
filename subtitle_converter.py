import json


def ms_to_hours(millis)->str:
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000

    return ("%d:%d:%d.%d" % (hours, minutes, seconds, lay))


class SubtitleConverter(object):
    def __init__(self, file_dir: str = 'subtitle.json')->None:
        print('开始转换，请耐心等候。。。')
        self.file_dir = file_dir

    def convert_subtitle(self, ) -> None:
        content_body: list = []
        with open(self.file_dir, 'r', encoding='utf8') as file:
            json_content: str = file.read()
            dict_content: dict = json.loads(json_content)
            content_body = dict_content['body']

        srt_dir: list = self.file_dir.split('.')[:-1]
        srt_dir_str: str = ' '.join(srt_dir) + '.srt'
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
