#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: config.py
@time: 2021/11/29 9:37
@desc: 配置文件
"""
import os
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 视频根目录
BASE_PATH = ['G:/编程脚本/Movies']
# 视频格式限制
AIM_SUFFIX = ['.mkv', '.wmv', '.mp4', '.avi']
# 保存路径
JSON_SAVE_PATH = os.path.join(base_dir, 'temp/catalogue.json')
MOVIES_SAVE_PATH = os.path.join(base_dir, 'temp/movies.pickle')

# logo路径
ICO_PATH = os.path.join(base_dir, 'materials/自由之翼.ico')
# 窗口位置
ROOT_GEOMETRY = '+900+300'
# 密码保存位置
PASSWORD_SAVE_PATH = os.path.join(base_dir, 'configs/password')
