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
import os

from system_hotkey import SystemHotkey
import tkinter as tk
from foo.json_dict_pickle_transfer import load_pickle
from foo.get_all_infos import get_all_infos
from foo.mythreads import MyThreadManage
from random import sample


class TkManage:

    def __init__(self, root):
        self.root = root

        # 其他变量
        self.mtm = MyThreadManage()

        # 【信息变量】
        # 是否读取的到数据
        self.flag = True
        # 当前播放
        self.current_movie = None
        # 顺序播放指针
        self.indicator = -1
        # 播放历史
        self.play_list = []

        # 是否置顶的标签
        self.cb_top = tk.BooleanVar()

        # 资源导入
        self.movies, self.actors = self.mtm.create_thread_and_run(self.load_resources, need_return=True)

        # 快捷键注册
        self.register_hk()

    def load_resources(self):
        print('【初始化】更新资源中...')
        try:
            get_all_infos()
            return load_pickle('m'), load_pickle('a')
        except:
            print('【初始化】你没有资源或者路径配置错误...')
            self.flag = False
            return None, None

    def flag_check(self):
        """检查是否读取到有效的资源"""
        if not self.flag:
            print('【初始化】你没有资源或者路径配置错误...')
            return False
        else:
            return True

    def set_top(self):
        """设置置顶"""
        current_top_situation = not self.cb_top.get()
        self.cb_top.set(current_top_situation)
        if current_top_situation:
            self.root.wm_attributes('-topmost', 1)
            print('【置顶】设置界面置顶...')
        else:
            self.root.wm_attributes('-topmost', 0)
            print('【置顶】取消界面置顶...')
        self.root.focus_force()

    def quit(self):
        """退出"""
        self.root.destroy()

    def get_next_movie(self):
        """获取下一个电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.indicator >= 0:
            self.play_list.append(self.current_movie)

        self.indicator += 1
        self.current_movie = self.movies[self.indicator]
        print('【下一个】' + self.current_movie.get_movie_info())

    def get_last_movie(self):
        """获取上一个历史电影，无法回头"""
        if not self.flag_check():
            return 'error: invalid resource'

        if len(self.play_list) > 0:
            self.current_movie = self.play_list.pop()
            print('【上一个】' + self.current_movie.get_movie_info())
        else:
            print('【上一个】没有上一个电影...')

    def play_movie(self):
        """播放当前电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        def temp_f():
            try:
                os.system(self.current_movie.get_path())
                print('【播放】' + self.current_movie.get_movie_info())
            except:
                print('【播放】播放路径错误...')

        self.mtm.create_thread_and_run(target=temp_f)

    def play_random_movie(self):
        """播放随机电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.current_movie is not None:
            self.play_list.append(self.current_movie)
        self.current_movie = sample(self.movies, 1)[0]
        self.play_movie()

    def register_hk(self):
        """注册快捷键绑定"""
        sh = SystemHotkey()
        sh.register(('alt', 't'), callback=lambda e: self.set_top())
        sh.register(('alt', 'w'), callback=lambda e: self.quit())
        sh.register(('alt', 'r'), callback=lambda e: self.play_random_movie())
        sh.register(('alt', 'e'), callback=lambda e: self.get_next_movie())
        sh.register(('alt', 'q'), callback=lambda e: self.get_last_movie())
        sh.register(('alt', 's'), callback=lambda e: self.play_movie())
        # sh.register(('alt', 'shift', 'r'), callback=lambda e: threading.Thread(target=reset_password).start())
