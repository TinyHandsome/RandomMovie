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
from foo.tk_manage import TkManage

root = tk.Tk()
root.title('自由之翼')
root.resizable(0, 0)
root.iconbitmap(ICO_PATH)
root.geometry(ROOT_GEOMETRY)
tkm = TkManage(root)

# 字体设置和配置设置
font_entry = ("microsoft yahei", 14)
font_button = ("microsoft yahei", 14)
font_label = ("microsoft yahei", 14)

# 菜单栏
menubar = tk.Menu(root)
# 创建文件菜单
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=filemenu)
filemenu.add_checkbutton(label='置顶(t)', variable=tkm.cb_top, onvalue=True,
                         # font=font_button,
                         offvalue=False, command=tkm.set_top)
filemenu.add_separator()
filemenu.add_command(label='退出(w)', command=tkm.quit)

f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(root)
f4 = tk.Frame(root)

r1 = tk.Checkbutton(f1, text='置顶(t)', font=font_button, variable=tkm.cb_top, onvalue=True, offvalue=False,
                    command=tkm.set_top)
r1.deselect()
tkm.set_top()
r1.pack()

f1.pack()

root.config(menu=menubar)
root.mainloop()
