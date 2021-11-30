#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: tk_manage.py
@time: 2021/11/30 9:33
@desc: 管理tk的一些函数和计数
"""

from system_hotkey import SystemHotkey
import tkinter as tk
from foo.json_dict_pickle_transfer import load_pickle


class TkManage:

    def __init__(self, root):
        self.root = root
        # 是否置顶的标签
        self.cb_top = tk.BooleanVar()

        # 资源导入
        self.movies = load_pickle('m')
        self.actors = load_pickle('a')
        print(self.movies)
        print('---\n\n\n')
        print(self.actors)

        # 快捷键注册
        self.register_hk()

    def set_top(self):
        current_top_situation = self.cb_top.get()
        if current_top_situation:
            self.root.wm_attributes('-topmost', 1)
        else:
            self.root.wm_attributes('-topmost', 0)
        self.root.focus_force()

    def quit(self):
        self.root.destroy()

    def register_hk(self):
        """注册快捷键绑定"""
        sh = SystemHotkey()
        sh.register(('alt', 't'), callback=lambda e: self.set_top())
        sh.register(('alt', 'w'), callback=lambda e: self.quit())
        # sh.register(('alt', 'r'), callback=lambda e: random_open())
        # sh.register(('alt', 'e'), callback=lambda e: set_path())
        # sh.register(('alt', 'q'), callback=lambda e: set_last_one())
        # sh.register(('alt', 's'), callback=lambda e: open_movie())
        # sh.register(('alt', 'shift', 'r'), callback=lambda e: threading.Thread(target=reset_password).start())


