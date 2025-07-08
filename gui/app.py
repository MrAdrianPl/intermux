import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.interface as interface
from core.router import check_existing_routing_tables, clear_custom_routing_tables

# Allow root to access the X server
subprocess.run("xhost +SI:localuser:root", shell=True, capture_output=True, text=True)

# Elevate privileges if not running as root
if os.geteuid() != 0:
    script_path = os.path.abspath(__file__)
    try:
        os.execvp("pkexec", ["pkexec", "python3", script_path])
    except Exception as e:
        print(f"[X] Failed to elevate with pkexec: {e}")
        sys.exit(1)


# Ensure DISPLAY and XAUTHORITY are set for GUI applications
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":1"
if "XAUTHORITY" not in os.environ:
    os.environ["XAUTHORITY"] = f"/home/{os.getenv('SUDO_USER')}/.Xauthority"



def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[!] Failed: {cmd}")
        print(f"[✗] stderr: {result.stderr.strip()}")
    else:
        print(f"[✓] Ran: {cmd}")
    
    return result.stdout.strip()

def refresh():
    global interface_names
    interfaces = interface.get_active_interfaces()
    interface_names = [i['name'] for i in interfaces if i['flag'] == 'UP' and i['ip_addresses']]
    interface_combo['values'] = interface_names
    if not interface_names:
        interface_combo.set("No active interfaces found")
    else:
        interface_combo.set(interface_names[0])  # Set first available as default 

def add_path():
    app = path_entry.get()
    iface = interface_combo.get()
    if not app or not iface:
        messagebox.showerror("Error", "Please enter a valid application path and select an interface.")
        return
    if app:
        selected_paths.insert(tk.END, f"{app} -> {iface}")
        path_entry.delete(0, tk.END)

        return app, iface

def clear_all():
    if not selected_paths.size() and not created_paths.size():
        messagebox.showinfo("Info", "No paths to clear.")
        return
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all paths?"):
        clear_custom_routing_tables()
        messagebox.showinfo("Success", "All paths cleared successfully!")
        # Clear the listboxes and entry
        selected_paths.delete(0, tk.END)
        created_paths.delete(0, tk.END)
        path_entry.delete(0, tk.END)

def routing():

    if check_existing_routing_tables():
        # messagebox.showinfo("Info", "Routing tables already exist. No need to create again.")
        return
    
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/router.py'))

    create_cmd = ['pkexec', 'python3', script_path]
    create_result = subprocess.run(create_cmd)
    if create_result.returncode == 0:
        # messagebox.showinfo("Success", "All routing tables created successfully!\nTaking you to the configure page...")
        pass
    else:
        messagebox.showerror("Error", f"Failed to create routing tables:\n{create_result.stderr}")

def assign():

    app_interface = selected_paths.get(first=0, last=tk.END)
    
    app_dict = dict()
    for item in app_interface:
        app, iface = item.split(" -> ")
        app_dict[app] = iface

    print(f"[✓] Assigning paths: {app_dict}")

    for i in selected_paths.get(first= 0, last=tk.END):
        created_paths.insert(tk.END, i)
        selected_paths.delete(0, tk.END)
    routing()

    run_cmd(f"sudo ip netns add ns_wlan0")
    run_cmd("sudo ip link add veth0 type veth peer name veth1")
    run_cmd("sudo ip link set veth1 netns ns_wlan0")
    run_cmd("sudo ip addr add 10.0.0.1/24 dev veth0")
    run_cmd("sudo ip link set veth0 up")
    run_cmd("sudo mkdir -p /etc/netns/ns_wlan0/tmp")
    run_cmd('''sudo ip netns exec ns_wlan0 env \
               DISPLAY=$DISPLAY \
               XAUTHORITY=$HOME/.Xauthority \
               firefox --no-remote''')


def clear_routing_tables():
    if not check_existing_routing_tables():
        messagebox.showinfo("Info", "No custom routing tables found to clear.")
        return
    
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all custom routing tables?"):
        clear_custom_routing_tables()
        messagebox.showinfo("Success", "All custom routing tables cleared successfully!")
    else:
        messagebox.showinfo("Cancelled", "Clearing of routing tables cancelled.")


# Create main window
root = tk.Tk()
root.title("Network Interface Binding")
root.geometry("800x600")

# Configure network tool theme colors
bg_color = "#0d1117"        # GitHub dark theme background
fg_color = "#c9d1d9"        # Light gray text
entry_bg = "#161b22"        # Slightly lighter background
button_bg = "#21262d"       # Dark button background
button_fg = "#58a6ff"       # GitHub blue
listbox_bg = "#161b22"      # Same as entry background
listbox_fg = "#c9d1d9"      # Light gray text
border_color = "#30363d"    # GitHub border color
highlight_bg = "#1f6feb"    # GitHub selection blue
title_color = "#58a6ff"     # GitHub blue

# Configure styles
style = ttk.Style()
style.configure("Dark.TFrame", background=bg_color)
style.configure("Dark.TLabel", 
               background=bg_color, 
               foreground=fg_color)
