#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter.scrolledtext import *

from About import *
from AkInfo import *
from EncAndDec import EncAndDec
from Env import *
from TokenInfo import *


# 初始化主页面
class MainPage:
    def __init__(self, window_info, cfg_path):
        self.log = None
        self.window_info = window_info
        self.cfg_path = cfg_path
        self.menu_list = {0: '菜单', 1: '切换环境', 2: '关于', 3: '退出', 4: '配置加解密', 5: '查询ak权限', 6: '查询token权限'}
        self.init_window()

    def init_window(self):
        # 读取配置好的yaml文件
        with open(self.cfg_path, encoding='utf-8') as config:
            data = yaml.load(config.read(), Loader=yaml.FullLoader)
            print('读取到的配置文件:{}'.format(data))
            self.window_info.cfg = data
            self.window_info.title(data['app']['title'])
            # self.window_info.geometry('650x300+635+390')
            self.init_main_page()
            self.init_log()
            self.init_menu()

    # 初始化菜单
    def init_menu(self):
        menu = Menu(self.window_info)
        menu_file = Menu(menu)
        menu.add_cascade(label=self.menu_list[0], menu=menu_file)
        # 初始化about页面
        menu_file.add_command(label=self.menu_list[2], command=lambda: self.init_about(title=self.menu_list[2]))
        # 初始化 环境切换页面
        menu_file.add_command(label=self.menu_list[1], command=lambda: self.init_env(title=self.menu_list[1]))
        # 退出之前增加分割线
        menu_file.add_separator()
        menu_file.add_command(label=self.menu_list[3], command=self.window_info.destroy)
        self.window_info.config(menu=menu)

    # 初始化日志模块
    def init_log(self):
        text = ScrolledText(self.window_info, font=("", 10), width=80, height=10)
        text.grid(row=2, column=0, pady=10)
        text.config(bg='black', fg='green')
        self.window_info.log = text
        self.window_info.write_log = self.write_log
        self.window_info.clear_log = self.clear_log
        cls_log = Button(text='清空日志')
        cls_log.grid(row=2, column=1, columnspan=2)
        cls_log.bind('<Button-1>', self.clear_log)
        # 输入内容到日志控件
        self.write_log('日志模块初始化成功.\r\n当前激活配置为:%s' % self.window_info.cfg['choose_env'])

    def write_log(self, text=None):
        self.window_info.log.insert('end', text + '\r\n')

    # 清除日志内容
    def clear_log(self, event):
        self.window_info.log.delete(1.0, 'end')

    # 初始化关于页面
    def init_about(self, title):
        About(self.window_info, title)

    # 初始化环境切换
    def init_env(self, title):
        Env(self.window_info, title, self.window_info.cfg)

    # 初始化首页组件
    def init_main_page(self):
        enc = Button(text=self.menu_list[4], width=50, height=2)
        enc.bind('<Button-1>', self.go_enc)
        enc.grid(row=0, column=0, pady=10, padx=4, sticky=W, columnspan=1)
        # 按钮 前往查询ak权限
        ak_auth = Button(text=self.menu_list[5], width=50, height=2)
        ak_auth.bind('<Button-1>', self.get_ak_auth)
        ak_auth.grid(row=0, column=1, pady=10, padx=4, columnspan=1)
        # 按钮 前往查询token权限
        token_get = Button(text=self.menu_list[6], width=50, height=2)
        token_get.bind('<Button-1>', self.get_token_auth)
        token_get.grid(row=1, column=0, pady=10, padx=4, sticky=W, columnspan=1)

    # 调用加解密功能
    def go_enc(self, event):
        EncAndDec(self.window_info, self.menu_list[4])

    # 调用查询ak权限功能
    def get_ak_auth(self, event):
        AkInfo(self.window_info, self.menu_list[5])

    # 调用查询token权限功能
    def get_token_auth(self, event):
        TokenInfo(self.window_info, self.menu_list[6])
