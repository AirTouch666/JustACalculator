import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QClipboard


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.IS_CALC = False
        self.STORAGE = []
        self.MAXSHOWLEN = 13
        self.current_display = '0'

        self.initUI()

    def initUI(self):
        self.setWindowTitle('JustACalculator')
        self.setFixedSize(310, 450)  # Increased window size

        # Layouts
        vbox = QVBoxLayout()

        # Create a horizontal layout for the display and the copy button
        display_hbox = QHBoxLayout()

        # Copy Button
        self.copy_button = QPushButton(self)
        self.copy_button.move(10, 40)
        self.copy_button.setFixedSize(45, 45)
        copy_icon = QIcon('icon/copy.png')  # Load the icon from the SVG file
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setIconSize(self.copy_button.size())  # Set icon size to button size
        self.copy_button.clicked.connect(self.copyToClipboard)

        display_hbox.addWidget(self.copy_button)

        self.display_label = QLabel(self.current_display, self)
        self.display_label.setAlignment(
            Qt.AlignCenter | Qt.AlignRight)  # Centering the text both horizontally and vertically
        self.display_label.setStyleSheet("background-color: black; color: white; font-size: 30px;")
        self.display_label.setFixedHeight(70)  # Increased height of the display label

        display_hbox.addWidget(self.display_label)
        vbox.addLayout(display_hbox)

        button_size = (65, 45)  # Size of each button (width, height)

        buttons = [
            ['MC', 'MR', 'MS', 'M+', 'M-'],
            ['del', 'CE', 'C', '+/-', '√'],
            ['7', '8', '9', '/', '%'],
            ['4', '5', '6', '*', '1/x'],
            ['1', '2', '3', '+', '-'],
            ['0', ' ', '.', '^', '=']
        ]

        # Reduce layout margins to shift everything slightly to the left and down
        vbox.setContentsMargins(10, 30, 10, 10)  # Top, left, bottom, right

        # Reduce button spacing
        hbox = QHBoxLayout()
        hbox.setSpacing(-5)  # Set horizontal spacing to 5 pixels

        for row in buttons:
            hbox = QHBoxLayout()
            for button in row:
                btn = QPushButton(button, self)
                btn.clicked.connect(lambda checked, b=button: self.press(b))
                btn.setFixedSize(*button_size)  # Apply the new size
                hbox.addWidget(btn)
            vbox.addLayout(hbox)
        vbox.addSpacing(-8)
        self.setLayout(vbox)
        self.show()

    def copyToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_display)
        check_icon = QIcon('icon/check.png')  # 使用不同的图标来表示检查标记

        # 创建一个更大的图标，例如 48x48
        large_icon = check_icon.pixmap(45, 45)
        self.copy_button.setIcon(QIcon(large_icon))  # 将按钮图标设置为更大的图标
        self.copy_button.move(10, 40)

        # 使用样式表将图标稍微向下移动一点
        self.copy_button.setStyleSheet("QPushButton { icon-position: bottom center; }")

        # 使用 QTimer 在 1 秒后恢复原始图标和样式
        QTimer.singleShot(1000, lambda: self.restoreCopyButtonIcon())

    def restoreCopyButtonIcon(self):
        self.copy_button.setIcon(QIcon('icon/copy.png'))
        self.copy_button.setStyleSheet("")  # 清空样式表，移除自定义样式

    def press(self, button):
        if button.isdigit() or button == '.':
            self.pressNumber(button)
        elif button in ['+', '-', '*', '/', '%', '^', '+/-', '√', '1/x', 'MC', 'MR', 'MS', 'M+', 'M-', '=']:
            self.pressOperator(button)
        elif button == 'del':
            self.delOne()
        elif button == 'CE':
            self.clearCurrent()
        elif button == 'C':
            self.clearAll()

    def pressNumber(self, number):
        if self.IS_CALC:
            self.current_display = '0'
            self.IS_CALC = False
        if self.current_display == '0':
            self.current_display = number
        else:
            if len(self.current_display) < self.MAXSHOWLEN:
                self.current_display += number
        self.updateDisplay()

    def pressOperator(self, operator):
        if operator == '+/-':
            if self.current_display.startswith('-'):
                self.current_display = self.current_display[1:]
            else:
                self.current_display = '-' + self.current_display
        elif operator == '1/x':
            try:
                result = 1 / float(self.current_display)
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == '√':
            try:
                result = math.sqrt(float(self.current_display))
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == 'MC':
            self.STORAGE.clear()
        elif operator == 'MR':
            if self.IS_CALC:
                self.current_display = '0'
            self.STORAGE.append(self.current_display)
            expression = ''.join(self.STORAGE)
            try:
                result = eval(expression)
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == 'MS':
            self.STORAGE.clear()
            self.STORAGE.append(self.current_display)
        elif operator == 'M+':
            self.STORAGE.append(self.current_display)
        elif operator == 'M-':
            if self.current_display.startswith('-'):
                self.STORAGE.append(self.current_display)
            else:
                self.STORAGE.append('-' + self.current_display)
        elif operator == '^':
            self.STORAGE.append(self.current_display)
            self.STORAGE.append('**')  # '**' is used for exponentiation in Python
            self.IS_CALC = True
        elif operator in ['+', '-', '*', '/']:
            self.STORAGE.append(self.current_display)
            self.STORAGE.append(operator)
            self.IS_CALC = True
        elif operator == '%':
            result = float(self.current_display) / 100
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == '=':
            if self.IS_CALC:
                self.current_display = '0'
            self.STORAGE.append(self.current_display)
            expression = ''.join(self.STORAGE)
            try:
                result = eval(expression)
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.STORAGE.clear()
            self.IS_CALC = True
        self.updateDisplay()

    def modifyResult(self, result):
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        result = str(result)
        if len(result) > self.MAXSHOWLEN:
            if len(result.split('.')[0]) > self.MAXSHOWLEN:
                result = 'Overflow'
            else:
                result = result[:self.MAXSHOWLEN]
        return result

    def updateDisplay(self):
        self.display_label.setText(self.current_display)

    def clearAll(self):
        self.STORAGE.clear()
        self.IS_CALC = False
        self.current_display = '0'
        self.updateDisplay()

    def clearCurrent(self):
        self.current_display = '0'
        self.updateDisplay()

    def delOne(self):
        if self.IS_CALC:
            self.current_display = '0'
            self.IS_CALC = False
        if self.current_display != '0':
            if len(self.current_display) > 1:
                self.current_display = self.current_display[:-1]
            else:
                self.current_display = '0'
        self.updateDisplay()

    def keyPressEvent(self, event):
        key = event.key()

        if Qt.Key_0 <= key <= Qt.Key_9:  # Numbers 0-9
            self.pressNumber(str(key - Qt.Key_0))
        elif key == Qt.Key_Plus:
            self.pressOperator('+')
        elif key == Qt.Key_Minus:
            self.pressOperator('-')
        elif key == Qt.Key_Asterisk:
            self.pressOperator('*')
        elif key == Qt.Key_Slash:
            self.pressOperator('/')
        elif key == Qt.Key_Period:
            self.pressNumber('.')
        elif key == Qt.Key_Equal or key == Qt.Key_Return:
            self.pressOperator('=')
        elif key == Qt.Key_Backspace:
            self.delOne()
        elif key == Qt.Key_Percent:
            self.pressOperator('%')
        elif key == Qt.Key_AsciiCircum:  # '^'
            self.pressOperator('^')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())