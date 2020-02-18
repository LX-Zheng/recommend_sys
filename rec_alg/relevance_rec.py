# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 14:36 
# @Author : long 
# @File : relevance_rec.py

# 计算电影的相似度
import os
import numpy as np
from scipy.sparse import dok_matrix
import heapq

rec_num = 30

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))

train = f_path + "/output/train.txt"

f_train = open(train)

user_s = set()
video_s = set()
# 获取所有用户id和视频id 使用set避免重复
line = f_train.readline()
while line:
    d = line.split(",")
    user_id = int(d[0])
    video_id = int(d[1])
    user_s.add(user_id)
    video_s.add(video_id)
    line = f_train.readline()

f_train.close()

user = list(user_s)
video = list(video_s)

user_num = len(user)
video_num = len(video)

print("===================开始构建用户id索引==================")
uid2idx_map = dict()  # 获得用户id到index的映射关系，index从0开始编码
idx2uid_map = dict()  # 获得index到用户id的映射关系，index从0开始编码
index = 0
for uid in user:
    uid2idx_map[uid] = index
    idx2uid_map[index] = uid
    index += 1


print("===================开始构建视频id索引==================")
vid2idx_map = dict()  # 获得视频id到index的映射关系，index从0开始编码
idx2vid_map = dict()  # 获得index到视频id的映射关系，index从0开始编码
index = 0
for vid in video:
    vid2idx_map[vid] = index
    idx2vid_map[index] = vid
    index += 1

print("===================开始构建用户行为矩阵==================")
# 构建用户行为矩阵
Mat = dok_matrix((video_num, user_num), dtype=np.float32)  # 行是视频、列是用户

f_train = open(train)
line = f_train.readline()
i = 0
while line:
    print(i)
    i += 1
    d = line.split(",")
    user_id = int(d[0])
    video_id = int(d[1])
    score = int(d[2])
    u_idx = uid2idx_map[user_id]
    v_idx = vid2idx_map[video_id]
    Mat[v_idx, u_idx] = score
    line = f_train.readline()

f_train.close()
print("===================完成构建用户行为矩阵==================")

Mat_csr = Mat.tocsr()  # 压缩稀疏行矩阵

print("===================Mat_csr.shape==================")
print(Mat_csr.shape)


print("-----------video_num---------------")
print(video_num)


def top_n_max(vector, n):
    """
    给定一个数组，求该数组最大的n个值，及每个值对应的下标index.
    :param vector: 输入的数值型数组，类型 <type 'numpy.ndarray'>
    :param n: 输出最大值的个数
    :return: [[v1,v2,v3],[idx1,idx2,idx3]]
    """
    idx_ = heapq.nlargest(n, range(len(vector)), vector.take)
    res_ = vector[idx_]
    return [res_, idx_]


def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    inner_product = float(vector_a * vector_b.T)
    nom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = inner_product / nom
    return cos


cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))
data_f = f_path + "/output/similarity_rec.npy"

all_sim_map = dict()
for v1 in range(video_num):
    print(v1)
    vec1 = Mat_csr.getrow(v1)
    vec = np.zeros(video_num)  # 评分
    for v2 in range(video_num):
        if v1 == v2:
            val = 0
        else:
            vec2 = Mat_csr.getrow(v2)
            val = cos_sim(vec1.A, vec2.A)
        vec[v2] = val
    c = top_n_max(vec, rec_num)  # [[v1,v2,v3],[idx1,idx2,idx3]]
    original_vid = idx2vid_map[v1]
    sim = c[0]
    idx = c[1]
    vid = [idx2vid_map[k] for k in idx]
    res = zip(vid, sim)
    all_sim_map[original_vid] = res

print(len(all_sim_map))
np.save(data_f, all_sim_map)


# 相似推荐的数据结构如下：
# {2345: [(1905, 0.5), (2452, 0.3), (3938, 0.1)]}
