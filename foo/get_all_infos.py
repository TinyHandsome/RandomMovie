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
import re

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


def get_remove_suffix(file):
    """获取文件非后缀"""
    return os.path.splitext(file)[0]


def deal_long_name(long_name):
    """对文件名进行正则表达式的拆解"""
    # 【情况1】有车牌
    pattern1 = re.compile(r'(?P<plate_number>[\d\w]+-[\d]+)(?P<code>\w+)?(?P<c>-C)?'
                          '(?P<u>-uncensored)?(【(?P<topic>.*?)】)?(（(?P<name>.*?)）)?', re.I)
    result = pattern1.match(long_name)
    # 【情况2】无车牌，但有topic
    pattern2 = re.compile(r'(?P<plate_number>.*?)(?P<c>-C)?(?P<u>-uncensored)?【(?P<topic>.*?)】(（(?P<name>.*?)）)?', re.I)

    if result:
        params = result.groupdict()
    else:
        result = pattern2.match(long_name)
        if result:
            params = result.groupdict()
        else:
            # 【情况3】啥都不行
            params = None

    return params


def generate_single_movie_info_dict(result_dict: dict, path: str, actor_name: str):
    """将电影的信息转换为字典返回"""

    code = result_dict.get('code').lower()
    c = (result_dict.get('c') is not None) or ('ch' in code)

    # 检查完ch之后，去掉code中的ch
    code = code.replace('ch', '')

    if 'a' in code:
        episode = 'a'
    elif 'b' in code:
        episode = 'b'
    else:
        episode = '' if code is None else code

    def get_value_if_not_none_else_empty(key):
        """获取字典中的值，如果位空的话则为空字符串"""
        return result_dict.get(key) if result_dict.get(key) is not None else ''

    # 演员名处理
    name = actor_name
    if get_value_if_not_none_else_empty('name') != '':
        name = actor_name

    sub_data = {
        'plate_num': get_value_if_not_none_else_empty('plate_num'),
        'episode': episode,
        'c': '中文字幕' if c else '',
        'u': '无码' if result_dict.get('u') is not None else '有码',
        'topic': get_value_if_not_none_else_empty('topic'),
        'name': name,
        'path': path
    }

    return sub_data


def get_all_infos():
    """获取所有文件的信息"""
    data = []

    for path in BASE_PATH:
        seconds = os.listdir(path)

        for actor_name in seconds:
            second_path = os.path.join(path, actor_name)
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
                    long_name = get_remove_suffix(movie)
                    result_dict = deal_long_name(long_name)

                    # 如果没有成功匹配，就直接给个topic完事儿
                    if not result_dict:
                        result_dict['topic'] = long_name

                    # 开始写入数据
                    sub_data = generate_single_movie_info_dict(result_dict, third_path, actor_name)
                    data.append(sub_data)

    print(data)


if __name__ == '__main__':
    get_all_infos()