import tkinter as tk
from database import Database
from interface import OrderApp

root = tk.Tk()
db = Database()
app = OrderApp(root, db)

def on_closing():
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
