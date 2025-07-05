import tkinter as tk
from tkinter import ttk

def refresh():
    # Placeholder for refresh functionality
    pass

def add_path():
    path = path_entry.get()
    if path:
        selected_paths.insert(tk.END, path)
        path_entry.delete(0, tk.END)

def clear_all():
    selected_paths.delete(0, tk.END)
    created_paths.delete(0, tk.END)
    path_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Bind Apps to interfaces")
root.geometry("800x600")

# Configure modern blue theme colors
bg_color = "#1a1b26"        # Deep navy background
fg_color = "#a9b1d6"        # Soft blue-white text
entry_bg = "#24283b"        # Slightly lighter navy for input fields
button_bg = "#414868"       # Muted blue for buttons
button_fg = "#c0caf5"       # Bright blue-white for button text
listbox_bg = "#24283b"      # Same as entry background
listbox_fg = "#a9b1d6"      # Soft blue-white for list text
border_color = "#565f89"    # Muted blue for borders
highlight_bg = "#3d59a1"    # Soft blue for selection
title_color = "#7aa2f7"     # Bright blue for title
accent_color = "#7dcfff"    # Light blue for accents

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
                       text="Bind Apps to interfaces", 
                       font=('Inter', 14, 'bold'), 
                       style="Dark.TLabel",
                       foreground=title_color)
title_label.pack(side=tk.LEFT)
refresh_btn = ttk.Button(title_frame, 
                        text="Refresh", 
                        width=15, 
                        command=refresh, 
                        style="Dark.TButton")
refresh_btn.pack(side=tk.RIGHT)

# Interface Selection
interface_frame = ttk.Frame(main_frame, style="Dark.TFrame")
interface_frame.pack(fill=tk.X, pady=(0, 10))
interface_label = ttk.Label(interface_frame, 
                          text="Select Interface", 
                          width=20, 
                          style="Dark.TLabel",
                          font=('Inter', 10))
interface_label.pack(side=tk.LEFT)
interface_combo = ttk.Combobox(interface_frame, 
                             values=["eth0", "wlan0", "docker0"])
interface_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Application Path
path_frame = ttk.Frame(main_frame, style="Dark.TFrame")
path_frame.pack(fill=tk.X, pady=(0, 10))
path_label = ttk.Label(path_frame, 
                      text="Application/Path", 
                      width=20, 
                      style="Dark.TLabel",
                      font=('Inter', 10))
path_label.pack(side=tk.LEFT)
path_entry = ttk.Entry(path_frame, style="Dark.TEntry")
path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Add button
add_frame = ttk.Frame(main_frame, style="Dark.TFrame")
add_frame.pack(fill=tk.X, pady=(0, 20))
add_btn = ttk.Button(add_frame, 
                    text="Add", 
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
                          selectforeground=button_fg,
                          relief=tk.FLAT,
                          font=('Inter', 10))
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
                         selectforeground=button_fg,
                         relief=tk.FLAT,
                         font=('Inter', 10))
created_paths.pack(fill=tk.BOTH, expand=True)

# Clear button
clear_frame = ttk.Frame(main_frame, style="Dark.TFrame")
clear_frame.pack(fill=tk.X)
clear_btn = ttk.Button(clear_frame, 
                      text="Clear everything?", 
                      width=20,
                      command=clear_all, 
                      style="Dark.TButton")
clear_btn.pack(anchor=tk.CENTER)

# Start the application
if __name__ == '__main__':
    root.mainloop()
