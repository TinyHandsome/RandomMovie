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
import re

from configs.config import BASE_PATH
from foo.file_folder_deal import *
from foo.json_dict_transfer import save_dict_to_json
from foo.actor import Actor


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

    c = False
    episode = ''

    code = result_dict.get('code')
    if code is not None:
        code = code.lower().strip()
        c = 'ch' in code
        # 检查完ch之后，去掉code中的ch
        code = code.replace('ch', '')

        # 再检查ab
        if 'a' in code:
            episode = 'a'
        elif 'b' in code:
            episode = 'b'
    c = (result_dict.get('c') is not None) or c

    def get_value_if_not_none_else_empty(key):
        """获取字典中的值，如果位空的话则为空字符串"""
        return result_dict.get(key).strip() if result_dict.get(key) is not None else ''

    # 演员名处理
    name = actor_name
    if get_value_if_not_none_else_empty('name') != '':
        name = actor_name

    movie = {
        'plate_number': get_value_if_not_none_else_empty('plate_number'),
        'episode': episode,
        'c': '中文字幕' if c else '',
        'u': '无码' if result_dict.get('u') is not None else '有码',
        'topic': get_value_if_not_none_else_empty('topic'),
        'name': name.strip(),
        'path': path
    }

    movie = Actor(**movie)

    return movie


def get_actor_movies(data):
    """根据演员文件夹的名称，获得对应的电影信息"""
    ...


def get_all_infos():
    """获取所有文件的信息"""
    data = []
    folder_actors = []

    for path in BASE_PATH:
        seconds = os.listdir(path)

        for actor_name in seconds:
            second_path = os.path.join(path, actor_name)
            # _开头的文件夹，无演员名
            if is_dir(second_path):
                if actor_name.startswith('_'):
                    actor_name = ''
                else:
                    folder_actors.append(actor_name)

            # 遍历三级目录
            thirds = os.listdir(second_path)
            for movie in thirds:
                third_path = os.path.join(second_path, movie)
                # 如果是文件，且后缀满足要求
                if is_file(third_path) and is_aim_suffix(movie):
                    long_name = get_remove_suffix(movie)
                    result_dict = deal_long_name(long_name)

                    # 如果没有成功匹配，就直接给个topic完事儿
                    if not result_dict:
                        result_dict = {'topic': long_name}

                    # 开始写入数据
                    movie_data = generate_single_movie_info_dict(result_dict, third_path, actor_name)
                    data.append(movie_data.__dict__)

    # 保存数据到JSON
    save_dict_to_json(data)
    # 加工数据获得演员 对应的 所有数据，这里的演员只包含，文件夹的演员
    # actor_infos = get_actor_movies(data)


if __name__ == '__main__':
    get_all_infos()
