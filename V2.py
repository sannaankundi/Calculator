# This is BUILT using PyQT6! If you want to use this version of the calculator, you need to install PyQt6.

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel
from PyQt6.QtGui import QFont
import sys
import math
import re

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Ultimate Calculator")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("border-radius: 10px; border: 1px solid #A9A9A9;")  # Rounded border for the main window
        
        self.expression = ""
        self.history = []
        
        layout = QVBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont('Arial', 20))
        self.input_field.setReadOnly(True)
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("border-radius: 10px; border: 1px solid #A9A9A9;")  # Rounded border for the input field
        layout.addWidget(self.input_field)
        
        self.history_label = QLabel("History:", self)
        self.history_label.setFont(QFont('Arial', 12))
        self.history_label.setFixedHeight(100)
        layout.addWidget(self.history_label)
        
        grid_layout = QGridLayout()
        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', 'sqrt'),
            ('1', '2', '3', '-', '^'),
            ('0', '.', '=', '+', 'CE'),
            ('sin', 'cos', 'tan', 'log', 'ln'),
            ('(', ')', 'π', 'e', 'DEL')
        ]
        
        for r, row in enumerate(buttons):
            for c, btn_text in enumerate(row):
                button = QPushButton(btn_text, self)
                button.setFont(QFont('Arial', 12))
                button.setFixedSize(60, 40)
                button.setStyleSheet("border-radius: 10px; border: 1px solid #A9A9A9;")
                button.clicked.connect(lambda _, x=btn_text: self.on_button_click(x))
                grid_layout.addWidget(button, r, c)
                
                if btn_text == '=':
                    button.setStyleSheet("background-color: #27AE60; color: white; border-radius: 10px; border: 1px solid #A9A9A9;")
                elif btn_text == 'C':
                    button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; border: 1px solid #A9A9A9;")
                elif btn_text == 'CE':
                    button.setStyleSheet("background-color: #E67E22; color: white; border-radius: 10px; border: 1px solid #A9A9A9;")
                elif btn_text == 'DEL':
                    button.setStyleSheet("background-color: #C0392B; color: white; border-radius: 10px; border: 1px solid #A9A9A9;")
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)
    
    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == 'sqrt':
            self.expression += 'math.sqrt('
        elif char == '^':
            self.expression += '**'
        elif char == 'π':
            self.expression += str(math.pi)
        elif char == 'e':
            self.expression += str(math.e)
        elif char in ['sin', 'cos', 'tan', 'log', 'ln']:
            self.expression += f'math.{char}('
        elif char == '=':
            self.evaluate()
            return
        elif char == 'CE':
            self.expression = self.expression[:-1]
        elif char == 'DEL':
            self.expression = self.expression[:-1]
        else:
            self.expression += char
        
        self.input_field.setText(self.expression)
    
    def evaluate(self):
        try:
            # Normalize numbers with leading zeros
            normalized_expression = re.sub(r'\b0+(\d+)', r'\1', self.expression)
            result = str(eval(normalized_expression))
            self.input_field.setText(result)
            self.history.append(f"{self.expression} = {result}")
            self.update_history()
            self.expression = result
        except Exception:
            self.input_field.setText("Error")
            self.expression = ""
    
    def update_history(self):
        self.history_label.setText("History:\n" + "\n".join(self.history[-5:]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
