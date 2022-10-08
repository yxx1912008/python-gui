from tkinter import messagebox
from tkinter.ttk import Frame

import httpx

from BaseWin import *


# ak权限信息查询
class AkInfo(BaseWin):

    # 创建页面其他控件
    def __init__(self, p_win, title='默认窗口'):
        self.ak_value = StringVar()
        self.sk = StringVar(value='--')
        self.no_auth = StringVar(value='--')
        self.lb = None
        super().__init__(p_win, title)

    def create_other_plugin(self):
        ak = Label(self.window_info, text="输入需要查询权限的ak:", font=("", 10))
        ak_input = Entry(self.window_info, textvariable=self.ak_value, width=50)
        ak_input.grid(row=2, column=0, columnspan=1, pady=5, padx=5)
        ak.grid(row=1, column=0, pady=5, padx=5)
        search_btn = Button(self.window_info, text="查询", command=self.get_ak_info)
        search_btn.grid(row=3, column=0, pady=5, padx=5)
        Label(self.window_info, text="sk:").grid(row=4, column=0, pady=5)
        sk = Label(self.window_info, textvariable=self.sk)
        sk.grid(row=5, column=0, pady=5)
        Label(self.window_info, text="是否免鉴权:").grid(row=6, column=0, pady=5)
        na = Label(self.window_info, textvariable=self.no_auth)
        na.grid(row=7, column=0, pady=5)
        Label(self.window_info, text="权限列表:").grid(row=8, column=0, pady=5)
        f = Frame(self.window_info, width=450, height=250, bg='grey')
        f.grid(row=9, columnspan=4, pady=4)
        # EXTENDED：可以使listbox支持shift和Ctrl
        lb = Listbox(f, selectmode=EXTENDED, width=100)
        lb.pack()
        # 滚动条
        sc = Scrollbar(f, width=15)
        sc.pack(side=RIGHT, fill=Y)
        # 配置
        lb.configure(yscrollcommand=sc.set)
        lb.pack(side=LEFT, fill=BOTH, expand=True)
        lb.bind('<Double-Button-1>', self.show_url)
        self.lb = lb

    # 查询ak对应的信息
    def get_ak_info(self):
        if len(self.ak_value.get()) == 0:
            messagebox.showerror(title='错误', message='请先输入ak')
            return
        cfg = self.p_win.cfg
        print(cfg['choose_env'])
        v = [item for item in cfg['envs'] if item['name'] == cfg['choose_env']][0]
        print(v)
        url = 'http://%s:%s/%s' % (v['host'], v['port'], v['auth_ak_info'])
        print(url)
        try:
            response = httpx.post(url, data=self.ak_value.get())
        except Exception as e:
            self.p_win.write_log('查询ak信息失败,当前配置文件:{}'.format(v))
            messagebox.showerror(title='错误', message='查询ak信息失败,检查网络')
            return
        res = response.json()
        print(response.text)
        r = ''
        if 'statusCode' in res:
            if res['statusCode'] != '200':
                messagebox.showerror(title='错误', message=res['message'])
                return
        if 'code' in res:
            if res['code'] != '6100000':
                messagebox.showerror(title='错误', message=res['message'])
                return
        if 'result' in res:
            if res['result'] == None:
                messagebox.showerror('错误', message='查询结果为空')
                return
            self.p_win.write_log('读取ak权限信息成功:' + str(res['result']))
            r = res['result']
        elif 'data' in res:
            if res['data'] == None:
                messagebox.showerror('错误', message='查询结果为空')
                return
            self.p_win.write_log('读取ak权限信息成功:' + str(res['data']))
            r = res['data']
        else:
            self.p_win.write_log('读取ak权限失败,可能是格式异常:' + response.json())
            return
        print(r)
        self.sk.set(r['secretKey'])
        print('需要鉴权' if not r['noAuth'] else '免鉴权')
        self.no_auth.set('需要鉴权' if not r['noAuth'] else '免鉴权')
        self.lb.delete(0, END)
        for t in r['methodAndUrls']:
            str_split = t.split('$$')
            s = '方法:%s,url:%s' % (str_split[0], str_split[1])
            self.lb.insert(END, s)

    # 绑定事件
    def show_url(self, event):
        messagebox.showinfo('鉴权信息', message=self.lb.get(self.lb.curselection()))


if __name__ == '__main__':
    root = Tk()
    AkInfo(root, title='ak资源信息查询')
    root.mainloop()
