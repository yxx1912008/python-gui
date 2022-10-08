#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter.messagebox

from MainPage import *


def start():
    root = Tk()
    root.iconbitmap('favicon.ico')
    if not os.path.exists(cfg_path):
        print('配置文件不存在', cfg_path)
        root.withdraw()
        showerror = tkinter.messagebox.showerror(title="错误", message="配置文件未找到,程序退出！")
        if showerror:
            root.destroy()
    else:
        MainPage(root, cfg_path)

    root.mainloop()


# 配置文件路径
cfg_path = 'config.yaml'

if __name__ == '__main__':
    start()
