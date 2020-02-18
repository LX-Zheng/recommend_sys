# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 11:04 
# @Author : long 
# @File : transform2triple.py

# 将mini_training_set转换为三元组(userid，videoid，score) 写到data.txt
import os

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))
all_files = os.listdir(f_path + '/data/mini_training_set')

data = f_path + "/output/data.txt"
fp = open(data, "w")

for path in all_files:
    with open(f_path + "/data/mini_training_set/" + path, "r") as f:
        lines = f.readlines()
    video_id = lines[0].strip(':\n')
    for l in lines[1:]:
        user_score_time = l.strip('\n').split(',')
        user_id = user_score_time[0]
        score = user_score_time[1]
        fp.write(user_id + "," + video_id + "," + score + "\n")

fp.close()
