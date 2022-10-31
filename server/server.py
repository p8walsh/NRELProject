import socket
import sys
import time
import subprocess
from cryptography.hazmat.primitives import hashes

import Encrypt

X = 1024

password = "password123" + "salt"
keyList = ["a","b","c","d"]
digest = hashes.Hash(hashes.SHA512())
digest.update(password.encode('Latin-1'))
hashed_password = digest.finalize()
accepted_hashes = [hashed_password]

def parseCommand(command):
    print("command: ", command)
    commandList = command.split(", ")
    exeCount = commandList[0]
    delay = commandList[1]
    command = commandList[2]

    return exeCount, delay, command

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"

if len(sys.argv) == 1:
    print("No input detected. Using default port number 12344.")
    port = 12344
    
elif len(sys.argv) != 2:
    raise RuntimeError("Wrong number of input arguments!\nPlease input only a port number.")
else:
    port = int(sys.argv[1])

s.bind((host, port))


while True:
    # Authenticate password   
    print("Waiting for data on port", port)
    s.listen()
    connection, address = s.accept()
    receivedTime = time.time()
    print("Connected to client!")
    try:
        with connection:
            auth_status = False
            while auth_status == False:
                data = connection.recv(X)
                #print("Data: ", data)
                #data = data.decode("Latin-1")

                # Decrypt input
                #data = Encrypt.encrypt(keyList, data)

                # Compare hash with accepted password hashes
                for hash in accepted_hashes:
                    print(data, hash, data == hash)
                    if data == hash:
                        auth_status = True          
                if auth_status == True:
                    # Send password succeeded message
                    connection.send(("Authentication Success! Executing command...").encode("Latin-1"))
                else:
                    # Send authentication failed message 
                    connection.send(("Authentication Failed. Try again.").encode("Latin-1"))

            while True:
                data = connection.recv(X).decode("Latin-1")
                print("Data received: ", data)
                exeCount, delay, command = parseCommand(data)

                # Try decrypting the command
                print("Command before decryption:", command)
                command = Encrypt.encrypt(keyList, command)
                print("\n\nCommand after decryption:", command)

                print("Received Command:", data)

                if command == "stop":
                    break

                for i in range(int(exeCount)):
                    print("Execution Number:", i)
                    startTime = time.time()
                    try:
                        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                    except subprocess.CalledProcessError as e:
                        output = str(e).encode('Latin-1')
                    endTime = time.time()
                    print("Execution Time:", endTime-startTime, "second(s)")
                    print("Execution Output:", output.decode("Latin-1"))
                    print("\nOutput Size:", len(output), "bytes\n")

                    serverTime = subprocess.check_output("date", stderr=subprocess.STDOUT, shell=True)
                    connection.send(serverTime)
                    
                    # add some delay to prevent timing issues
                    time.sleep(0.5)

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
    
    except IndexError as e:
        print("IndexError, most likely caused by user closing their window.\nAttempting to exit gracefully.")
        print(e)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.bind((host,port))
