import tkinter as tk
import math
import re
import tkinter.messagebox as msgbox
from math import radians


history_inputs = []
history = []
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

def cross_check_history():
    if not history_inputs:
        msgbox.showinfo("History", "No previous inputs.")
        return

    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Recheck Inputs")
    popup.geometry("300x300")

    label = tk.Label(popup, text="Select an input to recheck or correct:", font=("Arial", 10))
    label.pack(pady=5)

    # Use a Listbox to show previous inputs
    listbox = tk.Listbox(popup, font=("Arial", 12), width=35, height=10)
    listbox.pack(pady=10)

    # Insert all expressions into the listbox
    for expr in history_inputs:
        listbox.insert(tk.END, expr)

# def evaluate_calculation():
#     global calculation
    # try:
    #     calculation = str(eval(calculation, {"__builtins__": None}, math.__dict__))
    #     entry.delete(0, tk.END)
    #     entry.insert(0, calculation)
    # except Exception as e:
    #     clear_field()
    #     entry.insert(0, f"Error: {str(e)}")

def evaluate_calculation():
    global calculation, history, history_inputs
    try:
        # Convert sin, cos, and tan to handle degrees
        calculation = re.sub(r'sin\(([^)]+)\)', r'sin(radians(\1))', calculation)
        calculation = re.sub(r'cos\(([^)]+)\)', r'cos(radians(\1))', calculation)
        calculation = re.sub(r'tan\(([^)]+)\)', r'tan(radians(\1))', calculation)

        # Now evaluate the calculation
        result = eval(calculation, {"__builtins__": None}, math.__dict__)
        result = round(result, 2)

        # Add result to history
        history.append(result)
        history_inputs.append(calculation)
        calculation = str(result)
        entry.delete(0, tk.END)
        entry.insert(0, calculation)

    except Exception as e:
        # If there's an error, clear the field and show the error message
        clear_field()
        entry.insert(0, f"Error: {str(e)}")
    # try:
    #     result = eval(calculation, {"__builtins__": None}, math.__dict__)
    #     calculation = str(result)
    #     history.append(result)  # Store result in history
    #     entry.delete(0, tk.END)
    #     entry.insert(0, calculation)
    # except Exception as e:
    #     clear_field()
    #     entry.insert(0, f"Error: {str(e)}")

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

def cross_check_history():
    if not history_inputs:
        msgbox.showinfo("History", "No previous inputs.")
        return

    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Recheck Inputs")
    popup.geometry("300x300")

    # Add label to prompt user
    label = tk.Label(popup, text="Select an input to recheck or correct:", font=("Arial", 10))
    label.pack(pady=5)

    # Create a Listbox to show previous inputs
    listbox = tk.Listbox(popup, font=("Arial", 12), width=35, height=10)
    listbox.pack(pady=10)

    # Insert all expressions into the listbox
    for expr in history_inputs:
        listbox.insert(tk.END, expr)


    # Function to handle selection
    def load_selected_input():
        selected = listbox.curselection()  # Get the index of the selected item
        if selected:
            expr = listbox.get(selected[0])  # Get the selected input expression
            global calculation
            calculation = expr  # Set the global calculation to the selected expression
            entry.delete(0, tk.END)  # Clear the current entry field
            entry.insert(0, expr)  # Load the selected expression into the entry
            popup.destroy()  # Close the popup window
        else:
            msgbox.showwarning("No selection", "Please select an input to recheck.")
    select_btn = tk.Button(popup, text="Load to Calculator", command=load_selected_input)
    select_btn.pack(pady=5)

    # # Insert all expressions into the listbox
    # for expr in history_inputs:
    #     listbox.insert(tk.END, expr)
    #     def load_selected_input():
    #     selected = listbox.curselection()
    #     if selected:
    #         expr = listbox.get(selected[0])
    #         global calculation
    #         calculation = expr
    #         entry.delete(0, tk.END)
    #         entry.insert(0, expr)
    #         popup.destroy()

    # Button to confirm selection
    
# --- GUI Setup ---
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("320x500")
root.resizable(False, False)
entry = tk.Entry(root, font=('Arial', 18), bd=10, relief="ridge", width=21, justify="right")
entry.pack(pady=10)
# entry = tk.Entry(root, font=('Arial', 18), bd=10, relief="ridge", width=21, justify="right")
# entry.pack(pady=10)
# select_btn = tk.Button(popup, text="Load to Calculator", command=load_selected_input)
# select_btn.pack(pady=5)

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
    ("C", clear_field),
    
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

check_all_btn = tk.Button(frame, text="Check All", font=("Arial", 12), height=2, width=26, command=cross_check_history)
check_all_btn.grid(row=row + 1, column=0, columnspan=4, padx=2, pady=5)

theme_btn = tk.Button(root, text="Toggle Theme", font=("Arial", 12), height=1, command=toggle_theme)
theme_btn.pack(pady=5)

root.bind("<Key>", on_key)
apply_theme()
root.mainloop()