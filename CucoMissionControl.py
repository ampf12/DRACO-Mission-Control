# Importing tkinter module
from tkinter import *
import socket
from Network_Check import connect as socket_connect
from Network_Check import ping
from time import sleep


def rgb(color, *args):
    if len(args) == 2:
        color = color, args[0], args[1]
    return "#%02x%02x%02x" % color


connected = False

# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("800x600")
root.title("Mission Control")
root.configure(background="black")
connectStatus = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

key_commands = {
    "w": "FORWARD",
    "a": "LEFT",
    "s": "BACK",
    "d": "RIGHT",
    "c": "CLOSE",
    "x": "OPEN",
    "e": "CHECK"
}


# Sends command by openning a conection with server, executing and closing
def SendCommand(command):
    global s
    if not connected:
        return
    print(f"USER>> {command}")
    s.send(str.encode(command))
    reply = s.recv(1024)
    print(f"PI>> {reply.decode('utf-8')}")


# Key detection and distribution to corresponding method
def key(event):
    if event is None:
        return
    key_press = ''
    if not type(event) == str:
        if event.char is None:
            return
        else:
            key_press: str = event.char.lower()
    else:
        key_press = event.lower()
    if key_press in key_commands:
        print(f'Key Press:\t{key_press.upper()}')
        text.config(state=NORMAL)
        text.insert('1.0', f'Key Press:\t{key_press.upper()}\n')
        text.config(state=DISABLED)
        SendCommand(key_commands[key_press])
    else:
        print("Invalid key")
        text.config(state=NORMAL)
        text.insert('1.0', "Invalid key\n")
        text.config(state=DISABLED)


# Click detection
def callback(event):
    print("Mouse Position:", event.x, event.y)


frame = Frame(root, width=50, height=50, bg=rgb(20, 20, 20))
frame.bind("<w>", key)
frame.bind("<a>", key)
frame.bind("<s>", key)
frame.bind("<d>", key)
frame.bind("<c>", key)
frame.bind("<x>", key)
frame.bind("<e>", key)
frame.bind("<Button-1>", callback)


# Connect button reveals moving commands
def ConnectHP():
    # Arrow buttons appear
    # global move
    # move = Button(root, text="Move", command=Move)
    # move.place(x=365, y=200)
    host = '192.168.137.2'
    port = 5560
    global s, connected
    status.config(text='Status: Connecting...')
    print(f"Pinging ip: {host}")
    p = ping(host, 6)
    if p[0]:
        print("PING SUCCESSFUL!")
        print(f"Checking port: {port}")
        connection = socket_connect(host, port)
        if connection:
            s.connect((host, port))
            connected = True
        else:
            print("NO CONNECTION!")
            status.config(text='Status: Not Connected')
    else:
        print("PING FAILED!")
        status.config(text='Status: Not Connected')


# Disconnect button Kills server
def DisconnectHP():
    global s
    # move.destroy()
    # frame.destroy()
    command = "KILL"
    SendCommand(command)
    print("Client has disconnected from Server")
    s.close()


def batteryStatus():
    global connectStatus


# Disconnect button

class Controls:
    def __init__(self, x: int, y: int):
        self.forward = Button(root, text='/\\', bg='black', fg='white', command=lambda: key('w'))
        self.backward = Button(root, text='\\/', bg='black', fg='white', command=lambda: key('s'))
        self.right = Button(root, text='>', bg='black', fg='white', command=lambda: key('d'))
        self.left = Button(root, text='<', bg='black', fg='white', command=lambda: key('a'))

        self.forward.place(x=x, y=y, width=32, height=32)
        self.backward.place(x=x, y=y + 64, width=32, height=32)
        self.right.place(x=x + 32, y=y + 32, width=32, height=32)
        self.left.place(x=x - 32, y=y + 32, width=32, height=32)

    def set_position(self, x: int, y: int):
        self.forward.place(x=x, y=y, width=32, height=32)
        self.backward.place(x=x, y=y + 64, width=32, height=32)
        self.right.place(x=x + 32, y=x + 32, width=32, height=32)
        self.left.place(x=x - 32, y=x + 32, width=32, height=32)


# Battery Level label
battery = Label(root, text="Battery Level: ", bg="black", fg="white")
battery.place(x=0, y=32)

# Status Label widget
status = Label(root, text="Status: Not Connected", bg="black", fg="white")
status.place(x=800 - 128, y=0)

# Time passed label
timeElapsed = Label(root, text="Time Elapsed: 00:00", bg="black", fg="white")
timeElapsed.place(x=0, y=64)

# Object detecting label
# objects = Label(root, text="Object Detecting:", bg="black", fg="white")
# objects.place(x=600, y=60)

# Console
console = Label(root, text="Console", bg="black", fg="white")
console.place(x=650, y=60)

# Camera feed
feed = Label(root, text="Camera Feed", bg="black", fg="white")
feed.place(x=360, y=128)

connect = Button(root, text="Connect", bg=rgb(0, 20, 0), fg="Green", command=ConnectHP)
connect.place(x=0, y=0, width=64)
disconnect = Button(root, text="Disconnect", bg=rgb(20, 0, 0), fg="Red", command=DisconnectHP)
disconnect.place(x=64, y=0, width=80)
frame.focus_set()
frame.place(x=200, y=150, width=400, height=400)
text = Text(root, width=40, height=10, bg=rgb((25, 25, 25)), fg="white", font=("Courier New", 9), highlightthickness=0)
text.place(x=630, y=150, height=290, width=150)  # x=200 #w = 524
text.config(state=DISABLED)
controls = Controls(700 - 16, 550 - 96)

# camera_frame = Label(root, bg=rgb(20,20,20))
# camera_frame.place(x=200,y=150,width=400,height=400)
root.mainloop()
