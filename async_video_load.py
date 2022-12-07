import json
from typing import Union

import requests
from requests import Session, Response


def get_playlist_info_json_file(BVID: str) -> str:
    headers: dict[str, str] = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "referer": "https://message.bilibili.com/"
    }
    base_url: str = f'https://www.bilibili.com/video/{BVID}'
    playlist_url: str = f'https://api.bilibili.com/x/web-interface/view/detail?bvid={BVID}'
    session: Union[Session, Session] = requests.Session()
    playlist: Response = session.get(playlist_url, headers=headers)
    playlist_dict:str=playlist.text
    print(playlist_dict)


async def get_bvid_list():
    ...


async def load_video_and_audio_by_bvid():
    ...


async def merge_video_and_audio():
    ...


def rename_merged_video():
    ...


if __name__ == '__main__':
    BVID: str = 'BV1KB4y1Q7fU'
    get_playlist_info_json_file(BVID)
