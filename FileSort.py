import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def organize_files(path):
    extension_to_folder = {
        '.csv': 'csv files',
        '.png': 'Image files',
        '.jpeg': 'Image files',
        '.jpg': 'Image files',
        '.txt': 'Text files',
        '.mp4': 'Video files',
        '.exe': 'Apps',
        '.pdf': 'Pdf',
        '.docx': 'Documents',
        '.pptx': 'Documents',
        '.torrent': 'Torrent files'
    }

    for folder in set(extension_to_folder.values()):
        folder_path = os.path.join(path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in extension_to_folder:
                destination_folder = os.path.join(path, extension_to_folder[ext])
                destination_path = os.path.join(destination_folder, file)
                if not os.path.exists(destination_path):
                    shutil.move(file_path, destination_path)
                else:
                    print(f"File already exists at destination: {destination_path}")

def start_organizing(path, interval):
    def organize():
        while True:
            organize_files(path)
            threading.Event().wait(interval)
    
    threading.Thread(target=organize, daemon=True).start()

def on_start_click():
    path = filedialog.askdirectory()
    if path:
        try:
            interval = int(interval_entry.get()) * 60  # Convert minutes to seconds
            start_organizing(path, interval)
            messagebox.showinfo("Success", "File organizer started!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the interval.")
    else:
        messagebox.showwarning("Warning", "No directory selected!")

# Create the main window
root = tk.Tk()
root.title("File Organizer")

# Create a frame for the interval input and label
frame = tk.Frame(root)
frame.pack(pady=10)

# Create and pack the interval label and entry
interval_label = tk.Label(frame, text="Enter interval (in minutes):")
interval_label.pack(side=tk.LEFT)
interval_entry = ttk.Entry(frame)
interval_entry.pack(side=tk.LEFT, padx=5)

# Create a button to start organizing files
start_button = tk.Button(root, text="Select Folder and Start Organizing", command=on_start_click)
start_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
