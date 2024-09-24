import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QShortcut, QMenu, QAction
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
        self.setFixedSize(750, 600)  
        
        main_layout = QHBoxLayout()
        calc_layout = QVBoxLayout()
        calc_layout.setContentsMargins(20, 40, 20, 20)  
        calc_layout.setSpacing(10) 

        display_hbox = QHBoxLayout()
        display_hbox.setContentsMargins(0, 0, 0, 0) 

        self.display_label = QLabel(self.current_display, self)
        self.display_label.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.display_label.setStyleSheet("background-color: #2c3e50; color: white; font-size: 36px; border-radius: 10px; padding: 10px;")
        self.display_label.setFixedHeight(80)

        self.copy_button = QPushButton(self)
        self.copy_button.setFixedSize(50, 50)
        copy_icon = QIcon('icon/copy.png')
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setIconSize(self.copy_button.size())
        self.copy_button.clicked.connect(self.copyToClipboard)
        
        display_hbox.addWidget(self.copy_button)  
        display_hbox.addWidget(self.display_label)
        calc_layout.addLayout(display_hbox)

        button_size = (70, 50)  

        buttons = [
            ['C', 'Del', '+/-', '√'],
            ['x²', 'xʸ', '%', '1/x'],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        left_layout = QVBoxLayout()
        left_layout.addStretch()

        buttons_layout = QVBoxLayout()
        for row in buttons:
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0) 
            for button in row:
                btn = QPushButton(button, self)
                btn.clicked.connect(lambda checked, b=button: self.press(b))
                btn.setFixedSize(*button_size)  
                if button in ['=', '+', '-', '*', '/', 'xʸ']:
                    btn.setProperty('class', 'operator')
                elif button in ['C', 'Del', '+/-', '√', 'x²', '%', '1/x']:
                    btn.setProperty('class', 'function')
                else:
                    btn.setProperty('class', 'number')
                hbox.addWidget(btn)
                if button != row[-1]:  
                    hbox.addSpacing(10)  
            buttons_layout.addLayout(hbox)

        calc_inner_layout = QHBoxLayout()
        calc_inner_layout.addLayout(left_layout)
        calc_inner_layout.addLayout(buttons_layout)
        calc_layout.addLayout(calc_inner_layout)
        
        history_layout = QVBoxLayout()
        self.history_list = QListWidget(self)
        self.history_list.setFixedWidth(300)  
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #ecf0f1;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #bdc3c7;
                color: black;  
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #bdc3c7;
                background-color: transparent;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #d5dbdb;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:last-child {
                border-bottom: none;
            }
        """)
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.showContextMenu)
        
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
        elif button in ['+', '-', '*', '/', '%', '+/-', '√', '1/x', 'C', 'Del', 'x²', 'xʸ', '=']:
            self.pressOperator(button)
        
        self.setFocus()  

    def pressNumber(self, number):
        if self.IS_CALC:
            self.current_display = '0'
            self.IS_CALC = False
        if self.current_display == '0':
            if number == '.':
                self.current_display = '0.'
            else:
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
        elif operator == 'x²':
            try:
                result = float(self.current_display) ** 2
                self.addToHistory(f"({self.current_display})² = {self.modifyResult(result)}")
            except:
                result = 'illegal operation'
            self.current_display = self.modifyResult(result)
            self.IS_CALC = True
        elif operator == 'xʸ':
            self.STORAGE.append(self.current_display)
            self.STORAGE.append('**')
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
            if not self.IS_CALC and self.STORAGE:  
                self.STORAGE.append(self.current_display)
                expression = ''.join(self.STORAGE)
                try:
                    result = eval(expression)
                    if '**' in expression:
                        expression = expression.replace('**', '^')
                    self.current_display = self.modifyResult(result)
                    self.addToHistory(f"{expression} = {self.current_display}")
                except:
                    self.current_display = 'illegal operation'
            self.STORAGE.clear()
            self.IS_CALC = True
        elif operator == 'C':
            self.clearAll()
        elif operator == 'Del':
            self.delOne()

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
        QShortcut(QKeySequence("Ctrl+C"), self, self.copyResult)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, self.copyExpression)

    def showContextMenu(self, position):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
                color: black; 
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        copy_result_action = QAction("复制结果 (Command+C)", self)
        copy_expression_action = QAction("复制算式和结果 (Shift+Command+C)", self)
        
        menu.addAction(copy_result_action)
        menu.addAction(copy_expression_action)
        
        copy_result_action.triggered.connect(self.copyResult)
        copy_expression_action.triggered.connect(self.copyExpression)
        
        menu.exec_(self.history_list.mapToGlobal(position))
        
        self.history_list.clearSelection()
        
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            item.setBackground(Qt.transparent)

    def copyResult(self):
        item = self.history_list.currentItem()
        if item:
            result = item.text().split('=')[-1].strip()
            QApplication.clipboard().setText(result)

    def copyExpression(self):
        item = self.history_list.currentItem()
        if item:
            expression = item.text().strip()  
            QApplication.clipboard().setText(expression)

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
            color: black;  
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #bdc3c7;
            background-color: transparent;
            border-radius: 5px;
        }
        QListWidget::item:hover {
            background-color: #d5dbdb !important;
        }
        QListWidget::item:selected {
            background-color: #3498db;
            color: white;
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

