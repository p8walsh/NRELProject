import socket
import sys
import time
import threading

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
    print("hello????", flush=True)
    serverAddress = input("Input server address: ")
    if serverAddress == "default":
        serverAddress = "proteus8.ddns.net"
        port = 12344
        exeCount = "5"
        delay = "2"
        command = "time /t"
    else:
        port = int(input("Input port number: "))
        exeCount = str(input("Input number of command executions: "))
        delay = str(input("Input delay between command executions: "))
        command = str(input("Input command: "))

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

