# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 14:02 
# @Author : long 
# @File : hot_rec.py

# 将training_set转换为三元组(userid，videoid，score)
import os
import numpy as np

N = 30  # 推荐的数量

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))

train = f_path + "/output/train.txt"

m = dict()

f_train = open(train)

# 计算每个视频累计的评分之和
line = f_train.readline()
while line:

    d = line.split(",")
    video_id = int(d[1])
    score = int(d[2])

    if video_id in m:
        m[video_id] += score
    else:
        m[video_id] = score

    line = f_train.readline()

sorted_list = sorted(m.items(), key=lambda item: item[1], reverse=True)

f_train.close()
print(sorted_list[:N])

hot_rec_map = {"hot": sorted_list[:N]}
hot_path = f_path + "/output/hot_rec.npy"
np.save(hot_path, hot_rec_map)
