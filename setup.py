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
        发现：
            1. 宽度的优先级：子组件 > 父组件
            2. 所以，要设置label宽度来限制字体不要出去，而不是限制frame的宽度
        参考：
            1. (tkinter 界面常用颜色表单)[https://www.jianshu.com/p/480ff177b14b]
        todo
            1. 处理日志
            2. 完成界面
            3. 对不同的信息展示不同的颜色
"""

import tkinter as tk

from configs.config import *
from foo.tk_manage import TkManage, label_limit_length_check

root = tk.Tk()
root.title('自由之翼')
root.resizable(0, 0)
root.iconbitmap(ICO_PATH)
root.geometry(ROOT_GEOMETRY)
tkm = TkManage(root)

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
playmenu.add_command(label='▶ 播放', command=tkm.play_movie, accelerator='Alt+Space')
playmenu.add_command(label='⏭ 下一个', command=tkm.get_next_movie, accelerator='Alt+E')
playmenu.add_command(label='🔀 随机播放', command=tkm.play_random_movie, accelerator='Alt+R')
# 直达
menubar.add_command(label='⏮', command=tkm.get_last_movie)
menubar.add_command(label='▶', command=tkm.play_movie)
menubar.add_command(label='⏭', command=tkm.get_next_movie)
menubar.add_command(label='🔀', command=tkm.play_random_movie)

# -播放板块
f_main = tk.Frame(root, width=WIDTH_F_MAIN)

# -- 左侧栏
f_main_left = tk.Frame(f_main)
# 车牌号
l_plate_number = tk.Label(f_main_left, textvariable=tkm.plate_num, bg='pink', font=FONT_OTHER_LABEL,
                          width=WIDTH_L_PLATE_NUM)
l_plate_number.grid(row=0, column=0, sticky='wesn')
# 演员名称
l_actor_name = tk.Label(f_main_left, textvariable=tkm.actor_name, bg='coral', font=FONT_OTHER_LABEL,
                        width=WIDTH_L_ACTOR_NAME)
l_actor_name.grid(row=0, column=1, sticky='wesn')
tkm.actor_name.trace_add('write', lambda *args: label_limit_length_check(tkm.actor_name, LIMIT_WIDTH_ACTOR_NAME, l_actor_name))

# 其他信息
l_other_info = tk.Label(f_main_left, textvariable=tkm.other_info, bg='orangered', font=FONT_OTHER_LABEL,
                        width=WIDTH_L_OTHER_INFO)
l_other_info.grid(row=0, column=2, sticky='wesn')
# 电影名称
l_movie_name = tk.Label(f_main_left, textvariable=tkm.movie_name, bg='peachpuff', anchor='center', relief='sunken',
                        font=FONT_MOVIE_NAME, width=WIDTH_L_MOVIE_NAME)
l_movie_name.grid(row=1, column=0, columnspan=3, sticky='wesn')
tkm.movie_name.trace_add('write', lambda *args: label_limit_length_check(tkm.movie_name, LIMIT_WIDTH_MOVIE_NAME, l_movie_name))
f_main_left.pack(side='left', expand=True, fill='both')

# -- 右侧栏：演员表
f_main_right = tk.Frame(f_main)
sb_actors = tk.Scrollbar(f_main_right)
sb_actors.pack(side='right', fill='y')
lb_actors = tk.Listbox(f_main_right, listvariable=tkm.actor_names, setgrid=True, selectbackground='firebrick', width=WIDTH_LB_ACTORS, yscrollcommand=sb_actors.set)
lb_actors.pack(expand=True, fill='both')
sb_actors.configure(command=lb_actors.yview)
f_main_right.pack(side='left', expand=True, fill='both')
tkm.actor_lb = lb_actors
tkm.actor_lb.bind('<Button-1>', lambda e: tkm.choose_actor())
f_main.pack(side='top', expand=True, fill='both')

# -脚注板块
f_foot = tk.Frame(root, width=WIDTH_F_FOOT)
# 各种信息
l_info = tk.Label(f_foot, textvariable=tkm.l_info, width=WIDTH_L_INFO, anchor='w', bg='lightgrey')
l_info.pack(side='left', expand=True, fill='both')

# 作者
l_writer = tk.Label(f_foot, text='@李英俊小朋友', width=12, fg='grey', anchor='e', bg='lightgrey')
l_writer.pack(side='right')
l_writer.bind('<Button-1>', lambda e: tkm.open_readme())
f_foot.pack(side='top', expand=True, fill='both')

root.config(menu=menubar)
root.mainloop()
