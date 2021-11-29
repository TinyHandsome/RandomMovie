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

from configs.config import MOVIE_JSON_SAVE_PATH, MOVIE_PICKLE_SAVE_PATH, ACTOR_JSON_SAVE_PATH, ACTOR_PICKLE_SAVE_PATH
from foo.file_folder_deal import check_if_file_folder_exists


def save_movie_to_json(data, c):
    """将数据集合保存到json中"""
    if c == 'm':
        path = MOVIE_JSON_SAVE_PATH
        result = [i.get_json() for i in data]
    elif c == 'a':
        path = ACTOR_JSON_SAVE_PATH
        result = [i.get_json() for i in data.values()]
    else:
        raise Exception('咨询管理员解决...')

    check_if_file_folder_exists(path)

    json_content = json.dumps(result, ensure_ascii=False, indent=4)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json_content)


def save_data_to_pickle(data, c):
    """将数据集合持久化到本地"""
    if c == 'm':
        path = MOVIE_PICKLE_SAVE_PATH
    elif c == 'a':
        path = ACTOR_PICKLE_SAVE_PATH
    else:
        raise Exception('咨询管理员解决...')

    check_if_file_folder_exists(path)
    with open(path, 'wb') as f:
        pickle.dump(data, f)
