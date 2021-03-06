#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: movie.py
@time: 2021/11/29 15:36
@desc: Movie类
"""

from dataclasses import dataclass


@dataclass
class Movie:
    plate_number: str
    episode: str
    c: str
    u: str
    topic: str
    name: str
    path: str

    def get_actor_name(self):
        return self.name

    def get_json(self):
        return self.__dict__

    def get_path(self):
        return self.path

    def get_movie_info(self):
        return (self.plate_number + self.episode + '：' + self.topic + '（' + self.name + '）').replace(' ', '')

    def get_movie_plate_num(self):
        return self.plate_number + self.episode

    def get_movie_actor_name(self):
        return self.name

    def get_movie_name(self):
        return self.topic

    def get_movie_other_info(self):
        return ' '.join([self.c, self.u])
