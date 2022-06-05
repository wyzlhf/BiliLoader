import os


def delete_temp_audio_and_video(path: str):
    if os.path.exists(path):
        os.remove(path)
        # print(f'{path}删除成功！')
    else:
        print("The file does not exist")


def rename_merged_video(old_path: str, new_path: str):
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        # print(f'文件*{old_path}*重名成功，重命名后的文件名为*{new_path}8')
    else:
        print("The file does not exist")


if __name__ == '__main__':
    ...
