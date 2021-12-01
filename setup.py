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
        todo
            1. 处理日志
            2. 完成界面
            3. 对不同的信息展示不同的颜色
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
playmenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='播放', menu=playmenu)
playmenu.add_command(label='⏮ 上一个', command=tkm.get_last_movie, accelerator='Alt+Q')
playmenu.add_command(label='▶ 播放', command=tkm.play_movie, accelerator='Alt+S')
playmenu.add_command(label='⏭ 下一个', command=tkm.get_next_movie, accelerator='Alt+E')
playmenu.add_command(label='🔀 随机播放', command=tkm.play_random_movie, accelerator='Alt+R')
# 直达
menubar.add_command(label='⏮', command=tkm.get_last_movie)
menubar.add_command(label='▶', command=tkm.play_movie)
menubar.add_command(label='⏭', command=tkm.get_next_movie)
menubar.add_command(label='🔀', command=tkm.play_random_movie)

# -播放板块
f_main = tk.Frame(root)

# -- 左侧栏
f_main_left = tk.Frame(f_main)
# 车牌号
l_plate_number = tk.Label(f_main_left, textvariable=tkm.plate_num, width=10)
l_plate_number.grid(row=0, column=0)
# 演员名称
l_actor_name = tk.Label(f_main_left, textvariable=tkm.actor_name)
l_actor_name.grid(row=0, column=1)
# 其他信息
l_other_info = tk.Label(f_main_left, textvariable=tkm.other_info, width=10)
l_other_info.grid(row=0, column=2)
# 电影名称
l_movie_name = tk.Label(f_main_left, textvariable=tkm.movie_name)
l_movie_name.grid(row=1, column=0, columnspan=3)
# 右侧选框演员对应的所有电影
temp_list = (1, 2, 3)
l_list = tk.OptionMenu(f_main_left, tkm.l_list_choose, *temp_list)
l_list.grid(row=2, column=0, columnspan=3, sticky='s')
f_main_left.pack(side='left')

# -- 右侧栏：演员表
f_main_right = tk.Frame(f_main)
lb_actors = tk.Listbox(f_main_right, listvariable=tkm.actors)
lb_actors.pack(expand=True, fill='both')
f_main_right.pack(side='left', expand=True, fill='both')

f_main.pack(side='top', expand=True, fill='both')

# -脚注板块
f_foot = tk.Frame(root)
# 各种信息
l_info = tk.Label(f_foot, textvariable=tkm.l_info, width=60, anchor='w', bg='lightgrey')
l_info.pack(side='left', expand=True, fill='both')
# 作者
l_writer = tk.Label(f_foot, text='@李英俊小朋友', width=12, fg='grey', anchor='e', bg='lightgrey')
l_writer.pack(side='right')
l_writer.bind('<Button-1>', lambda e: tkm.open_readme())
f_foot.pack(side='top')

root.config(menu=menubar)
root.mainloop()
