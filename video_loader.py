class VideoLoader(object):
    def __init__(self, bvid)->None:
        self.bvid = bvid
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}
