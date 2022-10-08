#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *


# 基础窗口信息，属于二级窗口
class BaseWin:
    def __init__(self, p_win, title='默认窗口'):
        self.p_win = p_win
        self.title = title
        self.create_base_win()
        print('当前打开页面为:' + title)
        self.create_other_plugin()

    # 获取居中窗口初始化信息
    def get_win_position(self, width=650, height=300):
        screen_width = self.p_win.winfo_screenwidth()
        screen_height = self.p_win.winfo_screenheight()
        print("scree info h={},w={}".format(screen_height, screen_width))
        window_size = f'{width}x{height}+{round((screen_width - width) / 2)}+{round((screen_height - height) / 2)}'
        print(window_size)
        return window_size

    # 关闭创建的子窗口
    def close_second_win(self):
        print('监听到窗口关闭:' + self.title)
        # 重新显示主窗口
        self.p_win.deiconify()
        self.window_info.destroy()

    # 创建基础窗口
    def create_base_win(self):
        toplevel = Toplevel(self.p_win)
        toplevel.iconbitmap('favicon.ico')
        self.window_info = toplevel
        toplevel.title(self.title)
        # toplevel.geometry(self.get_win_position())
        # 隐藏父窗口
        self.p_win.withdraw()
        toplevel.wm_protocol(name='WM_DELETE_WINDOW', func=self.close_second_win)
        Label(toplevel, text=self.title, font=(None, 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        # toplevel.grid_columnconfigure(0, weight=1)

    # 用于初始化其他控件
    def create_other_plugin(self):
        pass
