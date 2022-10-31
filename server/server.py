import socket
import sys
import time
import subprocess
from cryptography.hazmat.primitives import hashes

import Encrypt

# Set standard message length
std_msg_len = 1024

# Set accepted password !VERY INSECURE!
# TODO: Only store hashed passwords
# TODO: Keep accepted password information in a separate, secure location
password = "password123" + "salt"

# Set keys used for basic encryption !VERY INSECURE!
# TODO: Replace current encryption with Fernet encryption
# TODO: Use better key management, also kept in a separate, secure location
keyList = ["a","b","c","d"]

# Hash the password for comparison with password that is received from user
digest = hashes.Hash(hashes.SHA512())
digest.update(password.encode('Latin-1'))
hashed_password = digest.finalize()
accepted_hashes = [hashed_password]

def parseCommand(command):
    """
    Split instruction that was received into its component parts

    Input: command - string - the data received from the user containing the execution count, the delay, and command separated by a comma and a space
    Returns: exeCount - string - the number of times the command should be repeated
             delay - string - the number of seconds to wait between executing the command
             command - string - the actual command to be executed
    """

    print("command: ", command)
    commandList = command.split(", ")
    exeCount = commandList[0]
    delay = commandList[1]
    command = commandList[2]

    return exeCount, delay, command

# Create the socket and set the host as this computer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"

# If there is no command line input default to this port number
if len(sys.argv) == 1:
    print("No input detected. Using default port number 12344.")
    port = 12344

# If there are too many inputs guide the user on what to use as input arguments
elif len(sys.argv) != 2:
    raise RuntimeError("Wrong number of input arguments!\nPlease input only a port number.")
else:
    port = int(sys.argv[1])

# Bind the socket
s.bind((host, port))

# Continue accepting new connections until this script is stopped
while True:

    print("Waiting for data on port", port)

    # Authenticate password   
    s.listen()
    connection, address = s.accept()
    receivedTime = time.time()
    print("Connected to client!")
    try:
        with connection:
            # Allow multiple password attempts
            # TODO: Add maximum attempts/delay to prevent dictionary attacks
            auth_status = False
            while auth_status == False:
                data = connection.recv(std_msg_len)

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

            # After successful authentication, allow the user to continue inputting commands until the connection is broken
            while True:
                data = connection.recv(std_msg_len).decode("Latin-1")
                exeCount, delay, command = parseCommand(data)

                # Try decrypting the command
                command = Encrypt.encrypt(keyList, command)
                print("\n\nCommand after decryption:", command)

                # If client input command "stop", close connection and go back to waiting for a new connection
                if command == "stop":
                    break

                # For every other command, execute them exeCount number of times
                for i in range(int(exeCount)):
                    print("Execution Number:", i)
                    
                    # Time command execution duration
                    startTime = time.time()

                    # Avoid crashing due to improper commands
                    try:
                        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                    except subprocess.CalledProcessError as e:
                        output = str(e).encode('Latin-1')

                    endTime = time.time()
                    print("Execution Time:", endTime-startTime, "second(s)")
                    print("Execution Output:", output.decode("Latin-1"))
                    print("\nOutput Size:", len(output), "bytes\n")

                    # Get the current time on the server to send to the client
                    serverTime = subprocess.check_output("date", stderr=subprocess.STDOUT, shell=True)
                    connection.send(serverTime)
                    
                    # Add some delay to prevent timing issues
                    time.sleep(0.1)

                    # Send the result of the command
                    connection.send(output)

                    # Wait for the amount of time specified between command execution
                    time.sleep(float(delay))

    # BrokenPipeError can be caused sometimes if the client crashes
    except BrokenPipeError as e:
        print("BrokenPipeError. \nAttempting to exit gracefully.")
        print(e, '\n\n\n')
        
        # Close and reopen the socket
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.bind((host,port))
    
    # IndexError can be caused if the client is closed without using the "quit" command
    except IndexError as e:
        print("IndexError, most likely caused by user closing their window.\nAttempting to exit gracefully.")
        print(e)

        # Close and reopen the socket
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.bind((host,port))
