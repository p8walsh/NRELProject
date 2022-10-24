README file for Peter Walsh's ECE 456 Lab 6.

How to use:
    1. Start either rcmddTCP.py or rcmddUDP.py using the command line arguments instructed (Ex: python3 rcmddTCP.py PortNumber)
    2. Then run the matching rcmd script (rcmdTCP.py or rcmdUDP.py, respectively) using the command line arguments as instructed (Ex: python3 rcmdTCP.py ServerName PortNumber ExecutionCount TimeDelay Command)

*Notes:
- If running the TCP version, it is possible to stop mid-execution by typing rcend into the terminal of the rcmd script.
- The rcmdd scripts print out the hostname they are being run on and the port number provided for reference when using the rcmd script.