#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser

from BaseWin import *


class About(BaseWin):

    def create_other_plugin(self):
        label = Label(self.window_info, text='本工具仅用于内部问题定位使用，提高定位速度。\r\n当前版本:%s' % self.p_win.cfg['app']['version'])
        label.grid(row=1, column=0, rowspan=1,
                   pady=10)
        mail = Label(self.window_info, fg='blue', text='邮箱:admin@mail.huochuankeji.com')
        mail.grid(row=2, column=0, rowspan=1,
                  pady=10)
        mail.bind('<Button-1>', lambda event: webbrowser.open('https://huochuankeji.com'))


if __name__ == '__main__':
    root = Tk()
    about = About(root, '关于')
    root.mainloop()
