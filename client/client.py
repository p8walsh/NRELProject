import socket
import sys
import time
import threading
from tkinter import *
from tkinter import ttk

import Encrypt

# python3 rcmdTCP.py proteus8.ddns.net 12344 5 2 time

def normalExecution(serverAddress, port, exeCount, delay, command, serverAddressPort):

    if input() == "rcend":
        print("User Input rcend Detected, stopping program.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((serverAddress, port))
            s.sendto("rcend".encode("Latin-1"), serverAddressPort)
        mainThread.join()
        sys.exit()
    else:
        mainThread.join()
        sys.exit()

if __name__ == '__main__':
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    serverAddress = StringVar(value="proteus8.ddns.net")
    port = StringVar(value="12344")
    exeCount = StringVar(value="5")
    delay = StringVar(value="2")
    command = StringVar(value="time /t")

    ttk.Label(frm, text="Server Address: ").grid(column=0, row=0)
    ttk.Entry(frm, textvariable=serverAddress).grid(column=1, row=0)
    ttk.Label(frm, text="Port Number: ").grid(column=0, row=1)
    ttk.Entry(frm, textvariable=port).grid(column=1, row=1)
    ttk.Label(frm, text="Command: ").grid(column=0, row=2)
    ttk.Entry(frm, textvariable=command).grid(column=1, row=2)
    ttk.Label(frm, text="Times to execute command: ").grid(column=0, row=3)
    ttk.Entry(frm, textvariable=exeCount).grid(column=1, row=3)
    ttk.Label(frm, text="Delay between executions: ").grid(column=0, row=4)
    ttk.Entry(frm, textvariable=delay).grid(column=1, row=4)
    ttk.Button(frm, text="Enter", command=root.destroy).grid(column=1, row=5)
    root.bind("<Return>", lambda e: root.destroy())
    root.mainloop()

    serverAddress = serverAddress.get()
    port = int(port.get())
    exeCount = exeCount.get()
    delay = delay.get()
    command = command.get()

    print(serverAddress, port, exeCount, delay, command)

    serverAddressPort = (serverAddress, port)

    # Encrypting the command
    keyList = ["a","b","c","d"]
    command = Encrypt.encrypt(keyList, command)
    print("\n\nCommand after encryption:", command)
    
    args = (serverAddress, port, exeCount, delay, command, serverAddressPort)

    mainThread = threading.Thread(target=normalExecution, args=args)
    mainThread.daemon = True
    try:
        mainThread.start()
        print("Sending command:\nhost:", serverAddress, "\nport:", port, "\nExecution Count:", exeCount, "\nDelay Time:", delay, "\nCommand:", command, "\n")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Complete initial connection
            s.connect((serverAddress, port))
            msgToServer = exeCount + ", " + delay + ", " + command
            s.sendto(msgToServer.encode("Latin-1"), serverAddressPort)

            for i in range(int(exeCount)):
                print("Execution Number:", i)
                msgFromServer, addr = s.recvfrom(2048)
                print("Time at server:", msgFromServer.decode("Latin-1"))
                msgFromServer, addr = s.recvfrom(2048)
                print(msgFromServer.decode("Latin-1"))


    except Exception as e:
        print(e)
        mainThread.join()
        raise e

