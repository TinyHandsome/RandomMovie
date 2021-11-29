#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Liyingjun
@contact: 694317828@qq.com
@software: pycharm
@file: setup.py
@time: 2021/11/29 9:47
@desc: tk主程序
"""

import tkinter as tk
from configs.config import ICO_PATH, ROOT_GEOMETRY


root = tk.Tk()
root.title('自由之翼')
root.resizable(0, 0)
root.iconbitmap(ICO_PATH)
root.geometry(ROOT_GEOMETRY)

# 字体设置和配置设置
font_entry = ("microsoft yahei", 14)
font_button = ("microsoft yahei", 14)
font_label = ("microsoft yahei", 14)
label_width = 5

# 变量区
media_code = tk.StringVar()
topic = tk.StringVar()
actors = tk.StringVar()
cb_top = tk.BooleanVar()
new_password = tk.StringVar()