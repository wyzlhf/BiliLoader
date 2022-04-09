from subtitle_loader import SubtitleLoader
from subtitle_converter import SubtitleConverter
from video_loader import PlaylistVideoLoader

# sl:SubtitleLoader = SubtitleLoader('BV1Ds411v72M')
# sc=SubtitleConverter('01. Course Outline.json')

pvl=PlaylistVideoLoader('BV1f3411J7w4')

if __name__ == '__main__':
    # sl.get_json_subtitle()
    # sc.convert_subtitle()
    # pvl.get_playlist()
    base_url='https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/84/43/571284384/571284384-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1649494609&gen=playurlv2&os=hwbv&oi=0&trid=449823d60109431a89b6f012360e88c0u&platform=pc&upsig=5267f12247d737a3bf7f8bbbf3a092b6&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=454570454&bvc=vod&nettype=0&orderid=0,2&agrr=1&bw=27453&logo=80000000'
    # pvl.get_playurl()
    pvl.get_one_video(base_url)