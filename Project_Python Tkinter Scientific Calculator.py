from tkinter import *
import math as m
import re

win = Tk()
win.geometry("380x680+470+20")
win.title("Python Calculator Project")
win.config(bg="grey11")
win.resizable(False, False)
win.overrideredirect(1)

memory_value = 0

def close():
    win.destroy()

def clear():
    entry.delete(0, "end")

def back():
    last_number = len(entry.get()) - 1
    entry.delete(last_number)

def press(input):
    lenth = len(entry.get())
    # If the input is 'x', convert it to '*'
    if input == 'x':
        input = '*'
    entry.insert(lenth, str(input))

def expression_break(function_name, expression):
    try:
        start_index = expression.find(function_name) + len(function_name) + 1
        end_index = expression.find(")", start_index)
        content = expression[start_index:end_index]
        data = content.split(',')
        return data
    except Exception as e:
        return ["Error"]

def memory_clear():
    global memory_value
    memory_value = 0.0
    entry.delete(0, "end")
    entry.insert(0, "Memory Cleared")
    print("Memory Cleared")

def memory_recall():
    entry.delete(0, "end")
    entry.insert(0, str(memory_value))
    print(f"Memory Recalled: {memory_value}")

def memory_add():
    global memory_value
    try:
        value = float(entry.get())
        memory_value += value
        entry.delete(0, "end")
        entry.insert(0, f"M+ Done: {memory_value}")
        print(f"Memory Added: {memory_value}")
    except ValueError:
        entry.delete(0, "end")
        entry.insert(0, "Error: Invalid Input")

def memory_subtract():
    global memory_value
    try:
        value = float(entry.get())
        memory_value -= value
        clear()
        entry.insert(0, "M- Done")
    except:
        clear()
        entry.insert(0, "Error")

def equal():
    expression = entry.get()
    clear()

    try:
        # Replace π, e, and custom syntax
        expression = expression.replace("π", str(m.pi)).replace("e", str(m.e))
        expression = expression.replace("x", "*")

        # Convert percentage: '10%' becomes '(10/100)'
        expression = re.sub(r'(\d+(\.\d+)?)\%', r'(\1/100)', expression)

        # Replace math functions with m.function
        expression = evaluate_functions(expression)

        # Evaluate the expression
        result = eval(expression)
        entry.insert(0, str(result))

    except ZeroDivisionError:
        entry.insert(0, "Error: Div by Zero")
    except Exception as e:
        entry.insert(0, "Error")
        print("Evaluation Error:", e)

def evaluate_functions(expression):
    expression = expression.replace("sqrt", "m.sqrt")
    expression = expression.replace("sin", "m.sin")
    expression = expression.replace("cos", "m.cos")
    expression = expression.replace("tan", "m.tan")
    expression = expression.replace("log", "m.log10")
    expression = expression.replace("ln", "m.log")
    expression = expression.replace("deg", "m.degrees")
    expression = expression.replace("rad", "m.radians")
    expression = expression.replace("fac", "m.factorial")
    return expression

entry_string = StringVar()
entry = Entry(win, textvariable=entry_string, fg="white", bg="grey20", border=0, font=("Bahnschrift semibold", 26))
entry.grid(columnspan=4, ipady=15)
font_value = ("caliberi", 18)

# Scientific Function Buttons
Button(win, text="tan", command=lambda: press("tan("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=1, column=0, sticky=E+W, ipady=5)
Button(win, text="cos", command=lambda: press("cos("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=1, column=1, sticky=E+W, ipady=5)
Button(win, text="sin", command=lambda: press("sin("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=1, column=2, sticky=E+W, ipady=5)
Button(win, text="sqrt", command=lambda: press("sqrt("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=1, column=3, sticky=E+W, ipady=5)

Button(win, text="log", command=lambda: press("log("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=2, column=0, sticky=E+W, ipady=5)
Button(win, text="ln", command=lambda: press("ln("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=2, column=1, sticky=E+W, ipady=5)
Button(win, text="deg", command=lambda: press("deg("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=2, column=2, sticky=E+W, ipady=5)
Button(win, text="rad", command=lambda: press("rad("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=2, column=3, sticky=E+W, ipady=5)

Button(win, text="fac", command=lambda: press("fac("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=3, column=0, sticky=E+W, ipady=5)
Button(win, text="pow", command=lambda: press("pow("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=3, column=1, sticky=E+W, ipady=5)
Button(win, text="rem", command=lambda: press(" % "), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=3, column=2, sticky=E+W, ipady=5)
Button(win, text="π", command=lambda: press("π"), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=3, column=3, sticky=E+W, ipady=5)

# Basic Controls
Button(win, text="C", command=clear, **dict(bg="grey5", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=4, column=0, columnspan=2, sticky=E+W, ipady=5)
Button(win, text="⌫", command=back, **dict(bg="grey5", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=4, column=2, columnspan=2, sticky=E+W, ipady=5)

# Parentheses and Operators
Button(win, text="(", command=lambda: press("("), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=5, column=0, sticky=E+W, ipady=5)
Button(win, text=")", command=lambda: press(")"), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=5, column=1, sticky=E+W, ipady=5)
Button(win, text="%", command=lambda: press("%"), **dict(bg="grey11", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=5, column=2, sticky=E+W, ipady=5)
Button(win, text=",", command=lambda: press(","), **dict(bg="grey5", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=5, column=3, sticky=E+W, ipady=5)

# Digits and Operators
digits = [
    ("7", 6, 0), ("8", 6, 1), ("9", 6, 2), ("x", 6, 3),
    ("4", 7, 0), ("5", 7, 1), ("6", 7, 2), ("/", 7, 3),
    ("1", 8, 0), ("2", 8, 1), ("3", 8, 2), ("-", 8, 3),
    (".", 9, 0), ("0", 9, 1), ("e", 9, 2), ("+", 9, 3)
]
for (text, r, c) in digits:
    Button(win, text=text, command=lambda val=text: press(val), **dict(bg="grey11" if text.isdigit() or text == "." else "grey5", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=r, column=c, sticky=E+W, ipady=5)

# Equal and Close
Button(win, text="=", command=equal, **dict(bg="darkorange1", fg="white", font=font_value, borderwidth=1, relief=SOLID)).grid(row=11, column=0, columnspan=3, sticky=E+W, ipady=5)
Button(win, text="Close", command=close, **dict(bg="grey5", fg="darkorange1", font=font_value, borderwidth=1, relief=SOLID)).grid(row=11, column=3, sticky=E+W, ipady=5)

# Memory Functions
Button(win, text="MC", command=memory_clear, **dict(bg="steelblue1", fg="grey11", font=font_value, borderwidth=1, relief=SOLID)).grid(row=10, column=0, sticky=E+W, ipady=5)
Button(win, text="MR", command=memory_recall, **dict(bg="steelblue1", fg="grey11", font=font_value, borderwidth=1, relief=SOLID)).grid(row=10, column=1, sticky=E+W, ipady=5)
Button(win, text="M+", command=memory_add, **dict(bg="steelblue1", fg="grey11", font=font_value, borderwidth=1, relief=SOLID)).grid(row=10, column=2, sticky=E+W, ipady=5)
Button(win, text="M-", command=memory_subtract, **dict(bg="steelblue1", fg="grey11", font=font_value, borderwidth=1, relief=SOLID)).grid(row=10, column=3, sticky=E+W, ipady=5)

mainloop()
