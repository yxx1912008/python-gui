import tkinter.messagebox
from tkinter.scrolledtext import *

import httpx

from BaseWin import *


# auth加解密工具
class EncAndDec(BaseWin):

    def __init__(self, p_win, title='默认窗口'):
        super().__init__(p_win, title)

    def create_other_plugin(self):
        self.window_info.minsize(350, 150)
        left = Label(self.window_info, text="待加密文本:", font=("", 10))
        left.grid(row=1, column=0, columnspan=1, pady=10, padx=10)
        l_text, r_text = ScrolledText(self.window_info, width=50, height=10), ScrolledText(self.window_info, width=50,
                                                                                           height=10)
        l_text.grid(row=2, column=0)
        r_text.grid(row=2, column=1)
        self.window_info.l_text, self.window_info.r_text = l_text, r_text
        right = Label(self.window_info, text="待解密文本:", font=("", 10))
        right.grid(row=1, column=1, columnspan=1, pady=10, padx=10)
        Button(self.window_info, text='加密', command=self.enc).grid(row=3, column=0, padx=10, pady=10)
        Button(self.window_info, text='解密', command=self.dec_str).grid(row=3, column=1, padx=10, pady=10)

    # 加密
    def enc(self):
        s = self.window_info.l_text.get('1.0', 'end-1c')
        if len(s) == 0 or s == '':
            tkinter.messagebox.showerror(title='错误', message='待加密字符串不能为空')
        else:
            cfg = self.p_win.cfg
            print(cfg['choose_env'])
            v = [item for item in cfg['envs'] if item['name'] == cfg['choose_env']][0]
            print(v)
            url = 'http://%s:%s/%s' % (v['host'], v['port'], v['auth_enc'])
            print(url)
            try:
                response = httpx.post(url, data=s)
                print(response.json())
            except Exception as e:
                self.p_win.write_log('加密失败,当前配置文件:{}'.format(v))
                tkinter.messagebox.showerror(title='错误', message='文本加密失败,检查网络')
                return
            res = response.json()
            r = ''
            if 'result' in res:
                self.p_win.write_log('加密成功,密文已复制到粘贴板:' + res['result'])
                r = res['result']
            elif 'data' in res:
                self.p_win.write_log('加密成功,密文已复制到粘贴板:' + res['data'])
                r = res['data']
            else:
                self.p_win.write_log('加密失败:' + response.json())
                tkinter.messagebox.showerror(title='错误', message='文本加密失败,查询日志')
                return
            self.window_info.clipboard_clear()
            self.window_info.clipboard_append(r)
            self.window_info.r_text.delete(1.0, 'end')
            self.window_info.r_text.insert('end', r)
            tkinter.messagebox.showinfo('操作成功', '操作成功,已复制到剪贴板')

# 解密
    def dec_str(self):
        s = self.window_info.r_text.get('1.0', 'end-1c')
        if len(s) == 0 or s == '':
            tkinter.messagebox.showerror(title='错误', message='待解密字符串不能为空')
        else:
            cfg = self.p_win.cfg
            print(cfg['choose_env'])
            v = [item for item in cfg['envs'] if item['name'] == cfg['choose_env']][0]
            print(v)
            url = 'http://%s:%s/%s' % (v['host'], v['port'], v['auth_dec'])
            print(url)
            try:
                response = httpx.post(url, data=s)
                print(response.json())
            except Exception as e:
                self.p_win.write_log('解密失败,当前配置文件:{}'.format(v))
                tkinter.messagebox.showerror(title='错误', message='文本解密失败,检查网络')
                return
            res = response.json()
            r = ''
            if 'statusCode' in res:
                if res['statusCode'] != '200':
                    tkinter.messagebox.showerror(title='错误', message=res['message'])
                    return
            if 'code' in res:
                if res['code'] != '6100000':
                    tkinter.messagebox.showerror(title='错误', message=res['message'])
                    return
            if 'result' in res:
                self.p_win.write_log('解密成功,密文已复制到粘贴板:' + res['result'])
                r = res['result']
            elif 'data' in res:
                self.p_win.write_log('解密成功,密文已复制到粘贴板:' + res['data'])
                r = res['data']
            else:
                self.p_win.write_log('解密失败:' + response.json())
                return
            self.window_info.clipboard_clear()
            self.window_info.clipboard_append(r)
            self.window_info.l_text.delete(1.0, 'end')
            self.window_info.l_text.insert('end', r)
            tkinter.messagebox.showinfo('操作成功', '操作成功,已复制到剪贴板')


if __name__ == '__main__':
    root = Tk()
    e = EncAndDec(root, '加解密工具')
    root.mainloop()
