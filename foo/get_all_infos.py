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
from foo.actor import Actor
from foo.file_folder_deal import *
from foo.json_dict_pickle_transfer import *
from foo.movie import Movie


def deal_long_name(long_name):
    """对文件名进行正则表达式的拆解"""
    # 【情况1】有车牌
    pattern1 = re.compile(r'(?P<plate_number>[\d\w]+-[\d]+)(?P<code>[\w\d-]+)?(?P<c>-C)?'
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


def generate_single_movie_info_dict(result_dict: dict, path: str, actor_name: str) -> Movie:
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
    info_name = get_value_if_not_none_else_empty('name')
    if info_name != '':
        name = info_name

    movie = {
        'plate_number': get_value_if_not_none_else_empty('plate_number'),
        'episode': episode,
        'c': '中文字幕' if c else '',
        'u': '无码' if result_dict.get('u') is not None else '有码',
        'topic': get_value_if_not_none_else_empty('topic'),
        'name': name,
        'path': path
    }

    movie = Movie(**movie)

    return movie


def update_actor_info(actor_infos: dict, actor_name, movie_data):
    """处理值是list的字典"""
    current_actor_names = actor_infos.keys()

    if actor_name not in current_actor_names:
        actor_infos[actor_name] = (Actor(actor_name, [movie_data]))
    else:
        actor_infos[actor_name].set_movies(movie_data)


def get_actor_movies(actor_infos: dict, movie_data: Movie, folder_actors: list, folder_name_actor: str):
    """根据演员文件夹的名称，获得对应的电影信息"""
    # 直接演员名写入
    if folder_name_actor != '':
        update_actor_info(actor_infos, folder_name_actor, movie_data)
    else:
        # 不是的话，就要遍历寻找这个演员字符串中有没有演员列表中的演员，重复的也要包括
        for actor_name in folder_actors:
            if actor_name in movie_data.get_actor_name():
                update_actor_info(actor_infos, actor_name, movie_data)


def get_all_infos():
    """获取所有文件的信息"""
    # 总电影数据
    data = []
    # 文件夹演员名称列表
    folder_actors = []
    # 总文件夹演员数据
    actor_infos = {}

    for path in BASE_PATH:
        seconds = os.listdir(path)

        # 获取演员名命名的文件夹
        actor_names = [s for s in seconds if not s.startswith('_')]
        # 并入到总演员名中，并去重
        folder_actors.extend(actor_names)
        folder_actors = list(set(folder_actors))

        for folder_name_actor in seconds:
            second_path = os.path.join(path, folder_name_actor)
            # 只要文件夹
            if is_dir(second_path):
                # _开头的文件夹，无演员名
                if folder_name_actor.startswith('_'):
                    folder_name_actor = ''

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
                        movie_data = generate_single_movie_info_dict(result_dict, third_path, folder_name_actor)
                        # 加入到总movie中来
                        data.append(movie_data)
                        # 加工数据获得演员 对应的 所有数据，这里的演员名称只包含，文件夹的演员
                        get_actor_movies(actor_infos, movie_data, folder_actors, folder_name_actor)

    # 保存电影数据到json pickle
    save_movie_to_json(data, 'm')
    save_data_to_pickle(data, 'm')
    # 保存演员数据到json pickle
    save_movie_to_json(actor_infos, 'a')
    save_data_to_pickle(actor_infos, 'a')


if __name__ == '__main__':
    ...
