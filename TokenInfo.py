import json
from tkinter import messagebox
from tkinter.ttk import Frame

import httpx

from BaseWin import *


# ak权限信息查询
class TokenInfo(BaseWin):

    # 创建页面其他控件
    def __init__(self, p_win, title='默认窗口'):
        self.token_value = StringVar()
        self.appId = StringVar(value='--')
        self.ta_value = StringVar(value='--')
        self.tl = None
        super().__init__(p_win, title)

    def create_other_plugin(self):
        cfg = self.p_win.cfg
        print(cfg['choose_env'])
        v = [item for item in cfg['envs'] if item['name'] == cfg['choose_env']][0]
        print(v)
        self.appId.set(v['appId'])
        self.ta_value.set(v['tenantId'])
        token = Label(self.window_info, text="输入需要查询权限的token:", font=("", 10))
        token.grid(row=1, column=0, pady=5, padx=5)
        token_input = Entry(self.window_info, textvariable=self.token_value, width=50)
        token_input.grid(row=2, column=0, columnspan=1, pady=5, padx=5)
        # appid
        Label(self.window_info, text="appid:").grid(row=3, column=0, pady=5)
        appId = Entry(self.window_info, textvariable=self.appId)
        appId.grid(row=4, column=0, pady=5)
        # tenantid
        Label(self.window_info, text="tenantId:").grid(row=5, column=0, pady=5)
        ta = Entry(self.window_info, textvariable=self.ta_value)
        ta.grid(row=6, column=0, pady=5)
        search_btn = Button(self.window_info, text="查询", command=self.get_token_info)
        search_btn.grid(row=7, column=0, pady=5, padx=5)
        q = Frame(self.window_info, width=450, height=250, bg='grey')
        q.grid(row=8, columnspan=4, pady=4)
        tl = Listbox(q, selectmode=EXTENDED, width=100)
        tl.pack()
        sc = Scrollbar(q, width=15)
        sc.pack(side=RIGHT, fill=Y)
        tl.configure(yscrollcommand=sc.set)
        tl.pack(side=LEFT, fill=BOTH, expand=True)
        tl.bind('<Double-Button-1>', self.show_url)
        self.tl = tl
        print(self.tl)

    # 查询ak对应的信息
    def get_token_info(self):
        if len(self.token_value.get()) == 0:
            messagebox.showerror(title='错误', message='请先输入token')
            return
        cfg = self.p_win.cfg
        v = [item for item in cfg['envs'] if item['name'] == cfg['choose_env']][0]
        print(v)
        url = 'http://%s:%s/%s' % (v['host'], v['port'], v['auth_token_info'])
        print('请求url')
        d = {'accessToken': self.token_value.get(), 'appId': self.appId.get(), 'tenantId': self.ta_value.get()}
        try:
            print('开始网络请求')
            response = httpx.post(url, data=d)
        except Exception as e:
            pass
        r = ''
        res = response.json()
        print(response.text)
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
            self.p_win.write_log('读取token权限信息成功:' + str(res['result']))
            r = res['result']
        elif 'data' in res:
            if res['data'] == None:
                messagebox.showerror('错误', message='查询结果为空')
                return
            self.p_win.write_log('读取token权限信息成功:' + str(res['data']))
            r = res['data']
        else:
            self.p_win.write_log('读取token权限失败,可能是格式异常:' + response.json())
            return
        print(r)
        self.tl.delete(0, END)
        for t in r['authorities']:
            t1 = json.loads(t)
            self.tl.insert(END, t1['permissionUrl'])

    def show_url(self, event):
        messagebox.showinfo('权限信息', message=self.tl.get(self.tl.curselection()))


if __name__ == '__main__':
    root = Tk()
    TokenInfo(root, title='token权限信息查询')
    root.mainloop()
