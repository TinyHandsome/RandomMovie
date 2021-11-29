#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: get_all_infos.py
@time: 2021/11/29 9:57
@desc: 获取所有文件的信息
"""
import os

from configs.config import BASE_PATH, AIM_SUFFIX


def is_dir(path):
    """检查路径是否是文件夹"""
    return os.path.isdir(path)


def is_file(path):
    """检查路径是否是文件"""
    return os.path.isfile(path)


def is_aim_suffix(file):
    """检查文件的后缀名是否是目标后缀"""
    suffix = os.path.splitext(file)[1]
    if suffix in AIM_SUFFIX:
        return True
    else:
        return False


def get_all_infos():
    """获取所有文件的信息"""
    for path in BASE_PATH:
        seconds = os.listdir(path)

        for actor_name in seconds:
            second_path = os.path.join(BASE_PATH, actor_name)
            # _开头的文件夹，无演员名
            if is_dir(second_path):
                if actor_name.startswith('_'):
                    actor_name = ''

            # 遍历三级目录
            thirds = os.listdir(second_path)
            for movie in thirds:
                third_path = os.path.join(second_path, movie)
                # 如果是文件，且后缀满足要求
                if is_file(movie) and is_aim_suffix(movie):

