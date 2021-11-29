#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: json_dict_pickle_transfer.py
@time: 2021/11/29 14:59
@desc: json和dict相互转化
"""
import json
import pickle

from configs.config import JSON_SAVE_PATH, MOVIES_SAVE_PATH
from foo.file_folder_deal import check_if_file_folder_exists


def save_movie_to_json(data):
    """将电影类集合保存到json中"""
    check_if_file_folder_exists(JSON_SAVE_PATH)
    movies = [i.__dict__ for i in data]
    json_content = json.dumps(movies, ensure_ascii=False, indent=4)
    with open(JSON_SAVE_PATH, 'w', encoding='utf-8') as f:
        f.write(json_content)


def save_movie_to_pickle(data):
    """将电影类集合持久化到本地"""
    check_if_file_folder_exists(JSON_SAVE_PATH)
    with open(MOVIES_SAVE_PATH, 'w') as f:
        pickle.dump(data, f)
