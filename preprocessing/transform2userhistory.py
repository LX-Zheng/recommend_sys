# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 11:40 
# @Author : long 
# @File : transform2userhistory.py

# 将mini_training_set转换用户播放历史，方便后续计算基于item-based协同过滤
import numpy as np
import os


def user_action_to_map(source_path, store_path):
    """
    将用户的行为转化为dict存储到磁盘，主要将train和test分别存起来
    train用做个性化推荐
    test用作离线评估
    :param source_path: 存放原始数据的路径
    :param store_path: 搜集用户行为后的存放路径，以dict的结构存放在txt文件
    :return: null
    """
    rec_map = dict()
    source = open(source_path, 'r')
    print("===================开始收集用户播放历史==================")
    line = source.readline()
    while line:
        d = line.split(",")
        user_id = int(d[0])
        video_id = int(d[1])
        score = int(d[2])
        if user_id in rec_map:
            s = rec_map.get(user_id)
            s.add((video_id, score))
            rec_map[user_id] = s
        else:
            s = set()
            s.add((video_id, score))
            rec_map[user_id] = s
        line = source.readline()
    source.close()

    print("===================完成收集用户播放历史==================")

    print(len(rec_map))
    np.save(store_path, rec_map)


cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))

train_path = f_path + "/output/train.txt"
test_path = f_path + "/output/test.txt"

train_store_path = f_path + "/output/train_play_action.npy"
test_store_path = f_path + "/output/test_play_action.npy"

user_action_to_map(train_path, train_store_path)
user_action_to_map(test_path, test_store_path)


# 最终的用户行为map数据结构如下：
# {2097129: set([(3049, 2), (3701, 4), (3756, 3)]), 1048551: set([(3610, 4), (571, 3)])}


