import socket
from tkinter import *
from tkinter import ttk
from cryptography.hazmat.primitives import hashes

import Encrypt

def authenticate(password, socket, serverAddressPort, errormsg, auth_status, password_root):
    """
    Attempts to authenticate the user with the server using the password set by the server.

    Inputs: password - string - the password used in this authentication attempt
            socket - socket.socket - the socket object currently being used to communicate with the server
            serverAddressPort - string - a concatenation of the server's IP address and the port
            errormsg - tkinter.StringVar - used to update the message displayed to the user's GUI
            auth_status - tkinter.BooleanVar - used to update the user's authentication status
            password_root - tkinter.Tk - the GUI object used to close the window on a successful authentication attempt
    """

    # First add salt to password for unique hashing
    password = password + "salt"

    # Then hash password
    digest = hashes.Hash(hashes.SHA512())
    digest.update(password.encode('Latin-1'))
    hashed_password = digest.finalize()

    # Then transmit password
    socket.sendto(hashed_password, serverAddressPort)

    # Recieve response
    msgFromServer, addr = socket.recvfrom(2048)
    msgFromServer = msgFromServer.decode("Latin-1")

    # Handle response
    if msgFromServer == "Authentication Success! Executing command...":
        errormsg.set("Authentication Success! Executing command...")
        auth_status.set(True)
        password_root.destroy()
    else:
        errormsg.set("Authentication Unsuccessful. Try again.")
        auth_status.set(False)

def execute_command(socket, command, exeCount, delay, results, command_root):
    """
    Sends the command input to the server and updates the GUI with the results.

    Inputs: socket - socket.socket - the socket object currently being used to communicate with the server
            command - string - the command to be run on the server
            exeCount - string - the number of times to execute the command
            delay - string - the number of seconds to wait between each execution of the command
            results - tk.StringVar() - used to update the text shown on the GUI with the results of the command's execution
            command_root - tkinter.Tk - the GUI object used to close the window upon receiving the 'stop' command
    """

    # Allow user to close the window by entering 'stop' in the command window
    if command == "stop":
        command_root.destroy()
        
        # Connection still needs to be closed, so the command must still be sent
        # Encrypting the command
        keyList = ["a","b","c","d"]
        command = Encrypt.encrypt(keyList, command)

        # Send the command
        msgToServer = exeCount + ", " + delay + ", " + command
        socket.sendto(msgToServer.encode("Latin-1"), serverAddressPort)

        # Close this program with no error code
        exit(0)


    # Encrypting the command
    keyList = ["a","b","c","d"]
    command = Encrypt.encrypt(keyList, command)

    try:
        print("Sending command:\nhost:", serverAddress, "\nport:", port, "\nExecution Count:", exeCount, "\nDelay Time:", delay, "\nCommand:", command, "\n")

        # Send command
        msgToServer = exeCount + ", " + delay + ", " + command
        socket.sendto(msgToServer.encode("Latin-1"), serverAddressPort)

        # Accept response based on the number of times the command was executed
        for i in range(int(exeCount)):
            print("Execution Number:", i)
            msgFromServer, addr = socket.recvfrom(2048)
            print("Time at server:", msgFromServer.decode("Latin-1"))
            msgFromServer, addr = socket.recvfrom(2048)
            results.set(msgFromServer.decode("Latin-1"))
            print(results.get())


    except Exception as e:
        raise e

if __name__ == '__main__':
    # Establish connection to server
    # Create GUI for inputting Server Address and Port Number
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    serverAddress = StringVar(value="Ex: computer1.ddns.net")
    port = StringVar(value="Ex: 12344")
    

    ttk.Label(frm, text="Server Address: ").grid(column=0, row=0)
    ttk.Entry(frm, textvariable=serverAddress).grid(column=1, row=0)
    ttk.Label(frm, text="Port Number: ").grid(column=0, row=1)
    ttk.Entry(frm, textvariable=port).grid(column=1, row=1)
    ttk.Button(frm, text="Enter", command=root.destroy).grid(column=1, row=2)
    root.bind("<Return>", lambda e: root.destroy())
    root.mainloop()

    # Set variables to the values that were input by user
    serverAddress = serverAddress.get()
    port = int(port.get())

    # Create connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Complete initial connection
        s.connect((serverAddress, port))
        serverAddressPort = (serverAddress, port)

        # Authenticate user
        # Create GUI for inputting password
        password_root = Tk()
        password_frm = ttk.Frame(password_root, padding=10)
        password_frm.grid()
        password = StringVar()
        errormsg = StringVar()
        auth_status = BooleanVar(value=False)
        ttk.Label(password_frm, text="Password: ").grid(column=0, row=0)
        ttk.Entry(password_frm, textvariable=password, show="*").grid(column=1, row=0)
        ttk.Button(password_frm, text="Enter", command=lambda: authenticate(password.get(), s, serverAddressPort, errormsg, auth_status, password_root)).grid(column=1, row=1)
        ttk.Label(password_frm, textvariable=errormsg).grid(column=1, row=2)
        password_root.bind("<Return>", lambda e: authenticate(password.get(), s, serverAddressPort, errormsg, auth_status, password_root))

        password_root.mainloop()

        if auth_status.get() == True:
            print("Authentication Successful!")

        # Allow user to continue entering new commands
        # Create GUI for entering commands
        command_root = Tk()
        command_frm = ttk.Frame(command_root, padding=10)
        command_frm.grid()
        results = StringVar()
        exeCount = StringVar(value="Ex: 5")
        delay = StringVar(value="Ex: 2")
        command = StringVar(value="Ex: date")
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

