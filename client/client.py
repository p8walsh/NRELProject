import socket
from tkinter import *
from tkinter import ttk
from cryptography.hazmat.primitives import hashes

import Encrypt

def authenticate(password, socket, serverAddressPort, errormsg, auth_status, password_root):
    # First add salt to password for unique hashing
    password = password + "salt"

    # Then hash password
    digest = hashes.Hash(hashes.SHA512())
    digest.update(password.encode('Latin-1'))
    hashed_password = digest.finalize()
    print(hashed_password)

    # Then transmit password
    socket.sendto(hashed_password, serverAddressPort)
    msgFromServer, addr = socket.recvfrom(2048)
    msgFromServer = msgFromServer.decode("Latin-1")
    if msgFromServer == "Authentication Success! Executing command...":
        errormsg.set("Authentication Success! Executing command...")
        auth_status.set(True)
        password_root.destroy()
    else:
        errormsg.set("Authentication Unsuccessful. Try again.")
        auth_status.set(False)

def execute_command(s, command, exeCount, delay, results, command_root):
    if command == "stop":
        command_root.destroy()
        
        # Encrypting the command
        keyList = ["a","b","c","d"]
        command = Encrypt.encrypt(keyList, command)
        print("\n\nCommand after encryption:", command)

        msgToServer = exeCount + ", " + delay + ", " + command
        s.sendto(msgToServer.encode("Latin-1"), serverAddressPort)

        exit(0)
        
    # Encrypting the command
    keyList = ["a","b","c","d"]
    command = Encrypt.encrypt(keyList, command)
    print("\n\nCommand after encryption:", command)

    try:
        print("Sending command:\nhost:", serverAddress, "\nport:", port, "\nExecution Count:", exeCount, "\nDelay Time:", delay, "\nCommand:", command, "\n")

        msgToServer = exeCount + ", " + delay + ", " + command
        s.sendto(msgToServer.encode("Latin-1"), serverAddressPort)

        for i in range(int(exeCount)):
            print("Execution Number:", i)
            msgFromServer, addr = s.recvfrom(2048)
            print("Time at server:", msgFromServer.decode("Latin-1"))
            msgFromServer, addr = s.recvfrom(2048)
            results.set(msgFromServer.decode("Latin-1"))
            print(results.get())


    except Exception as e:
        raise e

if __name__ == '__main__':
    # Establish connection to server
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    serverAddress = StringVar(value="proteus8.ddns.net")
    #serverAddress = StringVar(value="PetersComputer")
    port = StringVar(value="12344")
    

    ttk.Label(frm, text="Server Address: ").grid(column=0, row=0)
    ttk.Entry(frm, textvariable=serverAddress).grid(column=1, row=0)
    ttk.Label(frm, text="Port Number: ").grid(column=0, row=1)
    ttk.Entry(frm, textvariable=port).grid(column=1, row=1)
    ttk.Button(frm, text="Enter", command=root.destroy).grid(column=1, row=2)
    root.bind("<Return>", lambda e: root.destroy())
    root.mainloop()

    serverAddress = serverAddress.get()
    port = int(port.get())

    # Create connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Complete initial connection
        s.connect((serverAddress, port))
        serverAddressPort = (serverAddress, port)

        # Authenticate user first:
        password_root = Tk()
        password_frm = ttk.Frame(password_root, padding=10)
        password_frm.grid()
        password = StringVar()
        errormsg = StringVar()
        auth_status = BooleanVar(value=False)
        ttk.Label(password_frm, text="Password: ").grid(column=0, row=0)
        ttk.Entry(password_frm, textvariable=password, show="*").grid(column=1, row=0)
        ttk.Button(password_frm, text="Enter", command=password_root.destroy).grid(column=1, row=1)
        ttk.Label(password_frm, textvariable=errormsg).grid(column=1, row=2)
        password_root.bind("<Return>", lambda e: authenticate(password.get(), s, serverAddressPort, errormsg, auth_status, password_root))

        password_root.mainloop()

        print(auth_status.get())

        # Allow user to continue entering new commands
        command_root = Tk()
        command_frm = ttk.Frame(command_root, padding=10)
        command_frm.grid()
        results = StringVar()
        exeCount = StringVar(value="5")
        delay = StringVar(value="2")
        command = StringVar(value="time")
        ttk.Label(command_frm, text="Command: ").grid(column=0, row=0)
        ttk.Entry(command_frm, textvariable=command).grid(column=1, row=0)
        ttk.Label(command_frm, text="Times to execute command: ").grid(column=0, row=1)
        ttk.Entry(command_frm, textvariable=exeCount).grid(column=1, row=1)
        ttk.Label(command_frm, text="Delay between executions: ").grid(column=0, row=2)
        ttk.Entry(command_frm, textvariable=delay).grid(column=1, row=2)
        ttk.Button(command_frm, text="Enter", command=lambda: execute_command(s, command.get(), exeCount.get(), delay.get(), results, command_root)).grid(column=1, row=3)
        ttk.Label(command_frm, textvariable=results).grid(column=1, row=4)
        command_root.bind("<Return>", lambda e: execute_command(s, command.get(), exeCount.get(), delay.get(), results, command_root))

        command_root.mainloop()