style.configure("Dark.TButton", 
               background=button_bg, 
               foreground=button_fg,
               borderwidth=1)
style.configure("Dark.TLabelframe", 
               background=bg_color, 
               foreground=fg_color)
style.configure("Dark.TLabelframe.Label", 
               background=bg_color, 
               foreground=fg_color)
style.configure("Dark.TEntry", 
               fieldbackground=entry_bg, 
               foreground=fg_color)
style.configure("TCombobox", 
               fieldbackground=entry_bg, 
               background=button_bg,
               foreground=fg_color,
               arrowcolor=fg_color)

# Set window background
root.configure(bg=bg_color)

# Create main frame with padding
main_frame = ttk.Frame(root, padding="20", style="Dark.TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

# Title and Refresh button
title_frame = ttk.Frame(main_frame, style="Dark.TFrame")
title_frame.pack(fill=tk.X, pady=(0, 20))
title_label = ttk.Label(title_frame, 
                       text="Network Interface Binding", 
                       font=('JetBrainsMono Nerd Font', 14, 'bold'), 
                       style="Dark.TLabel",
                       foreground=title_color)
title_label.pack(side=tk.LEFT)
refresh_btn = ttk.Button(title_frame, 
                        text="⟳ Refresh", 
                        width=15, 
                        command=refresh, 
                        style="Dark.TButton")
refresh_btn.pack(side=tk.RIGHT)

# Interface Selection
interface_frame = ttk.Frame(main_frame, style="Dark.TFrame")
interface_frame.pack(fill=tk.X, pady=(0, 10))
interface_label = ttk.Label(interface_frame, 
                          text="$ Select Interface", 
                          width=20, 
                          style="Dark.TLabel",
                          font=('JetBrainsMono Nerd Font', 10))
interface_label.pack(side=tk.LEFT)

interfaces = interface.get_active_interfaces()
interface_names = [i['name'] for i in interfaces if i['flag'] == 'UP' and i['ip_addresses']]

interface_combo = ttk.Combobox(interface_frame, 
                             values=interface_names)
interface_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Application Path
path_frame = ttk.Frame(main_frame, style="Dark.TFrame")
path_frame.pack(fill=tk.X, pady=(0, 10))
path_label = ttk.Label(path_frame, 
                      text="$ Application/Path", 
                      width=20, 
                      style="Dark.TLabel",
                      font=('JetBrainsMono Nerd Font', 10))
path_label.pack(side=tk.LEFT)
path_entry = ttk.Entry(path_frame, style="Dark.TEntry")
path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Add button
add_frame = ttk.Frame(main_frame, style="Dark.TFrame")
add_frame.pack(fill=tk.X, pady=(0, 20))
add_btn = ttk.Button(add_frame, 
                    text="+ Add", 
                    width=15, 
                    command=add_path, 
                    style="Dark.TButton")
add_btn.pack(anchor=tk.CENTER)

# Paths lists frame
paths_frame = ttk.Frame(main_frame, style="Dark.TFrame")
paths_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

# Selected paths
selected_frame = ttk.LabelFrame(paths_frame, 
                              text="Selected paths", 
                              style="Dark.TLabelframe",
                              padding=10)
selected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
selected_paths = tk.Listbox(selected_frame, 
                          bg=listbox_bg, 
                          fg=listbox_fg,
                          selectmode=tk.SINGLE, 
                          borderwidth=1,
                          highlightthickness=1, 
                          highlightbackground=border_color,
                          selectbackground=highlight_bg,
                          selectforeground="#ffffff",
                          relief=tk.FLAT,
                          font=('JetBrainsMono Nerd Font', 10))
selected_paths.pack(fill=tk.BOTH, expand=True)

# Created paths
created_frame = ttk.LabelFrame(paths_frame, 
                             text="Created paths", 
                             style="Dark.TLabelframe",
                             padding=10)
created_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
created_paths = tk.Listbox(created_frame, 
                         bg=listbox_bg, 
                         fg=listbox_fg,
                         selectmode=tk.SINGLE, 
                         borderwidth=1,
                         highlightthickness=1, 
                         highlightbackground=border_color,
                         selectbackground=highlight_bg,
                         selectforeground="#ffffff",
                         relief=tk.FLAT,
                         font=('JetBrainsMono Nerd Font', 10))
created_paths.pack(fill=tk.BOTH, expand=True)

# Bottom buttons frame
bottom_frame = ttk.Frame(main_frame, style="Dark.TFrame")
bottom_frame.pack(fill=tk.X)

# Buttons side by side
buttons_frame = ttk.Frame(bottom_frame, style="Dark.TFrame")
buttons_frame.pack(anchor=tk.CENTER)

assign_btn = ttk.Button(buttons_frame, 
                       text="⚡ Assign", 
                       width=20,
                       command=assign, 
                       style="Dark.TButton")
assign_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(buttons_frame, 
                      text="⌫ Clear everything", 
                      width=20,
                      command=clear_all, 
                      style="Dark.TButton")
clear_btn.pack(side=tk.LEFT, padx=5)

# Start the application
if __name__ == '__main__':
    root.mainloop()
