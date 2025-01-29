#This is built using Tkinter! I think it's already installed. If not, you can install it using pip. 
# It has a worse UI compared to the PyQt6 version, but it's easier to use and understand.
# If you have any questions, feel free to ask. I hope this helps!

import tkinter as tk
from tkinter import messagebox
import math
import os
import sys
import ctypes

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Calculator")
        self.root.geometry("400x490")  # Adjusted height to remove extra space
        self.root.configure(bg="#2E2E2E")  # Dark theme
        self.root.resizable(0, 0)  # Prevent resizing
        self.expression = ""
        self.history = []
        
        self.input_text = tk.StringVar()
        
        self.create_widgets()
        self.bind_keys()
    
    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.root, width=400, height=70, bd=0, bg="#3C3F41")
        input_frame.pack(side=tk.TOP, pady=10)
        
        input_field = tk.Entry(input_frame, font=('Arial', 20, 'bold'), textvariable=self.input_text, width=25, bg="#D0D3D4", bd=5, relief=tk.FLAT, justify=tk.RIGHT, )
        input_field.pack(ipady=15)
        
        # History Frame
        history_frame = tk.Frame(self.root, width=400, height=100, bg="#1E1E1E")
        history_frame.pack(side=tk.TOP, pady=5)
        
        self.history_label = tk.Label(history_frame, font=('Arial', 12), text="History:", anchor='w', bg="#1E1E1E", fg="#FFFFFF", justify=tk.LEFT)
        self.history_label.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Buttons Frame
        btns_frame = tk.Frame(self.root, width=400, height=400, bg="#2E2E2E")  # Adjusted height to remove extra space
        btns_frame.pack()
        
        self.create_buttons(btns_frame)
    
    def create_buttons(self, frame):
        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', 'sqrt'),
            ('1', '2', '3', '-', '^'),
            ('0', '.', '=', '+', 'CE'),
            ('sin', 'cos', 'tan', 'log', 'ln'),
            ('(', ')', 'π', 'e', 'DEL')
        ]
        
        for r, row in enumerate(buttons):
            for c, button in enumerate(row):
                btn = tk.Button(frame, text=button, fg="#FFFFFF", width=6, height=2, bd=0, bg="#4E5052", cursor="hand2", font=('Arial', 12, 'bold'), command=lambda x=button: self.on_button_click(x))
                btn.grid(row=r, column=c, padx=5, pady=5)
                
                if button == '=':
                    btn.configure(bg="#27AE60", fg="#FFFFFF", width=7, command=self.evaluate)
                elif button == 'C':
                    btn.configure(bg="#E74C3C", fg="#FFFFFF", command=self.clear_all)
                elif button == 'CE':
                    btn.configure(bg="#E67E22", fg="#FFFFFF", command=self.clear_entry)
                elif button == 'DEL':
                    btn.configure(bg="#C0392B", fg="#FFFFFF", command=self.delete_last)
    
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
        else:
            self.expression += str(char)
        
        self.input_text.set(self.expression)
    
    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.history.append(f"{self.expression} = {result}")
            self.update_history()
            self.expression = result
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            self.expression = ""
            self.input_text.set("")
    
    def clear_entry(self):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)
    
    def delete_last(self):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)
    
    def update_history(self):
        self.history_label.config(text="\n".join(self.history[-5:]))  # Show last 5 history items
    
    def bind_keys(self):
        self.root.bind('<Return>', lambda event: self.evaluate())
        self.root.bind('<BackSpace>', lambda event: self.clear_entry())
        self.root.bind('<Escape>', lambda event: self.clear_all())
    
    def clear_all(self):
        self.expression = ""
        self.input_text.set("")

def add_to_startup():
    if sys.platform == "win32":
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_path = os.path.abspath(__file__)
        shortcut_path = os.path.join(startup_path, 'Calculator.lnk')
        
        shell = ctypes.windll.shell32
        shortcut = shell.SHCreateShortcut(shortcut_path)
        shortcut.TargetPath = script_path
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.Save()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()