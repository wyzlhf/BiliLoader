from subtitle_loader import PlaylistSubtitleLoader
from video_loader import PlaylistVideoLoader
from subtitle_converter import convert_json_subtitle_to_srt_subtitle

# pvl=PlaylistVideoLoader('BV1f3411J7w4')

if __name__ == '__main__':
    BVID: str = 'BV17D4y177hK'  # 为初学者构建完整的 Typescript React Fitness 应用程序
    # BVID: str = 'BV1j24y1D7ZR'   #用户体验设计概论【全集】中英文字幕 （高清）乔治亚理工学院
    # BVID: str = 'BV125411n7X3'   #[中英字幕] Python 神经网络 - TensorFlow2.0 课程
    # BVID: str = 'BV1oY411a7Fs'   #Docker 与 Node 最佳实践指南【中英字幕
    # BVID: str = 'BV1UU4y1A7mh'   #Docker 精通 Docker Mastery with Kubernetes +Swarm from a Docker Captain
    # BVID:str='BV1QW4y1L7zL'   #JavaScript数据结构
    # BVID:str='BV1v8411p7qe'   #【全网最好的无人驾驶】为进华为花大价钱买的无人驾驶课程
    # 下载视频
    plv = PlaylistVideoLoader(BVID)
    plv.get_playlist_videos()
    # 下载字幕
    psl = PlaylistSubtitleLoader(BVID)
    psl.get_playlist_json_subtitles()

    convert_json_subtitle_to_srt_subtitle('./')
