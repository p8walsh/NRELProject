import socket
import sys
import time
import subprocess

X = 1024

def parseCommand(command):
    commandList = command.split(", ")
    exeCount = commandList[0]
    delay = commandList[1]
    command = commandList[2]

    return exeCount, delay, command

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
#host = "127.0.0.1"
print(host)

if len(sys.argv) != 2:
    raise RuntimeError("Wrong number of input arguments!\nPlease input only a port number.")
port = int(sys.argv[1])


s.bind((host, port))

while True:
    print("Waiting for data on port", port)
    s.listen()
    connection, address = s.accept()
    receivedTime = time.time()
    print("Connected to client!")
    try:
        with connection:
            data = connection.recv(X).decode("Latin-1")
            exeCount, delay, command = parseCommand(data)
            print("Received Command:", data)

            for i in range(int(exeCount)):
                print("Execution Number:", i)
                startTime = time.time()
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                endTime = time.time()
                print("Execution Time:", endTime-startTime, "second(s)")
                print("Execution Output:", output.decode("Latin-1"))
                print("\nOutput Size:", len(output), "bytes\n")

                serverTime = subprocess.check_output("date")
                connection.send(serverTime)
                connection.send(output)

                time.sleep(float(delay))
    except BrokenPipeError as e:
        print("BrokenPipeError, most likely caused by rcend command on client side.\nAttempting to exit gracefully.")
        print(e, '\n\n\n')
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.bind((host,port))