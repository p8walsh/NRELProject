import socket
import sys
import threading

def normalExecution(serverAddress, port, exeCount, delay, command, serverAddressPort):

    if input() == "rcend":
        print("User Input rcend Detected, stopping program.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((serverAddress, port))
            s.sendto("rcend".encode("Latin-1"), serverAddressPort)
        sys.exit()
    else:
        mainThread.join()
        sys.exit()

if __name__ == '__main__':
    # Parse input arguments
    if len(sys.argv) == 1:
        print("No inputs detected, running default behavior.")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()

        serverAddress = "proteus8.ddns.net"
        port = 12344
        exeCount = "5"
        delay = "2"
        command = "time /t"

    elif len(sys.argv) != 6:
        raise RuntimeError("Wrong Command Line Input!\nServerName PortNumber ExecutionCount TimeDelay Command")
    
    else:
        serverAddress = str(sys.argv[1])
        port = int(sys.argv[2])
        exeCount = str(sys.argv[3])
        delay = str(sys.argv[4])
        command = str(sys.argv[5])
    serverAddressPort = (serverAddress, port)

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
        raise e

