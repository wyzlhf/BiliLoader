import subprocess

import requests

old_path:str='D:\\Statistics 110: Probability 概率论 哈佛大学（中英）\\Lecture 1: Probability and Counting | Statistics 110'
if ':' in old_path:
    new_path:str=old_path.replace(':','_')
    print(new_path)
