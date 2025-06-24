import sys
import os
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import *
import core.interface as interface
from tkinter import messagebox, Toplevel

root = tk.Tk()
root.title("Interfaces")
root.geometry("700x600")
root.minsize(400, 300)
root.configure(bg='#2E3436')

# Make all columns expand equally
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)


#--------FUNCTIONS--------

#refresh button function
def refresh():
    interface_list.delete(0, END)  # Step 1: Clear
    interfaces_list = interface.get_active_interfaces()  # Step 2: Get new data
    if not interfaces_list:
        interface_list.insert(END, "No active interfaces found.")
    else:
        for name in interfaces_list:  # Step 3: Fill again
            interface_list.insert(END, f"{name['name']} - {name['flag']} - {name['type']} - {''.join(name['ip_addresses'][0]) if name['ip_addresses'] else 'N/A'}")

#congigure window opening
def open_configure_window():
    script_path = os.path.join(os.path.dirname(__file__), 'configure.py')
    display = os.environ.get("DISPLAY")
    xauth = os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority"))

    env_cmd = f'DISPLAY={display} XAUTHORITY={xauth} {sys.executable} "{script_path}"'
    subprocess.Popen(['pkexec', 'bash', '-c', env_cmd])

#routing button function
def routing():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/router.py'))
    
    result = subprocess.run(['pkexec', 'python3', script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        messagebox.showinfo("Success", "All routing tables created successfully!\nTaking you to the configure page...")
        open_configure_window()
    else:
        messagebox.showerror("Error", f"Routing failed:\n{result.stderr}")

#--------LABELS--------
header = Label(root, text='Available Interfaces', bg='#2E3436', fg='white', font=('Arial', 16))
header.grid(row=0, column=1, pady=10, padx=10, sticky='n')


#--------BUTTONS--------

#refresh button
refresh_button = Button(root, text='Refresh', command=refresh, bg='#555753', fg='white', activebackground='#555753', activeforeground='white')
refresh_button.grid(row=0, column=2, sticky='e', padx=10, pady=10)

#routing button
routing_button = Button(root, text='Create routing tables', command=routing, bg='#555753', fg='white', activebackground='#555753', activeforeground='white')
routing_button.grid(row=2, column=1, sticky='e', padx=10, pady=10)


#--------LISTBOX--------

interface_list = Listbox(root, bg='#555753', fg='white', selectbackground='#555753', selectforeground='white', width=50, height=10)
interfaces_list = interface.get_active_interfaces()
if not interfaces_list:
    interface_list.insert(END, "No active interfaces found.")

for name in interfaces_list:
    interface_list.insert(END, f"{name['name']} - {name['flag']} - {name['type']} - {''.join(name['ip_addresses'][0]) if name['ip_addresses'] else 'N/A'}")
interface_list.grid(row=1, column=0, columnspan=4, pady=20)

root.mainloop()