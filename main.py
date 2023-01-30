from subtitle_loader import PlaylistSubtitleLoader
from video_loader import PlaylistVideoLoader
from subtitle_converter import convert_json_subtitle_to_srt_subtitle

# pvl=PlaylistVideoLoader('BV1f3411J7w4')

if __name__ == '__main__':
    # BVID: str = 'BV1pL411p7wp'  #History of Ancient and Modern Philosophy (Spring 2018)
    BVID: str = 'BV1Tq4y1X77M'  #History of Analytic Philosophy (Spring 2021)
    # BVID: str = 'BV1Ni4y1d7QW'  #【惠顿学院】西方哲学史-81讲-中英字幕可自选
    # 下载视频
    plv = PlaylistVideoLoader(BVID)
    plv.get_playlist_videos()
    # 下载字幕
    psl = PlaylistSubtitleLoader(BVID)
    psl.get_playlist_json_subtitles()

    convert_json_subtitle_to_srt_subtitle('./')
