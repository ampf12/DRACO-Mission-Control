from tkinter import *

root = Tk()

def key(event):
    print( "pressed", repr(event.char))

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)


frame = Frame(root, width=100, height=100)
frame.bind("<w>", key)
frame.bind("<a>", key)
frame.bind("<s>", key)
frame.bind("<d>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()