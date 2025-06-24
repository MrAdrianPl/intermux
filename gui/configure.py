import sys
import os
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import *
import core.interface as interface

win = tk.Tk()
win.title("Configure")
win.geometry("700x600")
win.minsize(400, 300)
win.configure(bg='#2E3436')

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_columnconfigure(2, weight=1)
win.grid_columnconfigure(3, weight=1)

win.mainloop()