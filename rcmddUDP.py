import socket
import sys
import time
import subprocess

def parseCommand(command):
    commandList = command.split(", ")
    exeCount = commandList[0]
    delay = commandList[1]
    command = commandList[2]

    return exeCount, delay, command

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
#host = "127.0.0.1"
print(host)

if len(sys.argv) != 2:
    raise RuntimeError("Wrong number of input arguments!\nPlease input only a port number.")
port = int(sys.argv[1])

s.bind((host, port))

while True:
    print("Waiting for data...")
    data, addr = s.recvfrom(2048)
    receivedTime = time.time()
    print("Connected to client!")

    exeCount, delay, command = parseCommand(data.decode("Latin-1"))

    for i in range(int(exeCount)):
        print("Execution Number:", i)
        startTime = time.time()
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        endTime = time.time()
        print("Execution Time:", endTime-startTime, "second(s)")
        print("Execution Output:", output.decode("Latin-1"))
        print("\nOutput Size:", len(output), "bytes\n")

        serverTime = subprocess.check_output("date")
        s.sendto(serverTime, addr)
        s.sendto(output, addr)

        time.sleep(float(delay))