#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: actor.py
@time: 2021/11/29 15:36
@desc: Actor类
"""

from dataclasses import dataclass


@dataclass
class Actor:
    plate_number: str
    episode: str
    c: str
    u: str
    topic: str
    name: str
    path: str
