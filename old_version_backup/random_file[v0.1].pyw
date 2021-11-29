#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: random_file.py
@time: 2021/11/29 9:37
@desc:
"""

import os
import re
from random import sample
from functools import partial
import tkinter as tk
import threading
from system_hotkey import SystemHotkey

from configs.config import *


def get_file():
    """获取所有对应后缀的文件，并随机"""
    suffixs = []
    files = []
    for base in BASE_PATH:
        for root, _, fs in os.walk(base):
            for file in fs:
                suffix = os.path.splitext(file)[1]
                suffixs.append(suffix)

                if suffix in AIM_SUFFIX:
                    files.append(root + '/' + file)

    return sample(files, 1)[0].replace("\\", "/")


def get_word():
    words = [
        '兄弟，你很牛逼！',
        '给阿姨倒一杯卡布基诺！',
        '你在淦神魔？',
        '马老师发生甚么事了？',
        '从现在开始，这里叫做卢本伟广场！'
    ]
    return sample(words, 1)[0]


class ShowMachine:
    def __init__(self):
        self.aim_path = None
        self.ICO_PATH = ICO_PATH
        self.last_one = []
        self.sh = SystemHotkey()

        try:
            with open(PASSWORD_SAVE_PATH, 'rb') as f:
                self.password = str(f.read(), encoding='utf-8')
        except Exception as e:
            self.password = ''

        self.font_entry = ("microsoft yahei", 14)
        self.font_button = ("microsoft yahei", 14)
        self.font_label = ("microsoft yahei", 14)
        self.label_width = 5

    def get_password(self):
        """获取密令"""

        if self.password == '':
            self.show()
            return

        root = tk.Tk()
        root.title('自由之翼')
        root.resizable(0, 0)
        root.iconbitmap(self.ICO_PATH)
        root.geometry('+900+300')

        def confirm_code():
            """检查是否有密码，有的话验证"""
            if code.get() == self.password:
                root.destroy()
                self.show()
            else:
                e1.delete(0, tk.END)

        code = tk.StringVar()
        e1 = tk.Entry(root, textvariable=code, font=self.font_entry)
        e1.pack(side=tk.LEFT, fill=tk.Y)
        e1.focus_set()
        b1 = tk.Button(root, text='确定', font=self.font_button, command=confirm_code)
        b1.pack(side=tk.LEFT)

        root.bind_all("<Return>", lambda e: confirm_code())
        root.mainloop()

    def show(self):
        root = tk.Tk()
        root.title('自由之翼')
        root.iconbitmap(self.ICO_PATH)
        root.resizable(0, 0)
        root.geometry('+900+300')

        media_code = tk.StringVar()
        topic = tk.StringVar()
        actors = tk.StringVar()
        cb_top = tk.BooleanVar()
        new_password = tk.StringVar()

        def place_path():
            """
            将当前视频链接的分割为 番号，主题，演员
                1. 如果没有演员，则使用父文件夹名
            """
            file_path, file_name = os.path.split(self.aim_path)
            father_folder_name = file_path.split(r'/')[-1]

            # 通过正则表达式获取内容
            aim_pattern = re.compile(r'(?P<media_code>.*?)(?:【(?P<topic>.*)】)?(?:（(?P<actors>.*)）)?\..*')
            result_dcit = aim_pattern.match(file_name).groupdict()

            def get_dict_value(key):
                return result_dcit.get(key) if result_dcit.get(key) != None else ''

            media_code.set(get_dict_value('media_code').lower())
            topic.set(get_dict_value('topic'))
            actors.set(get_dict_value('actors') if get_dict_value('actors') != '' else father_folder_name)

        def set_path():
            if self.aim_path:
                self.last_one.append(self.aim_path)
            self.aim_path = get_file()

            place_path()

        def open_movie():
            def om():
                try:
                    os.startfile(self.aim_path)
                except Exception as e:
                    media_code.set('路径错误！')

            t = threading.Thread(target=lambda: om())
            t.start()

        def set_last_one():
            if self.last_one:
                self.aim_path = self.last_one.pop(-1)
                place_path()

        def random_open():
            self.aim_path = get_file()
            media_code.set(get_word())
            open_movie()

        def set_top():
            current_situation = cb_top.get()
            if current_situation:
                root.wm_attributes('-topmost', 1)
            else:
                root.wm_attributes('-topmost', 0)
            root.focus_force()

        def set_top_key():
            r1.toggle()
            set_top()

        def reset_password():
            """重新设置密令"""
            top = tk.Toplevel()
            top.geometry('+900+300')
            top.iconbitmap(self.ICO_PATH)
            top.title('重制密令')

            def save_file():
                with open(PASSWORD_SAVE_PATH, 'wb') as g:
                    self.password = new_password.get()
                    g.write(bytes(self.password, encoding='utf-8'))
                media_code.set('密令已重置')
                top.destroy()

            ee1 = tk.Entry(top, textvariable=new_password, font=self.font_entry)
            ee1.pack(side=tk.LEFT, fill=tk.Y)
            bb1 = tk.Button(top, text='确定', font=self.font_button, command=save_file)
            bb1.pack(side='left')
            ee1.focus_set()

        f1 = tk.Frame(root)
        f2 = tk.Frame(root)
        f3 = tk.Frame(root)
        f4 = tk.Frame(root)

        b4 = tk.Button(f1, text='上一个(q)', font=self.font_button, command=set_last_one)
        b4.pack(side='left')

        b2 = tk.Button(f1, text='打开(s)', font=self.font_button, command=open_movie)
        b2.pack(side='left')

        b1 = tk.Button(f1, text='下一个(e)', font=self.font_button, command=set_path)
        b1.pack(side='left')

        b5 = tk.Button(f1, text='摇一个(r)', font=self.font_button, command=random_open)
        b5.pack(side='left')

        r1 = tk.Checkbutton(f1, text='置顶(t)', font=self.font_button, variable=cb_top, onvalue=True, offvalue=False,
                            command=set_top)
        r1.select()
        r1.pack(side='left')
        # 初始化

        b3 = tk.Button(f1, text='关闭(w)', font=self.font_button, command=root.destroy)
        b3.pack(side='right', fill=tk.X, expand=True)
        b7 = tk.Button(f1, text='重制密令(R)', font=self.font_button,
                       command=lambda: threading.Thread(target=reset_password).start())
        b7.pack(side='right', fill=tk.X, expand=True)

        f1.grid(row=0, column=0)

        mylabel = partial(tk.Label, width=self.label_width, font=self.font_label, justify=tk.CENTER)
        myentry = partial(tk.Entry, font=self.font_entry)

        l1 = mylabel(f2, text='番号')
        l1.pack(side=tk.LEFT, fill=tk.Y)
        e1 = myentry(f2, textvariable=media_code)
        e1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        f2.grid(row=1, column=0, sticky='nswe')

        l2 = mylabel(f3, text='主题')
        l2.pack(side=tk.LEFT, fill=tk.Y)
        e2 = myentry(f3, textvariable=topic)
        e2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        f3.grid(row=2, column=0, sticky='nswe')

        l3 = mylabel(f4, text='演员')
        l3.pack(side=tk.LEFT, fill=tk.Y)
        e3 = myentry(f4, textvariable=actors)
        e3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        f4.grid(row=3, column=0, sticky='nswe')

        self.sh.register(('alt', 'w'), callback=lambda e: root.destroy())
        self.sh.register(('alt', 'r'), callback=lambda e: random_open())
        self.sh.register(('alt', 'e'), callback=lambda e: set_path())
        self.sh.register(('alt', 'q'), callback=lambda e: set_last_one())
        self.sh.register(('alt', 's'), callback=lambda e: open_movie())
        self.sh.register(('alt', 't'), callback=lambda e: set_top_key())
        self.sh.register(('alt', 'shift', 'r'), callback=lambda e: threading.Thread(target=reset_password).start())

        root.mainloop()


if __name__ == '__main__':
    sm = ShowMachine()
    sm.get_password()
