import json
from typing import Union, List, Dict

import requests
from requests import Session, Response


class SpaceAndChannelVideoLoader(object):
    ...


class PlaylistVideoLoader(object):
    '''
    1、通过传入参数BVID获取整个playlist情况，里面包含该playlist的aid和每个视频的cid，获取方法为：
        https://api.bilibili.com/x/web-interface/view/detail?bvid=BVID

        补充一种方法，请求https://api.bilibili.com/x/player/pagelist?bvid=BV1KL411K7cH&jsonp=jsonp，也能获取playlist详细信息
    2、通过
        https://api.bilibili.com/x/player/playurl?cid=571284384&bvid=BV1f3411J7w4&qn=80&type=&otype=json&fourk=1&fnver=0&fnval=4048
        代入session的方式请求获取json，里面包含了相应的视频和音频链接，下载最大的即可，后续如果有需要，再可以控制。
    3、获取baseURL，然后包括上请求的参数，比如reference等，去下载视频，要有标题啊（就是第一步中json的part部分，需要保存下来）


    '''

    def __init__(self, bvid: str) -> None:
        self.bvid: str = bvid
        self.headers: dict[str, str] = {
            'referer': f'https://www.bilibili.com/video/{self.bvid}?p=2',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        self.playlist_url: str = 'https://api.bilibili.com/x/web-interface/view/detail?bvid='
        # self.player_url:str=
        self.session: Union[Session, Session] = requests.Session()

    def get_playlist(self) -> List[Dict[int, str]]:
        '''
        获取playlist信息，从里面需要取到每个视频的标题，cid
        :return:
        '''

        playlist: Response = self.session.get(self.playlist_url + self.bvid, headers=self.headers)
        playlist_dict: dict = json.loads(playlist.text)
        pages: list = playlist_dict["data"]["View"]["pages"]

        playlist_content: List[Dict[int, str]] = []
        for page in pages:
            cid: int = page['cid']
            part: str = page['part']
            cid_part: dict = {'cid': cid, 'part': part}
            playlist_content.append(cid_part)
        # print(playlist_content)
        return playlist_content

    def get_playurl(self, cid: int = 571284044) -> str:
        player_url: str = f'https://api.bilibili.com/x/player/playurl?cid={cid}&bvid={self.bvid}&qn=80&type=&otype=json&fourk=1&fnver=0&fnval=4048'
        player: str = self.session.get(player_url).text
        player_dict: dict = json.loads(player)
        base_url_dict: dict = player_dict["data"]["dash"]["video"][0]
        base_url: str = base_url_dict['baseUrl']
        return base_url

    def get_one_video(self, base_url: str):
        response: Union[Response, Response] = self.session.get(base_url, headers=self.headers, stream=True)
        with open('aaa.mp4', 'wb') as f:
            f.write(response.content)
