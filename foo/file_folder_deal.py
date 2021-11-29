#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: file_folder_deal.py
@time: 2021/11/29 15:15
@desc: 文件和文件夹处理
"""
import os
from configs.config import AIM_SUFFIX


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


def get_remove_suffix(file):
    """获取文件非后缀"""
    return os.path.splitext(file)[0]


def check_if_file_folder_exists(file_path):
    """检查文件路径是否存在，不存在就创建该路径"""
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(file_path)
