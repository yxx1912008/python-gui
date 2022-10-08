import os.path
from tkinter import ttk, messagebox

import yaml

from BaseWin import *


# 用来切换具体环境
class Env(BaseWin):

    # 创建切换环境页面
    def __init__(self, p_win, title='默认窗口', cfg=None):
        # 优先去读取配置
        self.cfg = cfg
        self.cv = None
        super().__init__(p_win, title)

    def create_other_plugin(self):
        tips = '请选择当前激活的环境\r\n选择前一定要确认当前网络可以连通！'
        self.cv = StringVar()
        label = Label(self.window_info, text=tips)
        label.grid(row=1, column=0, rowspan=1,
                   pady=10)
        combobox = ttk.Combobox(self.window_info, textvariable=self.cv)
        combobox.grid(row=2, column=0, rowspan=1,
                      pady=10)
        combobox["value"] = [item[key] for item in self.cfg['envs'] for key in item if key == 'name']
        v = [item for item in self.cfg['envs'] if item['name'] == self.cfg['choose_env']]
        print('当前配置的环境为:{}'.format(v))
        combobox.current(self.cfg['envs'].index(v[0]))
        combobox.bind("<<ComboboxSelected>>", lambda event: self.choose_env())

    def choose_env(self):
        # 根据名称读取配置全量信息
        # v = [item for item in self.cfg['envs'] if item['name'] == self.cv.get()][0]
        with open('config.yaml', 'w', encoding='utf-8') as f:
            self.cfg['choose_env'] = self.cv.get()
            f.write(yaml.dump(self.cfg, allow_unicode=True, sort_keys=False))
            messagebox.showinfo(title="操作成功", message="环境切换为:{}".format(self.cv.get()))



if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as config:
        config = yaml.load(config.read(), Loader=yaml.FullLoader)
        print('读取到的配置文件:{}'.format(config))
        root = Tk()
        about = Env(root, '切换环境', config)
        root.mainloop()
