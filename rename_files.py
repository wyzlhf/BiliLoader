import os
from typing import List

def the_fist_rename(replaced_str: str,want_str:str=''):
    for file in os.listdir(path):
        file_name = os.path.join(path, file)
        new_file_name = os.path.join(path, file).replace(replaced_str, want_str)
        os.rename(file_name, new_file_name)


def the_second_rename():
    for file in os.listdir(path):
        file_name = os.path.join(path, file)
        new_file_name = os.path.join(path, file).replace(").mp4", ".mp4")
        os.rename(file_name, new_file_name)


def remove_some_type_file(file_path, file_type):
    _path, dirs, filename = os.walk(file_path)
    filenamelist = filename.split('.')
    if filenamelist[-1] == file_type:
        os.remove(os.path.join(file_path, filename))
def rename_file_name_according_location(file_path:str,location:int,replaced_str:str=' ',want_str:str='.')->None:
    file_name_list:List[str]=os.listdir(file_path)
    for file_name in file_name_list:
        file_name_with_path = os.path.join(path, file_name)
        if file_name[location]==replaced_str:
            new_file_name:str=file_name[:location]+want_str+file_name[location+1:]
            new_file_name_with_path:str=os.path.join(file_path,new_file_name)
            print(new_file_name)
            os.rename(file_name_with_path,new_file_name_with_path)

if __name__ == '__main__':
    path = r"D:\VIDEO\希勒【金融市场】【18课全双语高清】"
    replaced_str: str = '希勒【金融市场】【18课全双语高清】 ('
    # want_str:str='.zh-CN'
    the_fist_rename(
        replaced_str,
        # want_str
    )
    the_second_rename()
    # rename_file_name_according_location(path,6)
