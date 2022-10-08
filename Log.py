from tkinter.scrolledtext import *

from BaseWin import *


# 用于读取远程日志
class Log(BaseWin):

    def create_other_plugin(self):
        text = ScrolledText(self.window_info, width=80, height=5, font=("", 10))
        text.grid(row=1, column=0, rowspan=2,
                  pady=158)
        text.insert('end', '日志模块初始化成功...\r\n')
        text.config(bg='black', fg='green')
        self.log = text

    # 输入内容到日志控件
    def write_log(self, text=None):
        self.log.insert('end', text + '\r\n')

    # 清除日志内容
    def clear_log(self):
        self.log.delete(1.0, 'end')


if __name__ == '__main__':
    root = Tk()
    log = Log(root, '首页日志模块')
    root.geometry('650x300+635+390')
    log.write_log(text='写入日志成功')
    log.clear_log()
    root.mainloop()
