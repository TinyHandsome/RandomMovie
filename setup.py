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
filemenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='文件', menu=filemenu)
filemenu.add_checkbutton(label='置顶', variable=tkm.cb_top, onvalue=True,
                         # font=font_button, , selectcolor='red',
                         offvalue=False, command=tkm.set_top, accelerator='Alt+T')
filemenu.add_separator()
filemenu.add_command(label='退出', command=tkm.quit, accelerator='Alt+W')
# 创建编辑菜单
editmenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='编辑', menu=editmenu)
# 创建播放菜单
last_one = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='⏮', menu=last_one, command=...)
play = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='▶', menu=play, command=...)
next_one = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='⏭', menu=next_one, command=...)
random_one = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='🔀', menu=random_one, command=...)

f1 = tk.Frame(root)
f_left = tk.Frame(root)
f_right = tk.Frame(root)
f4 = tk.Frame(root)


f1.pack()

root.config(menu=menubar)
root.mainloop()
