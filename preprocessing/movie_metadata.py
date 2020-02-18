# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 10:05 
# @Author : long 
# @File : movie_metadata.py
import os
import numpy as np

cwd = os.getcwd()  # /User/long/Documents/recommend_sys/preprocessing
f_path = os.path.abspath(os.path.join(cwd, ".."))  # /User/long/Documents/recommend_sys

data = f_path + "/data/movie_titles.txt"

f_data = open(data, "r", encoding="ISO-8859-1")

metadata_map = dict()

line = f_data.readline()
while line:
    tmp = line.strip('\n').split(',')
    vid = int(tmp[0])
    year = tmp[1]
    title = tmp[2]
    metadata_map[vid] = (year, title)  # {1781:(2004,Noi the Albino), 1790:(1966,Born Free)}
    line = f_data.readline()

f_data.close()

store_path = f_path + "/output/movie_metadata.npy"
np.save(store_path, metadata_map)

print(metadata_map)
print(len(metadata_map))
