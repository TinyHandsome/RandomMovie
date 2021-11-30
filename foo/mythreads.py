#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: mythreads.py
@time: 2021/11/30 10:42
@desc: 我的多线程
        [Python内置库：threading（多线程）](https://www.cnblogs.com/guyuyun/p/11185832.html)
        (Python如何从线程中返回值)[https://zhuanlan.zhihu.com/p/21458868]
"""

from threading import Thread
from types import FunctionType


class MyThread(Thread):
    """我的多线程类"""

    def __init__(self, target, args, daemon):
        super().__init__()
        self.target = target
        self.args = args
        self.daemon = daemon
        self.result = None

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        self.join()
        return self.result


class MyThreadManage:
    def __init__(self):
        self.total_threads = []

    def create_thread_and_run(self, target, args=(), daemon=False, need_return=False):
        t = MyThread(target=target, args=args, daemon=daemon)
        # 不需要守护线程，也不需要join等待运行完了才执行主线程
        self.total_threads.append(t)
        t.start()
        if need_return:
            return t.get_result()
