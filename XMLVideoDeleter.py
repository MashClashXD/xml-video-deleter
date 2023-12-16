import os
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import tkinter as tk
from tkinter import filedialog
import json

# Configuration file for whitelist
CONFIG_FILE = "config.json"

def save_config(whitelist_folders):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(whitelist_folders, config_file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    else:
        return []

def parse_xml_and_delete(xml_file, whitelist_folders):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all path URLs in the XML
    path_elements = root.findall('.//pathurl')

    # Iterate through path URLs
    for path_element in path_elements:
        # Extract the path from the URL and unquote it
        path_url = path_element.text
        path = unquote(path_url.replace('file://localhost/', ''))

        # Check if the path is in a whitelisted folder
        for folder in whitelist_folders:
            if folder.lower() in path.lower():
                try:
                    os.remove(path)
                    print(f"Deleted: {path}")
                except FileNotFoundError:
                    print(f"File not found: {path}")
                except Exception as e:
                    print(f"Error deleting file {path}: {e}")
                break
        else:
            # If the path is not in any whitelisted folder, skip deletion
            print(f"Skipped: {path} (not in whitelisted folder)")

def browse_file_path():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    entry_var.set(file_path)

def add_folder():
    folder_path = filedialog.askdirectory()
    whitelist_listbox.insert(tk.END, folder_path)
    save_config(whitelist_listbox.get(0, tk.END))

def delete_selected_folder():
    selected_index = whitelist_listbox.curselection()
    if selected_index:
        whitelist_listbox.delete(selected_index)
        save_config(whitelist_listbox.get(0, tk.END))

# Create the main window
root = tk.Tk()
root.title("XML File Deletion Tool")

# Load whitelist from config
whitelist_folders = load_config()

# Create a StringVar to store the selected file path
entry_var = tk.StringVar()

# Create widgets
label = tk.Label(root, text="Select XML File:")
entry = tk.Entry(root, textvariable=entry_var, width=50)
browse_button = tk.Button(root, text="Browse", command=browse_file_path)

whitelist_label = tk.Label(root, text="Whitelist Folders:")
whitelist_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5)
add_button = tk.Button(root, text="Add Folder", command=add_folder)
delete_button = tk.Button(root, text="Delete Files", command=lambda: parse_xml_and_delete(entry_var.get(), whitelist_listbox.get(0, tk.END)))

# Populate the whitelist Listbox with loaded folders
for folder in whitelist_folders:
    whitelist_listbox.insert(tk.END, folder)

# Layout widgets
label.grid(row=0, column=0, padx=10, pady=10)
entry.grid(row=0, column=1, padx=10, pady=10)
browse_button.grid(row=0, column=2, padx=10, pady=10)

whitelist_label.grid(row=1, column=0, padx=10, pady=10)
whitelist_listbox.grid(row=1, column=1, padx=10, pady=10)
add_button.grid(row=1, column=2, padx=10, pady=10)
delete_button.grid(row=1, column=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
