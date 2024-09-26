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

<p align="center">
  <a href="https://github.com/AirTouch666/JustACalculator/blob/main/README.md">简体中文</a> | English
</p>

## ⚡️About

**A simple calculator for macOS🎉** The interface is simple and easy to use. I hope you like it 👻

## 💽Install Stable Version

[GitHub](https://github.com/AirTouch666/JustACalculator/releases) provides the installer, of course, you can also clone the code and compile it yourself.

### Install from [GitHub](https://github.com/AirTouch666/JustACalculator/releases)

Download the compressed package from [GitHub](https://github.com/AirTouch666/JustACalculator/releases), unzip the compressed package, and drag the app to the application folder

>#### ⚠️Note
>If the prompt **"JustACalculator.app" cannot be opened because Apple cannot check it for malicious software** appears, select **Open in Finder** in the **Finder**
### Install from Source Code
**Please move to [⌨️Local Development](#⌨️Local-Development)**

## ✨Features
- 🕹 Simple and intuitive graphical operation interface
- 🦄 Support for basic addition, subtraction, multiplication, and division operations
- ☑️ Support for history records
- 🎮 Support for shortcut keys
- 📋 Support for copy and paste
  
## 🖥Application Interface
![image](https://touchware.us.kg/%E6%9C%BA%E5%9C%BA%E6%8E%A8%E8%8D%90-%E9%AD%94%E6%88%92%E6%9C%BA%E5%9C%BA/justac.png)

## ⌨️Local Development

1. Clone the source code
```bash
git clone git@github.com:AirTouch666/JustACalculator.git
```
2. Install dependencies
```bash
pip install PyQt5
pip install pyinstaller
```
3. Use PyInstaller to package
```bash 
cd JustACalculator
pyinstaller -w -i icon/icon.icns --add-data "icon:icon" main.py
``` 

## 📜License
This project is licensed under the AGPL3.0 License. See the [LICENSE](https://github.com/AirTouch666/JustACalculator/blob/main/LICENSE) file for more details.
