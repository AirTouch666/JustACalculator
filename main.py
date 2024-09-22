import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QShortcut
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QClipboard, QKeySequence


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.IS_CALC = False
        self.STORAGE = []
        self.MAXSHOWLEN = 13
        self.current_display = '0'
        self.history = []
        self.initUI()
        self.setupShortcuts()
        self.setStyleSheet(self.getStyleSheet())

    def initUI(self):
        self.setWindowTitle('JustACalculator')
        self.setFixedSize(800, 600)  
        
        main_layout = QHBoxLayout()
        calc_layout = QVBoxLayout()
        calc_layout.setContentsMargins(20, 40, 20, 20)  
        calc_layout.setSpacing(10) 

        display_hbox = QHBoxLayout()
        display_hbox.setContentsMargins(0, 0, 0, 0) 

        self.copy_button = QPushButton(self)
        self.copy_button.setFixedSize(50, 50)
        copy_icon = QIcon('icon/copy.png')
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setIconSize(self.copy_button.size())
        self.copy_button.clicked.connect(self.copyToClipboard)

        display_hbox.addWidget(self.copy_button)

        self.display_label = QLabel(self.current_display, self)
        self.display_label.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.display_label.setStyleSheet("background-color: #2c3e50; color: white; font-size: 36px; border-radius: 10px; padding: 10px;")
        self.display_label.setFixedHeight(80)

        display_hbox.addWidget(self.display_label)
        calc_layout.addLayout(display_hbox)

        button_size = (70, 50)  

        buttons = [
            ['MC', 'MR', 'MS', 'M+', 'M-'],
            ['del', 'CE', 'C', '+/-', '√'],
            ['7', '8', '9', '/', '%'],
            ['4', '5', '6', '*', '1/x'],
            ['1', '2', '3', '+', '-'],
            ['0', ' ', '.', '^', '=']
        ]

        for row in buttons:
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0) 
            for button in row:
                btn = QPushButton(button, self)
                btn.clicked.connect(lambda checked, b=button: self.press(b))
                btn.setFixedSize(*button_size)
                if button in ['=', '+', '-', '*', '/', '^']:
                    btn.setProperty('class', 'operator')
                elif button in ['MC', 'MR', 'MS', 'M+', 'M-']:
                    btn.setProperty('class', 'memory')
                elif button in ['del', 'CE', 'C', '+/-', '√', '%', '1/x']:
                    btn.setProperty('class', 'function')
                else:
                    btn.setProperty('class', 'number')
                hbox.addWidget(btn)
                if button != row[-1]:  
                    hbox.addSpacing(10)  
            calc_layout.addLayout(hbox)
        
        history_layout = QVBoxLayout()
        self.history_list = QListWidget(self)
        self.history_list.setStyleSheet("""
            background-color: #ecf0f1;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #bdc3c7;
        """)
        
        self.clear_history_button = QPushButton("清空历史记录", self)
        self.clear_history_button.clicked.connect(self.clearHistory)
        self.clear_history_button.setObjectName("clearHistory")
        self.clear_history_button.setStyleSheet("""
            QPushButton#clearHistory {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton#clearHistory:hover {
                background-color: #c0392b;
            }
            QPushButton#clearHistory:pressed {
                background-color: #a93226;
            }
        """)
        
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(self.clear_history_button)
        
        main_layout.addLayout(calc_layout)
        main_layout.addSpacing(20)  
        main_layout.addLayout(history_layout)
        
        self.setLayout(main_layout)
        self.show()

    def copyToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_display)
        check_icon = QIcon('icon/check.png')

        large_icon = check_icon.pixmap(50, 50)
        self.copy_button.setIcon(QIcon(large_icon))
        
        self.copy_button.setStyleSheet("QPushButton { border: none; }")

        QTimer.singleShot(1000, self.restoreCopyButtonIcon)

    def restoreCopyButtonIcon(self):
        self.copy_button.setIcon(QIcon('icon/copy.png'))
        self.copy_button.setStyleSheet("")

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
        
        self.setFocus()  

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
                self.addToHistory(f"-({self.current_display[1:]}) = {self.current_display}")
            else:
                original = self.current_display
                self.current_display = '-' + self.current_display
                self.addToHistory(f"-({original}) = {self.current_display}")
        elif operator == '1/x':
            try:
                result = 1 / float(self.current_display)
                self.addToHistory(f"1/({self.current_display}) = {self.modifyResult(result)}")
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == '√':
            try:
                result = math.sqrt(float(self.current_display))
                self.addToHistory(f"√({self.current_display}) = {self.modifyResult(result)}")
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
                self.current_display = self.modifyResult(result)
                self.addToHistory(f"{expression} = {self.current_display}")
            except:
                self.current_display = 'illegal operation'
            self.STORAGE.clear()
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
            self.STORAGE.append('**')
            self.IS_CALC = True
        elif operator in ['+', '-', '*', '/']:
            self.STORAGE.append(self.current_display)
            self.STORAGE.append(operator)
            self.IS_CALC = True
        elif operator == '%':
            result = float(self.current_display) / 100
            self.addToHistory(f"{self.current_display}% = {self.modifyResult(result)}")
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == '=':
            if not self.IS_CALC and self.STORAGE:  # 只有在有运算且不是刚刚计算过的情下记录历史
                self.STORAGE.append(self.current_display)
                expression = ''.join(self.STORAGE)
                try:
                    result = eval(expression)
                    self.current_display = self.modifyResult(result)
                    self.addToHistory(f"{expression} = {self.current_display}")
                except:
                    self.current_display = 'illegal operation'
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

    def addToHistory(self, item):
        self.history.append(item)
        self.history_list.addItem(item)
        self.history_list.scrollToBottom()  

    def clearHistory(self):
        self.history.clear()
        self.history_list.clear()

    def clearAll(self):
        self.STORAGE.clear()
        self.IS_CALC = False
        self.current_display = '0'
        self.updateDisplay()
        self.history.clear()
        self.history_list.clear()

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

    def setupShortcuts(self):
        for i in range(10):
            QShortcut(QKeySequence(str(i)), self, lambda i=i: self.pressNumber(str(i)))
        
        QShortcut(QKeySequence('+'), self, lambda: self.pressOperator('+'))
        QShortcut(QKeySequence('-'), self, lambda: self.pressOperator('-'))
        QShortcut(QKeySequence('*'), self, lambda: self.pressOperator('*'))
        QShortcut(QKeySequence('/'), self, lambda: self.pressOperator('/'))
        QShortcut(QKeySequence('.'), self, lambda: self.pressNumber('.'))
        QShortcut(QKeySequence('='), self, lambda: self.pressOperator('='))
        QShortcut(QKeySequence(Qt.Key_Return), self, lambda: self.pressOperator('='))
        QShortcut(QKeySequence(Qt.Key_Enter), self, lambda: self.pressOperator('='))
        QShortcut(QKeySequence(Qt.Key_Backspace), self, self.delOne)
        QShortcut(QKeySequence('%'), self, lambda: self.pressOperator('%'))
        QShortcut(QKeySequence('^'), self, lambda: self.pressOperator('^'))
        QShortcut(QKeySequence('C'), self, self.clearAll)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.clearCurrent)

    def getStyleSheet(self):
        return """
        QWidget {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        QLabel {
            background-color: #2c3e50;
            color: white;
            font-size: 36px;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton {
            font-size: 18px;
            border-radius: 5px;
            border: none;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:pressed {
            background-color: #a0a0a0;
        }
        QPushButton[class="number"] {
            background-color: #ffffff;
            color: #2c3e50;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton[class="number"]:hover {
            background-color: #ecf0f1;
        }
        QPushButton[class="number"]:pressed {
            background-color: #bdc3c7;
        }
        QPushButton[class="operator"] {
            background-color: #e67e22;
            color: white;
        }
        QPushButton[class="operator"]:pressed {
            background-color: #d35400;
        }
        QPushButton[class="memory"] {
            background-color: #3498db;
            color: white;
        }
        QPushButton[class="memory"]:pressed {
            background-color: #2980b9;
        }
        QPushButton[class="function"] {
            background-color: #95a5a6;
            color: white;
        }
        QPushButton[class="function"]:pressed {
            background-color: #7f8c8d;
        }
        QListWidget {
            background-color: #ecf0f1;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #bdc3c7;
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #bdc3c7;
        }
        QListWidget::item:last-child {
            border-bottom: none;
        }
        QPushButton#clearHistory {
            background-color: #e74c3c;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton#clearHistory:hover {
            background-color: #c0392b;
        }
        QPushButton#clearHistory:pressed {
            background-color: #a93226;
        }
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())

