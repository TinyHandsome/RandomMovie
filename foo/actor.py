#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: actor.py
@time: 2021/11/29 16:24
@desc: 演员Actor类
"""

from foo.movie import Movie
from dataclasses import dataclass


@dataclass
class Actor:
    name: str
    movies: [Movie]

    def get_json(self):
        return {self.name: [m.get_json() for m in self.movies]}
