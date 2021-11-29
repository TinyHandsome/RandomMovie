#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: json_dict_transfer.py
@time: 2021/11/29 14:59
@desc: json和dict相互转化
"""
import json

from configs.config import JSON_SAVE_PATH
from foo.file_folder_deal import check_if_file_folder_exists


def save_dict_to_json(d: [dict]):
    check_if_file_folder_exists(JSON_SAVE_PATH)
    json_content = json.dumps(d, ensure_ascii=False, indent=4)
    with open(JSON_SAVE_PATH, 'w', encoding='utf-8') as f:
        f.write(json_content)
