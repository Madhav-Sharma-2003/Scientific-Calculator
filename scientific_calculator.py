import tkinter as tk
import math
import re

class CasioFX82MS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CASIO fx-82MS")
        self.root.geometry("350x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e40')

        self.display_var = tk.StringVar()
        self.current_display = ""
        self.current_eval = ""
        self.memory = 0
        self.last_answer = ""
        self.special_mode = None   # 'nCr' or 'nPr'
        self.special_args = []     # to store n and r

        self.create_display()
        self.create_buttons()

    def create_display(self):
        self.display_frame = tk.Frame(self.root, bg='#34495e', bd=3, relief='ridge')
        self.display_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky='ew')
        brand_label = tk.Label(self.display_frame, text="CASIO", font=('Arial', 10, 'bold'),
                               bg='#34495e', fg='white')
        brand_label.grid(row=0, column=0, sticky='w', padx=5)
        model_label = tk.Label(self.display_frame, text="fx-82MS", font=('Arial', 8),
                               bg='#34495e', fg='white')
        model_label.grid(row=0, column=1, sticky='e', padx=5)
        svpam_label = tk.Label(self.display_frame, text="S-V.P.A.M.", font=('Arial', 10, 'bold'),
                               bg='#34495e', fg='white')
        svpam_label.grid(row=1, column=0, sticky='w', padx=5)
        edition_label = tk.Label(self.display_frame, text="2nd edition", font=('Arial', 8),
                                 bg='#34495e', fg='white')
        edition_label.grid(row=1, column=1, sticky='e', padx=5)
        self.display = tk.Entry(self.display_frame, textvariable=self.display_var, font=('Arial', 16),
                                bd=2, relief='sunken', justify='right', state='readonly',
                                readonlybackground='#ecf0f1', width=20)
        self.display.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def create_buttons(self):
        button_layout = [
            [('SHIFT', 1, '#e74c3c', 'white'), ('ALPHA', 1, '#e74c3c', 'white'), ('', 0, '', ''),
             ('MODE', 1, '#95a5a6', 'black'), ('CLR', 1, '#95a5a6', 'black'), ('ON', 1, '#95a5a6', 'black')],
            [('x⁻¹', 1, '#bdc3c7', 'black'), ('nCr', 1, '#bdc3c7', 'black'), ('nPr', 1, '#bdc3c7', 'black'),
             ('Pol(', 1, '#bdc3c7', 'black'), ('x³', 1, '#bdc3c7', 'black'), ('', 0, '', '')],
            [('a/b/c', 1, '#bdc3c7', 'black'), ('√', 1, '#bdc3c7', 'black'), ('x²', 1, '#bdc3c7', 'black'),
             ('^', 1, '#bdc3c7', 'black'), ('log', 1, '#bdc3c7', 'black'), ('ln', 1, '#bdc3c7', 'black')],
            [('(-)', 1, '#bdc3c7', 'black'), ('°\'"', 1, '#bdc3c7', 'black'), ('hyp', 1, '#bdc3c7', 'black'),
             ('sin', 1, '#bdc3c7', 'black'), ('cos', 1, '#bdc3c7', 'black'), ('tan', 1, '#bdc3c7', 'black')],
            [('RCL', 1, '#bdc3c7', 'black'), ('ENG', 1, '#bdc3c7', 'black'), ('(', 1, '#bdc3c7', 'black'),
             (')', 1, '#bdc3c7', 'black'), (',', 1, '#bdc3c7', 'black'), ('M+', 1, '#e67e22', 'white')],
            [('7', 1, '#34495e', 'white'), ('8', 1, '#34495e', 'white'), ('9', 1, '#34495e', 'white'),
             ('DEL', 1, '#e74c3c', 'white'), ('AC', 1, '#e74c3c', 'white'), ('', 0, '', '')],
            [('4', 1, '#34495e', 'white'), ('5', 1, '#34495e', 'white'), ('6', 1, '#34495e', 'white'),
             ('×', 1, '#f39c12', 'white'), ('÷', 1, '#f39c12', 'white'), ('', 0, '', '')],
            [('1', 1, '#34495e', 'white'), ('2', 1, '#34495e', 'white'), ('3', 1, '#34495e', 'white'),
             ('+', 1, '#f39c12', 'white'), ('-', 1, '#f39c12', 'white'), ('', 0, '', '')],
            [('0', 1, '#34495e', 'white'), ('.', 1, '#34495e', 'white'), ('×10ˣ', 1, '#bdc3c7', 'black'),
             ('Ans', 1, '#bdc3c7', 'black'), ('=', 1, '#27ae60', 'white'), ('', 0, '', '')]
        ]
        for row_idx, row in enumerate(button_layout, start=1):
            for col_idx, (text, active, bg_color, fg_color) in enumerate(row):
                if active:
                    btn = tk.Button(self.root, text=text, font=('Arial', 10, 'bold'), width=6, height=2,
                                    bg=bg_color, fg=fg_color, command=lambda t=text: self.button_click(t))
                    btn.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky='nsew')
                else:
                    spacer = tk.Label(self.root, bg='#2c3e40', width=6, height=2)
                    spacer.grid(row=row_idx, column=col_idx, padx=1, pady=1)

    def button_click(self, char):
        # Clear nCr/nPr mode on AC, DEL, or after calculation
        if char == 'AC':
            self.current_display = ""
            self.current_eval = ""
            self.display_var.set("")
            self.special_mode = None
            self.special_args = []
        elif char == 'DEL':
            self.current_display = self.current_display[:-1]
            self.current_eval = self.current_eval[:-1]
            self.display_var.set(self.current_display)
            if self.special_mode and self.special_args:
                self.special_args.pop()
        elif char == '=':
            self.calculate_result()
        elif char == "nCr" or char == "nPr":
            self.current_display += f" {char} "
            self.display_var.set(self.current_display)
            self.special_mode = char
            self.special_args = []
        elif char in '0123456789':
            self.current_display += char
            self.display_var.set(self.current_display)
            if self.special_mode:
                self.special_args.append(char)
            else:
                self.current_eval += char
        elif char in '+-×÷^':
            self.current_display += char
            self.current_eval += char.replace("×", "*").replace("÷", "/")
            self.display_var.set(self.current_display)
        elif char == "√":
            self.current_display += "√("
            self.current_eval += "sqrt("
            self.display_var.set(self.current_display)
        elif char == "x²":
            self.current_display += "²"
            self.current_eval += "^2"
            self.display_var.set(self.current_display)
        elif char == "x³":
            self.current_display += "³"
            self.current_eval += "^3"
            self.display_var.set(self.current_display)
        elif char == "x⁻¹":
            self.current_display += "^(-1)"
            self.current_eval += "^-1"
            self.display_var.set(self.current_display)
        elif char in ["sin", "cos", "tan", "log", "ln"]:
            self.current_display += f"{char}("
            self.current_eval += f"{char}("
            self.display_var.set(self.current_display)
        elif char == "Ans":
            self.current_display += self.last_answer
            self.current_eval += self.last_answer
            self.display_var.set(self.current_display)
        elif char in "()":
            self.current_display += char
            self.current_eval += char
            self.display_var.set(self.current_display)
        elif char == ".":
            self.current_display += "."
            self.current_eval += "."
            self.display_var.set(self.current_display)
        elif char == "M+":
            try:
                self.memory += float(self.last_answer)
            except:
                pass
        elif char == "RCL":
            self.current_display += str(self.memory)
            self.current_eval += str(self.memory)
            self.display_var.set(self.current_display)
        elif char == "(-)":
            self.current_display += "-"
            self.current_eval += "-"
            self.display_var.set(self.current_display)
        else:
            pass

    def calculate_result(self):
        # Special handling for nCr and nPr with Casio syntax
        if self.special_mode in ["nCr", "nPr"] and len(self.special_args) >= 2:
            try:
                # Get n and r (allow multi-digit)
                parts = ''.join(self.special_args)
                # Find two numbers surrounding nCr/nPr in display
                match = re.search(r'(\d+)\s+' + self.special_mode + r'\s+(\d+)', self.current_display)
                if match:
                    n = int(match.group(1))
                    r = int(match.group(2))
                    if self.special_mode == "nCr":
                        result = math.comb(n, r)
                    else:
                        result = math.perm(n, r)
                    self.display_var.set(str(result))
                    self.last_answer = str(result)
                else:
                    self.display_var.set("Error")
            except Exception:
                self.display_var.set("Error")
            self.current_display = ""
            self.current_eval = ""
            self.special_mode = None
            self.special_args = []
            return

        # Normal calculation
        expression = self.current_eval
        try:
            def degrees_sin(x): return round(math.sin(math.radians(x)), 10)
            def degrees_cos(x): return round(math.cos(math.radians(x)), 10)
            def degrees_tan(x): return round(math.tan(math.radians(x)), 10)
            def py_log(x): return math.log10(float(x))
            def py_ln(x): return math.log(float(x))
            def py_sqrt(x): return math.sqrt(float(x))
            def py_comb(n, r): return math.comb(int(n), int(r))
            def py_perm(n, r): return math.perm(int(n), int(r))

            # Handle ^ powers
            expression = re.sub(r'(\d+)\^2', r'pow(\1,2)', expression)
            expression = re.sub(r'(\d+)\^3', r'pow(\1,3)', expression)
            expression = re.sub(r'(\d+)\^-1', r'1/(\1)', expression)

            # Replace function names
            expression = expression.replace("sin(", "degrees_sin(")
            expression = expression.replace("cos(", "degrees_cos(")
            expression = expression.replace("tan(", "degrees_tan(")
            expression = expression.replace("log(", "py_log(")
            expression = expression.replace("ln(", "py_ln(")
            expression = expression.replace("sqrt(", "py_sqrt(")
            expression = expression.replace("comb(", "py_comb(")
            expression = expression.replace("perm(", "py_perm(")

            result = eval(expression, {
                'pow': pow, 'degrees_sin': degrees_sin, 'degrees_cos': degrees_cos,
                'degrees_tan': degrees_tan, 'py_log': py_log,
                'py_ln': py_ln, 'py_sqrt': py_sqrt, 'py_comb': py_comb, 'py_perm': py_perm
            })

            self.last_answer = str(result)
            self.display_var.set(self.last_answer)
            self.current_display = ""
            self.current_eval = ""
            self.special_mode = None
            self.special_args = []
        except Exception:
            self.display_var.set("Error")
            self.current_display = ""
            self.current_eval = ""
            self.special_mode = None
            self.special_args = []

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calculator = CasioFX82MS()
    calculator.run()
