import tkinter as tk
from tkinter import messagebox
import math

class CasioCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.resizable(False, False)
        self.memory = 0
        self.expr = ""
        self.result_var = tk.StringVar()
        self.expr_var = tk.StringVar()
        self.mode = "DEG"  # Default mode

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        frame_disp = tk.Frame(self)
        frame_disp.grid(row=0, column=0, columnspan=6, sticky='nsew')

        tk.Label(frame_disp, textvariable=self.expr_var, anchor='e', font=('Consolas', 12), bg="white", width=30).grid(row=0, column=0, columnspan=6, sticky='ew')
        tk.Label(frame_disp, textvariable=self.result_var, anchor='e', font=('Consolas', 20, 'bold'), bg="white", width=30).grid(row=1, column=0, columnspan=6, sticky='ew')

        self.expr_var.set("")
        self.result_var.set("0")

        btn_cfg = {
            'font': ('Consolas', 12),
            'width': 6,
            'height': 2,
            'bg': '#D7E3FC',
        }

        buttons = [
            [("MC", lambda: self.memory_clear()), ("MR", lambda: self.memory_recall()), ("M+", lambda: self.memory_add()), ("M-", lambda: self.memory_sub()), ("CE", lambda: self.clear_entry()), ("C", lambda: self.clear_all())],
            [("sin", lambda: self.append_func('sin(')), ("cos", lambda: self.append_func('cos(')), ("tan", lambda: self.append_func('tan(')), ("π", lambda: self.append_value(str(math.pi))), ("e", lambda: self.append_value(str(math.e))), ("DEG", self.toggle_mode)],
            [("asin", lambda: self.append_func('asin(')), ("acos", lambda: self.append_func('acos(')), ("atan", lambda: self.append_func('atan(')), ("ln", lambda: self.append_func('ln(')), ("log", lambda: self.append_func('log(')), ("√", lambda: self.append_func('sqrt('))],
            [("x^y", lambda: self.append_op('**')), ("x²", lambda: self.append_func('sqr(')), ("e^x", lambda: self.append_func('exp(')), ("10^x", lambda: self.append_func('tenx(')), ("|x|", lambda: self.append_func('abs(')), ("mod", lambda: self.append_op('mod'))],
            [("nPr", lambda: self.append_func('nPr(')), ("nCr", lambda: self.append_func('nCr(')), ("!", lambda: self.append_func('fact(')), ("(", lambda: self.append_value('(')), (")", lambda: self.append_value(')')), ("←", self.backspace)],
            [("7", lambda: self.append_value('7')), ("8", lambda: self.append_value('8')), ("9", lambda: self.append_value('9')), ("/", lambda: self.append_op('/')), ("%", lambda: self.append_op('%')), ("Ans", self.use_ans)],
            [("4", lambda: self.append_value('4')), ("5", lambda: self.append_value('5')), ("6", lambda: self.append_value('6')), ("*", lambda: self.append_op('*')), ("-", lambda: self.append_op('-')), ("+", lambda: self.append_op('+'))],
            [("1", lambda: self.append_value('1')), ("2", lambda: self.append_value('2')), ("3", lambda: self.append_value('3')), (".", lambda: self.append_value('.')), ("0", lambda: self.append_value('0')), ("=", self.calculate)],
        ]

        for row_idx, row in enumerate(buttons, start=2):
            for col_idx, (label, cmd) in enumerate(row):
                b = tk.Button(self, text=label, command=cmd, **btn_cfg)
                b.grid(row=row_idx, column=col_idx, padx=1, pady=1)

    def append_value(self, val):
        # Auto-insert comma for nPr/nCr arguments if missing
        if self.expr.endswith("nPr(") or self.expr.endswith("nCr("):
            self.expr += val
        else:
            for func in ["nPr(", "nCr("]:
                pos = self.expr.rfind(func)
                if pos != -1:
                    sub_expr = self.expr[pos + len(func):]
                    if "," not in sub_expr:
                        self.expr += "," + val
                        self.expr_var.set(self.expr)
                        return
            self.expr += val
        self.expr_var.set(self.expr)

    def append_op(self, op):
        if op == 'mod':
            self.expr += '%'
        else:
            self.expr += op
        self.expr_var.set(self.expr)

    def append_func(self, func):
        self.expr += func
        self.expr_var.set(self.expr)

    def backspace(self):
        self.expr = self.expr[:-1]
        self.expr_var.set(self.expr)

    def clear_entry(self):
        self.expr = ""
        self.expr_var.set("")

    def clear_all(self):
        self.expr = ""
        self.result_var.set("0")
        self.expr_var.set("")

    def bind_keys(self):
        self.bind('<Key>', self.key_input)
        self.bind('<Return>', lambda e: self.calculate())
        self.bind('<BackSpace>', lambda e: self.backspace())
        self.bind('<Escape>', lambda e: self.clear_all())

    def key_input(self, event):
        ch = event.char
        if ch in '0123456789.+-*/()%':
            self.append_value(ch)
        elif ch == '\r':
            self.calculate()
        elif ch.lower() == 'c':
            self.clear_all()
        elif ch == '\x08':
            self.backspace()

    def use_ans(self):
        if self.result_var.get() != "Error":
            self.expr += self.result_var.get()
            self.expr_var.set(self.expr)

    def toggle_mode(self):
        self.mode = "RAD" if self.mode == "DEG" else "DEG"
        for child in self.children.values():
            if isinstance(child, tk.Button) and child['text'] in ["DEG", "RAD"]:
                child.config(text=self.mode)
                break

    def memory_add(self):
        try:
            val = float(self.result_var.get())
            self.memory += val
        except:
            pass

    def memory_sub(self):
        try:
            val = float(self.result_var.get())
            self.memory -= val
        except:
            pass

    def memory_recall(self):
        self.expr += str(self.memory)
        self.expr_var.set(self.expr)

    def memory_clear(self):
        self.memory = 0

    def calculate(self):
        expr = self.expr
        expr = expr.replace('ln(', 'math.log(')
        expr = expr.replace('log(', 'math.log10(')
        expr = expr.replace('sqrt(', 'math.sqrt(')
        expr = expr.replace('exp(', 'math.exp(')
        expr = expr.replace('tenx(', 'math.pow(10,')
        expr = expr.replace('sqr(', 'math.pow(')
        expr = expr.replace('fact', 'math.factorial')
        expr = expr.replace('abs', 'abs')
        expr = expr.replace('mod', '%')

        try:
            local_env = {
                'math': math,
                'abs': abs,
                'nPr': self._nPr,
                'nCr': self._nCr,
                'sin': lambda x: math.sin(math.radians(x)) if self.mode == 'DEG' else math.sin(x),
                'cos': lambda x: math.cos(math.radians(x)) if self.mode == 'DEG' else math.cos(x),
                'tan': lambda x: math.tan(math.radians(x)) if self.mode == 'DEG' else math.tan(x),
                'asin': lambda x: math.degrees(math.asin(x)) if self.mode == 'DEG' else math.asin(x),
                'acos': lambda x: math.degrees(math.acos(x)) if self.mode == 'DEG' else math.acos(x),
                'atan': lambda x: math.degrees(math.atan(x)) if self.mode == 'DEG' else math.atan(x),
                '__builtins__': {}
            }

            result = eval(expr, local_env)
            self.result_var.set(str(result))
        except Exception as e:
            self.result_var.set("Error")
            messagebox.showerror("Calculation Error", f"Invalid input: {e}")
        finally:
            self.expr = ""
            self.expr_var.set("")

    def _nPr(self, n, r):
        n, r = int(n), int(r)
        if n < 0 or r < 0 or n < r:
            raise ValueError("n and r must be ≥ 0 and n ≥ r")
        return math.factorial(n) // math.factorial(n - r)

    def _nCr(self, n, r):
        n, r = int(n), int(r)
        if n < 0 or r < 0 or n < r:
            raise ValueError("n and r must be ≥ 0 and n ≥ r")
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

if __name__ == "__main__":
    calc = CasioCalculator()
    calc.mainloop()
