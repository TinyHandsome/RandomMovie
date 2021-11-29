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
