# -*- coding: utf-8 -*- 
# @Time : 2020/2/17 11:25 
# @Author : long 
# @File : sampling.py

# 将三元组(userid，videoid，score)数据，按照7：3的比例随机分为训练集和测试集
import os
from random import random

cwd = os.getcwd()
f_path = os.path.abspath(os.path.join(cwd, ".."))

data = f_path + "/output/data.txt"
test = f_path + "/output/test.txt"
train = f_path + "/output/train.txt"

f_train = open(train, 'w')
f_test = open(test, 'w')

f_data = open(data)
line = f_data.readline()
while line:
    rand = random()
    if rand < 0.7:
        f_train.write(line)
    else:
        f_test.write(line)

    line = f_data.readline()

f_data.close()
f_train.close()
f_test.close()




