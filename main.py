from subtitle_loader import PlaylistSubtitleLoader
from video_loader import PlaylistVideoLoader

# pvl=PlaylistVideoLoader('BV1f3411J7w4')

if __name__ == '__main__':
    BVID: str = 'BV1Et4y1N7y7'

    # 下载视频
    # plv = PlaylistVideoLoader(BVID)
    # plv.get_playlist_videos()
    # 下载字幕
    psl = PlaylistSubtitleLoader(BVID)
    psl.get_playlist_json_subtitles()
