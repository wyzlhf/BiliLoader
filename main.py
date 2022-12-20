from subtitle_loader import PlaylistSubtitleLoader
from video_loader import PlaylistVideoLoader
from subtitle_converter import convert_json_subtitle_to_srt_subtitle

# pvl=PlaylistVideoLoader('BV1f3411J7w4')

if __name__ == '__main__':
    BVID: str = 'BV1ha4y1a7hR'

    # 下载视频
    plv = PlaylistVideoLoader(BVID)
    plv.get_playlist_videos()
    # 下载字幕
    psl = PlaylistSubtitleLoader(BVID)
    psl.get_playlist_json_subtitles()

    convert_json_subtitle_to_srt_subtitle('./')
