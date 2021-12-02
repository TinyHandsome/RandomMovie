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
        1. [SystemHotkey快捷键对应表](https://blog.csdn.net/u013595395/article/details/107650130)
"""
import datetime
import os
import time
import traceback
import copy

from system_hotkey import SystemHotkey
import tkinter as tk
from foo.json_dict_pickle_transfer import load_pickle
from foo.get_all_infos import get_all_infos
from foo.mythreads import MyThreadManage
from configs.config import TEST_MODE
from random import randint


def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')


def label_limit_length_check(tk_var: tk.StringVar, limit: int, label: tk.Label):
    """长度限制检查"""
    if len(tk_var.get()) > limit:
        label.configure(anchor='w')
    else:
        label.configure(anchor='center')


def get_listbox_curselection(lb, lb_set):
    """获取listbox的选项，以及在数组中的值"""
    select_index = lb.curselection()[0]
    # 演员名称
    select_name = lb.get(select_index)
    if isinstance(lb_set, dict):
        result = lb_set.get(select_name)
    elif isinstance(lb_set, list):
        result = lb_set[select_index]
    else:
        result = None

    return select_name, result


class TkManage:

    def __init__(self, root):
        self.root = root

        # 其他变量
        self.mtm = MyThreadManage()

        # 【信息变量】
        # 是否记录日志
        self.is_log = True
        # 是否读取的到数据
        self.flag = True
        # 当前播放
        self.current_movie = None
        # 历史指针
        self.indicator_history = -1
        # 顺序播放指针
        self.indicator = -1
        # 播放指针历史
        self.play_list = []

        # 是否置顶的标签
        self.cb_top = tk.BooleanVar()
        # 各种信息的值
        self.l_info = tk.StringVar()
        # 车牌+特殊编号
        self.plate_num = tk.StringVar()
        # 电影名称
        self.movie_name = tk.StringVar()
        # 演员名称
        self.actor_name = tk.StringVar()
        # 其他信息
        self.other_info = tk.StringVar()
        # 演员listbox变量
        self.actor_lb = None
        # 所有演员名称
        self.actor_names = tk.StringVar()
        # 电影listbox变量
        self.movies_lb = None
        # 所有电影名称
        self.movie_names = tk.StringVar()

        # 初始化界面
        self.init_tk()
        # 资源导入
        self.movies, self.actors = self.load_resources()
        # 设置电影从这个电影集中抽取
        self.movie_set = None
        self.update_movie_set(copy.deepcopy(self.movies))

        # 快捷键注册
        self.register_hk()

    def decorate_run_movie(self, my_func):
        """测试，未实装
        获取电影前装饰器和后装饰器
        1. 检查是否有资源
        2. 运行函数
        3. 更新tk信息
        """

        def wrapper(*args, **kwargs):
            if not self.flag_check():
                return 'error: invalid resource'

            my_func()

            self.update_tk_current_movie_info()

        return wrapper

    def print_info(self, info):
        """在脚注输出信息"""
        current_time = get_current_time()
        result_info = '[' + current_time + ']' + info
        self.mtm.create_thread_and_run(lambda: self.l_info.set(result_info))

    def load_resources(self):
        """ 初始化资源的过程
        1. 导入资源
        2. 更新演员名称
        :return:
        """
        try:
            # 用测试来控制，是否更新本地数据
            if not TEST_MODE:
                get_all_infos()
                self.print_info('【初始化】更新资源中...')
            else:
                self.print_info('【初始化】获取本地资源中...')
            movies, actors = load_pickle('m'), load_pickle('a')

            # 更新演员列表
            actor_names = actors.keys()
            self.actor_names.set(' '.join(actor_names))
            # 更新电影列表
            movie_infos = [m.get_movie_info() for m in movies]
            self.movie_names.set(' '.join(movie_infos))

            self.print_info('【初始化】获取资源完毕...')

            return movies, actors
        except Exception as e:
            if self.is_log:
                traceback.print_exc()
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

    def init_tk(self):
        """初始话界面"""
        self.plate_num.set('车牌号')
        self.actor_name.set('演员名')
        self.movie_name.set('电影名')
        self.other_info.set('其他')

    def update_tk_current_movie_info(self):
        """获取当前电影的信息，并传给tk"""
        self.plate_num.set(self.current_movie.get_movie_plate_num())
        self.actor_name.set(self.current_movie.get_movie_actor_name())
        self.movie_name.set(self.current_movie.get_movie_name())
        self.other_info.set(self.current_movie.get_movie_other_info())

    def get_next_movie(self):
        """顺序获取下一个电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.current_movie and self.indicator >= 0:
            self.play_list.append(self.indicator)

        self.indicator += 1
        if self.indicator < len(self.movie_set):
            ...
        else:
            self.print_info('【下一个】没有下一个啦，从头循环哦...')
            self.indicator = 0

        self.update_movie_curse()
        self.current_movie = self.movie_set[self.indicator]
        # 填入信息到tk中
        self.update_tk_current_movie_info()
        self.print_info('【下一个】' + self.current_movie.get_movie_info())

    def get_last_movie(self):
        """获取上一个历史电影，无法回头"""
        if not self.flag_check():
            return 'error: invalid resource'

        if len(self.play_list) > 0:
            self.indicator = self.play_list.pop()
            self.update_movie_curse()
            self.current_movie = self.movie_set[self.indicator]
            # 填入信息到tk中
            self.update_tk_current_movie_info()
            self.print_info('【上一个】' + self.current_movie.get_movie_info())
        else:
            self.print_info('【上一个】没有上一个电影...')

    def play_movie(self):
        """播放当前电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.current_movie:
            self.print_info('【播放】' + self.current_movie.get_movie_info())
        else:
            self.print_info('【播放】未选择电影...')

        def temp_f():
            try:
                os.system(self.current_movie.get_path())
            except:
                self.print_info('【播放】播放路径错误...')

        self.mtm.create_thread_and_run(target=temp_f)

    def random_movie(self):
        """播放随机电影"""
        if not self.flag_check():
            return 'error: invalid resource'

        if self.current_movie and self.indicator >= 0:
            self.play_list.append(self.indicator)

        self.indicator = randint(0, len(self.movie_set))
        self.update_movie_curse()
        self.current_movie = self.movie_set[self.indicator]
        # 填入信息到tk中
        self.update_tk_current_movie_info()
        self.print_info('【随机】' + self.current_movie.get_movie_info())

    def open_readme(self):
        """打开readme"""
        self.print_info('【点击】正在打开README...')
        os.startfile('README.md')

    def update_movie_set(self, new_movie_set):
        """更新movie set"""
        self.movie_set = new_movie_set
        # 重置指针
        self.indicator = -1
        # 更新movie set info
        movie_set_infos = self.get_movie_set_infos()
        self.movie_names.set(' '.join(movie_set_infos))

    def update_movie_curse(self):
        """更新电影指针的位置，选择演员之后，历史记录清零，注意：指针的历史记录不应该<0"""
        # 先清空之前的选择
        self.movies_lb.selection_clear(self.indicator_history)
        # 进行当前的选择
        self.movies_lb.see(self.indicator)
        self.movies_lb.selection_set(self.indicator)
        # 保存当前的选择为历史选择
        self.indicator_history = self.indicator

    def get_movie_set_infos(self):
        """获取所有电影的信息"""
        return [m.get_movie_info() for m in self.movie_set]

    def choose_actor(self):
        """点击选择演员，并历史记录清零"""

        def ca():
            # 清空历史记录
            self.play_list = []
            # 演员编号
            select_name, actor = get_listbox_curselection(self.actor_lb, self.actors)
            self.print_info('【点击】选择演员：' + select_name)
            # 更新movie set为该演员下的movie
            self.update_movie_set(actor.get_movies())
            # 获取第一个movie
            self.get_next_movie()

        self.mtm.create_thread_and_run(ca)

    def choose_movie(self):
        """点击选择电影"""

        def cm():
            # 电影编号
            select_name, self.current_movie = get_listbox_curselection(self.movies_lb, self.movie_set)
            self.update_tk_current_movie_info()
            self.print_info('【点击】选择电影：' + select_name)
            self.play_movie()

        self.mtm.create_thread_and_run(cm)

    def register_hk(self):
        """注册快捷键绑定"""
        sh = SystemHotkey()
        sh.register(('alt', 't'), callback=lambda e: self.set_top())
        sh.register(('alt', 'w'), callback=lambda e: self.quit())
        sh.register(('alt', 'r'), callback=lambda e: self.random_movie())
        sh.register(('alt', 'e'), callback=lambda e: self.get_next_movie())
        sh.register(('alt', 'q'), callback=lambda e: self.get_last_movie())
        sh.register(('alt', 'space'), callback=lambda e: self.play_movie())
        # sh.register(('alt', 'shift', 'r'), callback=lambda e: threading.Thread(target=reset_password).start())
