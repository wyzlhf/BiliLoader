from subtitle_loader import SubtitleLoader
from subtitle_converter import SubtitleConverter

sl = SubtitleLoader('BV1Ds411v72M')
# sc=SubtitleConverter('01. Course Outline.json')

if __name__ == '__main__':
    sl.get_json_url()
    # sc.convert_subtitle()