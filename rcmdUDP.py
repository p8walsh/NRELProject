import socket
import sys


# Parse input arguments
if len(sys.argv) != 6:
    raise RuntimeError("Wrong Command Line Input!\nServerName PortNumber ExecutionCount TimeDelay Command")
serverAddress = str(sys.argv[1])
port = int(sys.argv[2])
exeCount = str(sys.argv[3])
delay = str(sys.argv[4])
command = str(sys.argv[5])
serverAddressPort = (serverAddress, port)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("Sending command:\nhost:", serverAddress, "\nport:", port, "\nExecution Count:", exeCount, "\nDelay Time:", delay, "\nCommand:", command, "\n")

command = exeCount + ", " + delay + ", " + command

UDPClientSocket.sendto(command.encode("Latin-1"), serverAddressPort)

for i in range(int(exeCount)):
    print("Execution Number:", i)
    msgFromServer, addr = UDPClientSocket.recvfrom(2048)
    print("Time at server:", msgFromServer.decode("Latin-1"))
    msgFromServer, addr = UDPClientSocket.recvfrom(2048)
    print(msgFromServer.decode("Latin-1"))
