from tkinter import messagebox

def display_error_message(title:str, message:str) -> None:
  messagebox.showerror(f"{title}", f"{message}")

def display_info_message(title:str, message:str) -> None:
  messagebox.showinfo(f"{title}", f"{message}")