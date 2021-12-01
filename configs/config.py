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

# 是否开启测试模式
TEST_MODE = True

# 视频根目录
BASE_PATH = ['G:/编程脚本/Movies']
# 视频格式限制
AIM_SUFFIX = ['.mkv', '.wmv', '.mp4', '.avi']
# 保存路径
MOVIE_JSON_SAVE_PATH = os.path.join(base_dir, 'temp/movies.json')
MOVIE_PICKLE_SAVE_PATH = os.path.join(base_dir, 'temp/movies.pickle')
ACTOR_JSON_SAVE_PATH = os.path.join(base_dir, 'temp/actors.json')
ACTOR_PICKLE_SAVE_PATH = os.path.join(base_dir, 'temp/actors.pickle')

# logo路径
ICO_PATH = os.path.join(base_dir, 'materials/自由之翼.ico')
# 窗口位置
ROOT_GEOMETRY = '+900+300'
# 主体和脚注大小限制
WIDTH_F_MAIN, WIDTH_F_FOOT = None, None
# 左侧栏一些label的宽度设置
WIDTH_L_PLATE_NUM = 14
WIDTH_L_ACTOR_NAME = 40
WIDTH_L_OTHER_INFO = 20
WIDTH_L_MOVIE_NAME = WIDTH_L_PLATE_NUM + WIDTH_L_ACTOR_NAME + WIDTH_L_OTHER_INFO

# 脚注左侧label的长度与电影名保持一致
WIDTH_L_INFO = WIDTH_L_MOVIE_NAME

# 密码保存位置
PASSWORD_SAVE_PATH = os.path.join(base_dir, 'configs/password')
