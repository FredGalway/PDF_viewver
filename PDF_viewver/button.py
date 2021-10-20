from tkinter import *
from tkmacosx import Button

root = Tk()
root.geometry("200x200")
browse_btn = Button(root, text='Button', bg='#20bebe', fg='white', font=("Raleway",18), width=150, height=45, borderwidth=0, highlightthickness = 0)
browse_btn.grid(row=0, column=1)

root.mainloop()
