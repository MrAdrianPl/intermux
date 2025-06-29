import sys
import os
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.interface as interface  # Your module

win = tk.Tk()
win.title("Configure Interface Usage")
win.geometry("700x600")
win.minsize(400, 300)
win.configure(bg='#2E3436')

for i in range(4):
    win.grid_columnconfigure(i, weight=1)

# Header
header = Label(win, text="Bind Applications to Interfaces", bg="#2E3436", fg="white", font=("Arial", 16))
header.grid(row=0, column=0, columnspan=4, pady=20)


#--------FUNCTIONS--------

# Refresh function to update the interface list
def refresh_interfaces():
    global interface_names
    interfaces = interface.get_active_interfaces()
    interface_names = [i['name'] for i in interfaces if i['flag'] == 'UP']
    interface_combo['values'] = interface_names
    if not interface_names:
        interface_combo.set("No active interfaces found")
    else:
        interface_combo.set(interface_names[0])  # Set first available as default 

# Assign logic placeholder
def assign_interface():
    iface = interface_combo.get()
    app = app_entry.get()
    if iface and app:
        assigned_list.insert(END, f"{app} -> {iface}")
        app_entry.delete(0, END)
    else:
        print("Select interface and app")

# Get interfaces
interfaces = interface.get_active_interfaces()
interface_names = [i['name'] for i in interfaces if i['flag'] == 'UP']

#--------LABELS--------

# Interface dropdown
interface_label = Label(win, text="Select Interface:", bg="#2E3436", fg="white")
interface_label.grid(row=1, column=0, padx=10, sticky='e')

# Interface combo box
interface_combo = ttk.Combobox(win, values=interface_names, width=30)
interface_combo.grid(row=1, column=1, padx=10, sticky='w')

# App entry
app_label = Label(win, text="Application Name/Path:", bg="#2E3436", fg="white")
app_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

app_entry = Entry(win, width=35)
app_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

#listbox to show assignments
assigned_label = Label(win, text="Assigned:", bg="#2E3436", fg="white")
assigned_label.grid(row=4, column=0, padx=10, sticky='e')

assigned_list = Listbox(win, width=50, height=10, bg="#555753", fg="white")
assigned_list.grid(row=4, column=1, columnspan=2, pady=10, sticky='w')


#--------BUTTONS--------

# Assign button
assign_button = Button(win, text="Assign", command=assign_interface, bg="#4E9A06", fg="white")
assign_button.grid(row=3, column=1, pady=10)


# Refresh button   
refresh_button = Button(win, text='Refresh', command=refresh_interfaces, bg='#555753', fg='white', activebackground='#555753', activeforeground='white')
refresh_button.grid(row=0, column=2, sticky='e', padx=10, pady=10)

win.mainloop()
