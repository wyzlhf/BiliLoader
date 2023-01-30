import json
import re
import subprocess
from typing import Union, List, Dict
import requests
from bs4 import BeautifulSoup, ResultSet  # type: ignore
from requests import Session, Response
import os
from tenacity import retry
from time import sleep
from random import randint
from utils import delete_temp_audio_and_video, rename_merged_video
from typing import List, Dict


class SpaceAndChannelVideoLoader(object):
    ...


class PlaylistVideoLoader(object):
    def __init__(self, bvid: str) -> None:
        self.bvid: str = bvid
        self.headers: Dict[str, str] = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "referer": "https://message.bilibili.com/"
        }
        self.base_url: str = f'https://www.bilibili.com/video/{self.bvid}'
        self.playlist_url: str = f'https://api.bilibili.com/x/web-interface/view/detail?bvid={self.bvid}'
        self.session: Union[Session, Session] = requests.Session()
        self.plsylist_info: List[Dict] = self.get_playlist_info()

    def get_playlist_info(self) -> List[Dict]:
        playlist: Response = self.session.get(self.playlist_url, headers=self.headers)
        playlist_dict: dict = json.loads(playlist.text)
        pages: List[dict] = playlist_dict["data"]["View"]["pages"]
        # pprint(pages)

        playlist_content: List[Dict] = []
        for page in pages:
            cid: int = page['cid']
            part: str = page['part']
            page_url: str = f'{self.base_url}?p={page["page"]}'
            cid_part: dict = {'cid': cid, 'part': part, 'page': page_url}
            playlist_content.append(cid_part)
        # pprint(playlist_content)
        return playlist_content

    def send_request(self, url: str) -> Union[Response, Response]:
        response: Union[Response, Response] = requests.get(url=url, headers=self.headers)
        return response

    def get_video_data(self, html_data: str) -> list:
        json_data: str = re.findall(r'<script>window.__playinfo__=(.*?)</script>', html_data)[0]
        json_data_dict: dict = json.loads(json_data)
        audio_url: str = json_data_dict["data"]["dash"]["audio"][0]["backupUrl"][0]
        video_url: str = json_data_dict["data"]["dash"]["video"][0]["backupUrl"][0]
        video_data: list = [audio_url, video_url]
        return video_data

    def save_data(self, file_name: str, audio_url: str, video_url: str) -> None:
        print("正在下载 " + file_name + "的音频...")
        audio_data: bytes = self.send_request(audio_url).content
        print("完成下载 " + file_name + "的音频！")
        print("正在下载 " + file_name + "的视频...")
        video_data: bytes = self.send_request(video_url).content
        print("完成下载 " + file_name + "的视频！")
        with open(file_name + ".mp3", "wb") as f:
            f.write(audio_data)
        with open(file_name + ".mp4", "wb") as f:
            f.write(video_data)

    @retry()
    def get_video(self, url, filename):
        try:
            html_data: str = self.send_request(url).text
            video_data: list = self.get_video_data(html_data)
            self.save_data(filename, video_data[0], video_data[1])
        except:
            raise Exception
        return video_data

    # FFmpeg这个东西经常报错，很不好用，下面试一下使用moviepy的方法
    def merge_output_video(self, in_audio_name: str, in_video_name: str, out_video_name: str) -> None:
        print(f'开始合并{in_audio_name}&&{in_video_name}--->{out_video_name}')
        COMMAND = f'ffmpeg -i "{in_audio_name}.mp4" -i "{in_video_name}.mp3" -c:v copy -c:a aac -strict experimental "{out_video_name}.mp4"'
        process = subprocess.Popen(COMMAND, shell=True)
        process.wait()
        print(f'视频{out_video_name}合并完成')
        return

    # def merge_video_and_audio(self,in_audio_name: str, in_video_name: str, out_video_name: str) -> None:
    #     ...

    # def delete_temp_file(self, file_dir: str) -> None:
    #     os.remove(file_dir)
    #
    # def delete_temp_playlist(self):
    #     print('开始删除临时文件')
    #     playlist_content: List[Dict] = self.plsylist_info
    #     for item in playlist_content:
    #         file_name: str = item['part']
    #         temp_audio_name: str = file_name + '.mp3'
    #         self.delete_temp_file(temp_audio_name)
    #         temp_video_name: str = file_name + '.mp4'
    #         self.delete_temp_file(temp_video_name)
    #         print(f'临时文件{file_name}已删除')

    def get_playlist_videos(self):
        print('视频下载工作开始，请耐心等候。。。')
        playlist_content: List[Dict] = self.plsylist_info
        for item in playlist_content:
            url: str = item['page']
            file_name: str = item['part']
            print(file_name)
            if ":" in file_name:
                file_name = file_name.replace(":", "：")
            if '|' in file_name:
                file_name=file_name.replace('|','-')
            self.get_video(url, file_name)
            out_video_name: str = f'{file_name}_merged'
            self.merge_output_video(file_name, file_name, out_video_name)
            print(f'视频{file_name}下载合并完成，当前进度为{playlist_content.index(item) + 1}/{len(playlist_content)}')

            # sleep_time: int = randint(1, 50)
            # sleep(sleep_time)
            delete_temp_audio_and_video(f'{file_name}.mp3')
            print(f'删除临时文件{file_name}.mp3')
            delete_temp_audio_and_video(f'{file_name}.mp4')
            print(f'删除临时文件{file_name}.mp4')
            # 重新命名一下标题，主要是加上了序号，因为有些视频本身没有序号，找不到次序了，但是有些视频有，就会出现重复序号
            nature_index: int = playlist_content.index(item) + 1
            # rename_merged_video(f'{out_video_name}.mp4', f'{file_name}.mp4')
            # print(f'文件重命名成功，重命名后的文件名为：{file_name}.mp4')
            rename_merged_video(f'{out_video_name}.mp4', f'P{nature_index}-{file_name}.mp4')
            print(f'文件重命名成功，重命名后的文件名为：P{nature_index}-{file_name}.mp4')
            print('-------------------------------------------------')
        print('=========================所有视频下载合成完毕=========================')

    # def get_playlist_videos(self):
    #     self.get_videos()
    #     self.delete_temp_playlist()
