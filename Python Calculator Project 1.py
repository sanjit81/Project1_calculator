import tkinter as tk
import math
import re

calculation = ""
memory = 0
current_theme = "light"

disallowed_text = ["abc", "def"]  # Example disallowed strings
valid_scientific_buttons = ["sin", "cos", "tan", "log10", "sqrt", "pi", "e", "**"]

themes = {
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "entry_bg": "#f0f0f0",
        "button_bg": "#e0e0e0",
        "active_bg": "#d0d0d0"
    },
    "dark": {
        "bg": "#222222",
        "fg": "#ffffff",
        "entry_bg": "#333333",
        "button_bg": "#444444",
        "active_bg": "#555555"
    }
}

def add_to_calculation(symbol):
    global calculation

    # Block known disallowed words
    if any(text in symbol for text in disallowed_text):
        entry.delete(0, tk.END)
        entry.insert(0, "Text not allowed")
        return

    # Block random letter inputs unless they start with valid scientific functions
    if re.search("[a-zA-Z]", symbol) and not any(symbol.startswith(func) for func in valid_scientific_buttons):
        entry.delete(0, tk.END)
        entry.insert(0, "Text not allowed")
        return

    calculation += str(symbol)
    entry.delete(0, tk.END)
    entry.insert(0, calculation)

def memory_clear():
    global memory, calculation
    memory = 0
    calculation = ""
    entry.delete(0, tk.END)
    entry.insert(0, "Memory Cleared")

def memory_recall():
    global calculation
    calculation = str(memory)
    entry.delete(0, tk.END)
    entry.insert(0, calculation)

def memory_add():
    global memory
    try:
        result = eval(entry.get(), {"__builtins__": None}, math.__dict__)
        memory += result
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Err in M+")

def memory_subtract():
    global memory
    try:
        result = eval(entry.get(), {"__builtins__": None}, math.__dict__)
        memory -= result
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def evaluate_calculation():
    global calculation
    try:
        calculation = str(eval(calculation, {"__builtins__": None}, math.__dict__))
        entry.delete(0, tk.END)
        entry.insert(0, calculation)
    except Exception as e:
        clear_field()
        entry.insert(0, f"Error: {str(e)}")

def clear_field():
    global calculation
    calculation = ""
    entry.delete(0, tk.END)

def backspace():
    global calculation
    calculation = calculation[:-1]
    entry.delete(0, tk.END)
    entry.insert(0, calculation)

def percentage():
    global calculation
    try:
        result = str(eval(calculation, {"__builtins__": None}, math.__dict__) / 100)
        calculation = result
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except:
        clear_field()
        entry.insert(0, "Error")

def apply_theme():
    theme = themes[current_theme]
    root.config(bg=theme["bg"])
    entry.config(bg=theme["entry_bg"], fg=theme["fg"])
    canvas.config(bg=theme["bg"])
    frame.config(bg=theme["bg"])

    scientific_buttons = {"sin", "cos", "tan", "log", "√", "π", "e", "^"}
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Button):
            label = widget["text"]
            if current_theme == "dark" and label in scientific_buttons:
                widget.config(bg="#2a2f4a", fg="#00ffcc", activebackground="#3a3f5a")
            else:
                widget.config(bg=theme["button_bg"], fg=theme["fg"],
                              activebackground=theme["active_bg"], activeforeground=theme["fg"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

def on_key(event):
    char = event.char
    if char in "0123456789.+-*/()":
        add_to_calculation(char)
    elif event.keysym == "Return":
        evaluate_calculation()
    elif event.keysym == "BackSpace":
        backspace()
    elif char.isalpha():
        entry.delete(0, tk.END)
        entry.insert(0, "Text not allowed")

# --- GUI Setup ---
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("320x500")
root.resizable(False, False)

entry = tk.Entry(root, font=('Arial', 18), bd=10, relief="ridge", width=21, justify="right")
entry.pack(pady=10)

canvas = tk.Canvas(root, height=400, width=300, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Buttons ---
buttons = [
    ("7",), ("8",), ("9",), ("/",),
    ("4",), ("5",), ("6",), ("*",),
    ("1",), ("2",), ("3",), ("-",),
    ("0",), (".",), ("+",), ("=", evaluate_calculation),
    ("sin", lambda: add_to_calculation("sin(")),
    ("cos", lambda: add_to_calculation("cos(")),
    ("tan", lambda: add_to_calculation("tan(")),
    ("log", lambda: add_to_calculation("log10(")),
    ("√", lambda: add_to_calculation("sqrt(")),
    ("π", lambda: add_to_calculation("pi")),
    ("e", lambda: add_to_calculation("e")),
    ("^", lambda: add_to_calculation("**")),
    ("%", percentage),
    ("MC", memory_clear), 
    ("M+", memory_add), 
    ("M-", memory_subtract), 
    ("(",), (")",), 
    ("⌫", backspace),
    ("C", clear_field)
]

row, col = 0, 0
for b in buttons:
    text = b[0]
    cmd = b[1] if len(b) > 1 else lambda t=text: add_to_calculation(t)
    btn = tk.Button(frame, text=text, font=("Arial", 12), height=2, width=6, command=cmd)
    btn.grid(row=row, column=col, padx=2, pady=2)
    col += 1
    if col > 3:
        col = 0
        row += 1

theme_btn = tk.Button(root, text="Toggle Theme", font=("Arial", 12), height=1, command=toggle_theme)
theme_btn.pack(pady=5)

root.bind("<Key>", on_key)
apply_theme()
root.mainloop()