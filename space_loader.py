import requests
from subtitle_loader import PlaylistSubtitleLoader
from video_loader import PlaylistVideoLoader
from typing import List, Dict
import subprocess


def get_bvid_of_space_seriesdetail_list(url: str, num_pages: int = 1) -> list:
    space_parameter: Dict[str, str] = get_space_parameter(url)
    mid: str = space_parameter['mid']
    sid: str = space_parameter['sid']
    url_type: str = space_parameter['url_type']
    page_size: int = 30
    archives_list: list = []
    if url_type == 'collectiondetail':
        for page_number in range(num_pages):
            space_collectiondetail_api_url: str = f'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={mid}' \
                                                  f'&season_id={sid}&sort_reverse=false&page_num={page_number + 1}&page_size={page_size}'
            json_of_api_request: requests.Response = requests.get(space_collectiondetail_api_url)
            dict_of_api_request: dict = json_of_api_request.json()['data']['archives']
            archives_list.extend(dict_of_api_request)
    if url_type == 'seriesdetail':
        for page_number in range(num_pages):
            space_seriesdetail_api_url: str = f'https://api.bilibili.com/x/series/archives?mid={mid}&series_id={sid}' \
                                              f'&only_normal=true&sort=desc&pn={page_number}&ps={page_size}'
            json_of_api_request: requests.Response = requests.get(space_seriesdetail_api_url)
            dict_of_api_request: dict = json_of_api_request.json()['data']['archives']
            archives_list.extend(dict_of_api_request)
    return archives_list


def get_space_parameter(url: str) -> Dict[str, str]:
    splited_url_list: list = url.split('?')
    sid: str = splited_url_list[1].split('=')[1]
    splited_https_part_list: list = splited_url_list[0].split('/')
    url_type: str = splited_https_part_list[-1]
    mid: str = splited_https_part_list[3]
    space_parameter: dict = {}
    space_parameter['sid'] = sid
    space_parameter['mid'] = mid
    space_parameter['url_type'] = url_type
    return space_parameter


def get_number_of_pages(url: str) -> int:
    ...


if __name__ == '__main__':
    url: str = 'https://space.bilibili.com/1803865534/channel/collectiondetail?sid=862382'   #2 pages
    archives_list = get_bvid_of_space_seriesdetail_list(url, num_pages=2)
    # print(archives_list)
    # 此处开始是正常下载
    for item in archives_list:
        bvid: str = item['bvid']

        # 下载视频
        plv = PlaylistVideoLoader(bvid)
        plv.get_playlist_videos()
        # 下载字幕
        # psl = PlaylistSubtitleLoader(bvid)
        # psl.get_playlist_json_subtitles()
    print('=*=*=*=*=*=*=*=*=*=*=*=*SPACE VIDEOS DOWNLOAD COMPLETELY=*=*=*=*=*=*=*=*=*=*=*=*')
    # 此处结束是正常下载
    # 下面开始是使用you-get下载，临时策略，用后可删除
    # for archive in archives_list:
    #     bvid: str = archive['bvid']
    #     base_url: str = 'https://www.bilibili.com/video/'
    #     full_url: str = base_url + bvid
    #     subprocess.Popen(['you-get', full_url], shell=True).communicate()
