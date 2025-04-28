import tkinter as tk

from PyQt5.QtCore import QTimer
from pygame import mixer

def open_documentation():
    mixer.init()
    mixer.music.load("music.mp3")  # First animation music
    mixer.music.play()

    doc_window = tk.Toplevel(root)
    doc_window.title("Project Documentation")
    doc_window.geometry("800x600")
    doc_window.configure(bg="black")  # Set background color to black

    title_label = tk.Label(doc_window, text="Simple Desktop Based AI Application",
                           font=("Helvetica", 20, "bold"), fg="white", bg="black")  # Set label background to black
    title_label.pack(pady=20)
    QTimer.singleShot(5000, open_documentation)

    text_frame = tk.Frame(doc_window, bg="black")  # Set frame background to black
    text_frame.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame, font=("Consolas", 12), fg="#ffffff", bg="black",
                        yscrollcommand=scrollbar.set, wrap="word", relief="flat")  # Set text area background to black
    text_area.pack(fill="both", expand=True)

    scrollbar.config(command=text_area.yview)

    try:
        with open("Documentation.txt", "r", encoding="utf-8") as file:
            content = file.read()
            text_area.insert(tk.END, content)
    except Exception as e:
        text_area.insert(tk.END, f"Error loading file: {e}")

    text_area.config(state="disabled")

    def continue_action():
        doc_window.destroy()  # Close the documentation window
        print("Continuing to the next step...")

    continue_button = tk.Button(doc_window, text="Continue", command=continue_action, bg="black", fg="white")  # Set button colors
    continue_button.pack(pady=20)

def close():
    root.destroy()

root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")
root.configure(bg="black")  # Set background color to black

open_button = tk.Button(root, text="Open Documentation", command=open_documentation, bg="black", fg="white")  # Set button colors
open_button.pack(pady=20)

# New button for closing
next_button = tk.Button(root, text="Close", command=close, bg="black", fg="white")  # Set button colors
next_button.pack(pady=20)

root.mainloop()
