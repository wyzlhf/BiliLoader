import json
from typing import Any, List, Dict, Tuple
import requests
from requests import Response


class PlaylistSubtitleLoader(object):
    '''
        字幕json格式链接：https://i0.hdslb.com/bfs/subtitle/b3eaf7b000edc13a0ff94b7335201fe9e01b61fe.json
        https://api.bilibili.com/x/player/v2?cid=542890058&aid=467084764&bvid=BV1KL411K7cH   需要cid，aid，bivid，
        然后，https://api.bilibili.com/x/player/pagelist?bvid=BV1KL411K7cH&jsonp=jsonp   里面有cid
        ###https://api.bilibili.com/x/player/pagelist?bvid=BV1KL411K7cH&jsonp=jsonp     这里可以获取playlist的所有cid
        https://api.bilibili.com/x/web-interface/view/detail?bvid=BV1KL411K7cH&aid=467084764&need_operation_card=1
        &web_rm_repeat=1&need_elec=1&out_referer=https%3A%2F%2Fwww.bilibili.com%2F
        此处可以获取整个包括playlist的该页面总览信息，其中包括推荐列表
        目前是使用手动也就是人肉的方式判断是否有字幕，如果改进可以加上自动判断是否存在字幕的逻辑
        '''

    def __init__(self, bvid: str) -> None:
        print('开始下载json文件，请耐心等候。。。')
        print('---------------------------------------------')
        self.bvid = bvid
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}

    def get_video_info(self) -> Tuple[int, list]:
        detail_url: str = 'https://api.bilibili.com/x/web-interface/view/detail?bvid=' + self.bvid
        playlist_info_res: Response = requests.get(detail_url, headers=self.headers)
        playlist_info_str: str = playlist_info_res.text
        playlist_info_dict: dict = json.loads(playlist_info_str)
        aid: int = playlist_info_dict["data"]["View"]["aid"]
        pages: List[Dict[str, Any]] = playlist_info_dict["data"]["View"]["pages"]
        cid_part_order_list: List[Dict[str, Any]] = []
        for item in pages:
            cid: int = item['cid']
            part: str = item['part']
            order: int = pages.index(item) + 1
            part_dict: Dict = {'cid': cid, 'part': part, 'order': order}
            cid_part_order_list.append(part_dict)
        return (aid, cid_part_order_list)

    def get_playlist_json_subtitles(self) -> None:
        aid, cid_part_order_list = self.get_video_info()

        for cid_part_order_dict in cid_part_order_list:
            cid: int = cid_part_order_dict['cid']
            player_url: str = f'https://api.bilibili.com/x/player/v2?cid={cid}&aid={aid}&bvid={self.bvid}'
            player_content: Response = requests.get(player_url, headers=self.headers)
            content_str: str = player_content.text
            content_dict: dict = json.loads(content_str)
            # 从此处开始如果没有字幕会报错
            try:
                subtitle_list_len = len(content_dict['data']['subtitle']['subtitles'])
                for i in range(subtitle_list_len):
                    subtitle_url: str = 'https:' + content_dict['data']['subtitle']['subtitles'][i]['subtitle_url']
                    subtitle_type: str = content_dict['data']['subtitle']['subtitles'][i]["lan"]
                    json_content_dict: dict = requests.get(subtitle_url).json()
                    json_content_str: str = json.dumps(json_content_dict)
                    subtitle_title: str = f'P{cid_part_order_list.index(cid_part_order_dict) + 1}-' \
                                          f'{cid_part_order_dict["part"]}.{subtitle_type}.json'
                    if ":" in subtitle_title:
                        subtitle_title = subtitle_title.replace(":", "：")
                    if '|' in subtitle_title:
                        subtitle_title = subtitle_title.replace('|', '-')
                    with open(subtitle_title, 'a') as json_file:
                        print('正在写入json文件：', subtitle_title)
                        json_file.write(json_content_str)
                        print(
                            f'第{cid_part_order_list.index(cid_part_order_dict) + 1}/{len(cid_part_order_list)}个字幕文件下载完成')
                        print('---------------------------------------------')
            except:
                print('该视频集没有字幕，请您再次确认')
