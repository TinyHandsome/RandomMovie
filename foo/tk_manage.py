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
import datetime
import os

from system_hotkey import SystemHotkey
import tkinter as tk
from foo.json_dict_pickle_transfer import load_pickle
from foo.get_all_infos import get_all_infos
from foo.mythreads import MyThreadManage
from random import sample


def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')


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
        # 各种信息的值
        self.l_info = tk.StringVar()
        # 电影下拉菜单选项
        self.l_list_choose = tk.StringVar()
        # 所有演员名称
        self.actors = tk.StringVar()
        # 车牌+特殊编号
        self.plate_num = tk.StringVar()
        # 电影名称
        self.movie_name = tk.StringVar()
        # 演员名称
        self.actor_name = tk.StringVar()
        # 其他信息
        self.other_info = tk.StringVar()

        # 资源导入
        self.movies, self.actors = self.load_resources()

        # 快捷键注册
        self.register_hk()

    def decorate_run_movie(self, my_func):
        """获取电影前装饰器和后装饰器
        1. 检查是否有资源
        2. 运行函数
        3. 更新tk信息
        """
        def wrapper(*args, **kwargs):
            if not self.flag_check():
                return 'error: invalid resource'

            my_func()

            self.get_current_movie_info()

        return wrapper

    def print_info(self, info):
        current_time = get_current_time()
        result_info = '[' + current_time + ']' + info
        self.mtm.create_thread_and_run(lambda: self.l_info.set(result_info))

    def load_resources(self):
        """
        1. 导入资源
        2. 更新演员名称
        :return:
        """
        self.print_info('【初始化】更新资源中...')
        try:
            get_all_infos()
            movies, actors = load_pickle('m'), load_pickle('a')

            # 更新演员列表
            actor_names = [a.get_actor_name() for a in actors]
            self.actors.set(' '.join(actor_names))

            return movies, actors
        except:
            self.print_info('【初始化】你没有资源或者路径配置错误...')
            self.flag = False
            return None, None

    def flag_check(self):
        """检查是否读取到有效的资源"""
        if not self.flag:
            self.print_info('【播放前检查】你没有资源或者路径配置错误...')
            return False
        else:
            return True

    def set_top(self):
        """设置置顶"""
        current_top_situation = not self.cb_top.get()
        self.cb_top.set(current_top_situation)
        if current_top_situation:
            self.root.wm_attributes('-topmost', 1)
            self.print_info('【置顶】设置界面置顶...')
        else:
            self.root.wm_attributes('-topmost', 0)
            self.print_info('【置顶】取消界面置顶...')
        self.root.focus_force()

    def quit(self):
        """退出"""
        self.root.destroy()

    def get_current_movie_info(self):
        """获取当前电影的信息，并传给tk"""
        self.plate_num.set(self.current_movie.get_movie_plate_num())
        self.actor_name.set(self.current_movie.get_movie_actor_name())
        self.movie_name.set(self.current_movie.get_movie_name())
        self.other_info.set(self.current_movie.get_movie_other_info())

    def get_next_movie(self):
        """获取下一个电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.indicator >= 0:
            self.play_list.append(self.current_movie)

        self.indicator += 1
        self.current_movie = self.movies[self.indicator]
        # 填入信息到tk中
        self.get_current_movie_info()
        self.print_info('【下一个】' + self.current_movie.get_movie_info())

    def get_last_movie(self):
        """获取上一个历史电影，无法回头"""
        if not self.flag_check():
            return 'error: invalid resource'

        if len(self.play_list) > 0:
            self.current_movie = self.play_list.pop()
            # 填入信息到tk中
            self.get_current_movie_info()
            self.print_info('【上一个】' + self.current_movie.get_movie_info())
        else:
            self.print_info('【上一个】没有上一个电影...')

    def play_movie(self):
        """播放当前电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        self.print_info('【播放】' + self.current_movie.get_movie_info())

        def temp_f():
            try:
                os.system(self.current_movie.get_path())
            except:
                self.print_info('【播放】播放路径错误...')

        self.mtm.create_thread_and_run(target=temp_f)

    def play_random_movie(self):
        """播放随机电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.current_movie is not None:
            self.play_list.append(self.current_movie)
        self.current_movie = sample(self.movies, 1)[0]
        # 填入信息到tk中
        self.get_current_movie_info()
        self.play_movie()

    def open_readme(self):
        """打开readme"""
        self.print_info('【点击】正在打开README...')
        os.startfile('README.md')

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
