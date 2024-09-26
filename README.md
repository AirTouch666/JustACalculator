<p align="center">
  <img src="https://airpicture.pages.dev/file/f3830462cf36972feb846.png" alt="Static Badge" width="25%;" />
</p>
<p align="center">
  <b style="font-size: 24px;">JustACalculator</b>
</p>													             

<p align="center">
  <img src="https://img.shields.io/badge/language-Python-light" />
  <img src="https://img.shields.io/badge/IDE-Pycharm-light" />
  <img src="https://img.shields.io/badge/licence-AGPL3.0-orange" />
</p>



## ⚡️关于

**一个macOS平台下的计算器🎉** 界面简洁易用，希望大家喜欢 👻
## 💽安装稳定版
[GitHub](https://github.com/AirTouch666/JustACalculator/releases)提供了已经编译好的安装包，当然你也可以自己克隆代码编译打包。

### 从[GitHub](https://github.com/AirTouch666/JustACalculator/releases)安装
[GitHub](https://github.com/AirTouch666/JustACalculator/releases)下载压缩包，将压缩包解压后的 app 拖入应用程序文件夹
>#### ⚠️注意 Attention
>如果提示**无法打开“JACalc.app”，因为Apple无法检查其是否包含恶意软件**，在**访达中右键选择打开**即可
### 从源码安装
**请移步至[⌨️本地开发](#⌨️-本地开发)**

## ✨特性
- 🕹 简洁明了的图形操作界面
- 🦄支持基本的加减乘除运算
- ☑️支持历史记录
- 🎮支持快捷键
- 📋支持复制粘贴
## 🖥应用界面
![image](https://touchware.us.kg/%E6%9C%BA%E5%9C%BA%E6%8E%A8%E8%8D%90-%E9%AD%94%E6%88%92%E6%9C%BA%E5%9C%BA/justac.png)

## ⌨️本地开发
1.克隆源码
```bash
git clone git@github.com:AirTouch666/JustACalculator.git
```
2.安装依赖
```bash
pip install PyQt5
pip install pyinstaller
```
3.使用PyInstaller打包
```bash
cd JustACalculator
pyinstaller -w -i icon/icon.icns --add-data "icon:icon" main.py
```
