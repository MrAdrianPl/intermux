import sys
import os
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.interface as interface

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
    app = app_entry.get().strip()

    if not iface or not app:
        print("[X] Interface or App not selected.")
        return

    namespace = f"ns_{iface}"
    veth_host = f"veth0_{iface}"
    veth_ns = f"veth1_{iface}"
    subnet = "10.200.1"
    ip_host = f"{subnet}.1/24"
    ip_ns = f"{subnet}.2/24"

    try:
        subprocess.run(['sudo', 'ip', 'netns', 'add', namespace], stderr=subprocess.DEVNULL)

        # Delete old veth if exists
        subprocess.run(['sudo', 'ip', 'link', 'del', veth_host], stderr=subprocess.DEVNULL)

        subprocess.run(['sudo', 'ip', 'link', 'add', veth_host, 'type', 'veth', 'peer', 'name', veth_ns], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', veth_ns, 'netns', namespace], check=True)

        subprocess.run(['sudo', 'ip', 'addr', 'add', ip_host, 'dev', veth_host], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', veth_host, 'up'], check=True)

        subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'addr', 'add', ip_ns, 'dev', veth_ns], check=True)
        subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'link', 'set', veth_ns, 'up'], check=True)
        subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'link', 'set', 'lo', 'up'], check=True)

        subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'route', 'add', 'default', 'via', f'{subnet}.1'], check=True)

        subprocess.run([
            'sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING',
            '-s', f'{subnet}.0/24', '-o', iface, '-j', 'MASQUERADE'
        ], stderr=subprocess.DEVNULL)

        subprocess.Popen([
            'sudo', 'ip', 'netns', 'exec', namespace,
            'env',
            f'DISPLAY={os.environ.get("DISPLAY", ":0")}',
            f'XAUTHORITY={os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority"))}',
            app
        ])

        assigned_list.insert(END, f"{app} -> {iface}")
        app_entry.delete(0, END)

    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {e}")
    except Exception as e:
        print(f"[X] Unexpected error: {e}")






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
assigned_label.grid(row=4, column=0, padx=10, sticky='we')

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
