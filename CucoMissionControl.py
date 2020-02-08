# Importing tkinter module
from tkinter import *
import socket

# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("800x600")
root.title("Mission Control")
root.configure(background="black")
connectStatus = False

#Sends command by openning a conection with server, executing and closing
def SendCommand(command):
    host = '192.168.137.2'
    port = 5560

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(str.encode(command))
    reply = s.recv(1024)
    print(reply.decode('utf-8'))
    s.close()

#Detects Forward, backward, left or right commands and sends them to SendCommand
#Test method
# def Move():
#     command = 'REPEAT hi'
#     SendCommand(command)

#Move commands
def forward():
    print("w was pressed")
    command = 'FORWARD'
    SendCommand(command)

def right():
    print("d was pressed")
    command = 'RIGHT'
    SendCommand(command)

def left():
    print("a was pressed")
    command = 'LEFT'
    SendCommand(command)

def back():
    print("s was pressed")
    command = 'BACK'
    SendCommand(command)

#Key detection and destribution to corresponding method
def key(event):
    # print("pressed", repr(event.char)
    if repr(event.char) == "'w'":
        forward()
    elif repr(event.char) == "'d'":
        right()
    elif repr(event.char) == "'a'":
        left()
    elif repr(event.char) == "'s'":
        back()
    else:
        print("Invalid key")

# Click detection
def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)

#Connect button reveals moving commands
def ConnectHP():
    #Arrow buttons apprear
    # global move
    # move = Button(root, text="Move", command=Move)
    # move.place(x=365, y=200)

    #Key detection code
    global frame
    frame = Frame(root, width=50, height=50)
    frame.bind("<w>", key)
    frame.bind("<a>", key)
    frame.bind("<s>", key)
    frame.bind("<d>", key)
    frame.bind("<Button-1>", callback)
    frame.pack()


#Disconnect button Kills server
def DisconnectHP():
    # move.destroy()
    frame.destroy()
    command = "KILL"
    SendCommand(command)
    print("Client has disconnected from Server")


def batteryStatus():
    global connectStatus


# Connect button
connect = Button(root, text="Connect", fg="Green", command=ConnectHP)
connect.place(x=370, y=5)

#Disconnect button
disconnect = Button(root, text="Disconnect", fg="Red", command=DisconnectHP)
disconnect.place(x=365, y=60)

# Battery Level label
battery = Label(root, text="Battery Level: ", bg="black", fg="white")
battery.place(x=0, y=5)

# Status Label widget
status = Label(root, text="Status: Not Connected", bg="black", fg="white")
status.place(x=600, y=5)

#Time passed label
timeElapsed = Label(root, text="Time Elapsed: 00:00", bg="black", fg="white")
timeElapsed.place(x=0, y=60)

#Object detecting label
objects = Label(root, text="Object Detecting:", bg="black", fg="white")
objects.place(x=600, y=60)

#Camera feed
feed = Label(root, text="Camera Feed", bg="black", fg="white")
feed.place(x=360, y=130)


# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()