
## 自研工具框架

>本工具研发的目的就是在产品需求未出之前，但是仍然有需要的场景下快速实现相关工具
的可视化研发

    1.GUI采用python的亲儿子tkinter来实现，简单快捷。程序主文件为**App.py**
    2.使用本框架可以很快速的开发属于自己业务的GUI界面,只需要继承BaseWin即可。


1.程序主界面

![](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/1%E5%B7%A5%E5%85%B7%E4%B8%BB%E7%95%8C%E9%9D%A2.PNG "程序主界面")

2.程序关于界面

![](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/2.%E5%85%B3%E4%BA%8E%E9%A1%B5%E9%9D%A2.PNG "程序关于界面")

3.配置加解密
![](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/3.%E9%85%8D%E7%BD%AE%E5%8A%A0%E8%A7%A3%E5%AF%86.PNG)

4.ak对应权限查询
![](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/4.ak%E5%AF%B9%E5%BA%94%E6%9D%83%E9%99%90%E4%BF%A1%E6%81%AF%E6%9F%A5%E8%AF%A2.PNG)

5.查询token权限界面
![](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/5.%E6%9F%A5%E8%AF%A2token%E6%9D%83%E9%99%90.PNG)


基础框架完整演示动画
![gif.gif](https://huochuan.oss-cn-hangzhou.aliyuncs.com/hckj/code/python-gui/gif.gif "演示动画")



### 1.项目技术栈

    1.httpx用于进行网络请求
    2.PyYAML用于读取yaml文件
    3.pyinstaller用于编译exe文件在windows系统执行
    4.GUI使用python自带的tkinter框架实现

### 2.项目运行

```shell script
#建议使用python3.7或者以上版本
pip install -r requirements.txt
```

### 3.编译成windows支持的exe文件
pyinstaller有两种编译模式,一种支持命令行同步显示,一种直接显示，如果不了解，那就直接用第一种模式[编译不带命令行]

```shell script
#1.编译不带命令行
pyinstaller -F -i favicon.ico App.py
# 2.编译带命令行
pyinstaller -F -i -w favicon.ico App.py
```

### 4.内网离线使用
因为我们公司的特殊性，很多时候需要在内网开发，因此可以通过下面的方式把相关依赖导出,内网使用。
```shell script
#1.安装组件导出引入的依赖
pip install pipreqs
#2.导出安装包到指定目录
pip download -d ./lib -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
#3.内网离线导入
pip install --no-index --find-links=lib/ -r requirements.txt
#--find-links就是存放安装文件的目录
#-r是指按照requirements.txt这个文件去安装文件目录中找需要的安装包
```

### 5.python导出依赖清单

```shell script
#requirements.txt用来记录项目所有的依赖包和版本号。
pip freeze >requirements.txt
```