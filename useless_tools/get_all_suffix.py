#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: get_all_suffix.py
@time: 2021/11/29 10:26
@desc: 如果你不知道你目录下到底有哪些后缀的话，可以用这个工具查一查
"""

import os
from configs.config import BASE_PATH


def get_all_suffix():
    """获取当前目录下所有非文件夹 文件 的后缀集合"""
    suffixs = []
    for path in BASE_PATH:
        for root, _, files in os.walk(path):
            for file in files:
                suffix = os.path.splitext(file)[1]
                if suffix not in suffixs:
                    suffixs.append(suffix)

    print(suffixs)