!WARNING! This code has the potential to cause significant harm! Use extreme caution when using any of the code in this project. More detail in the "Project Overview" section. !WARNING!

README file for Peter Walsh's NREL Interview Project. 

Outline of README:
1. Overview of project, including risks involved with using this code.
2. Installation instructions.
3. Operation instructions.

1. Project Overview:
      This project was made by Peter Walsh in order to gain more experience with development tools including GitHub and Docker and to demonstrate some of his abilities related to network programming.
In short, running the "server.py" script will allow others running the "client.py" script to remotely execute commands on the machine that is running the "server.py" script.
      
      THIS IS POTENTIALLY VERY DANGEROUS. There are currently very few safeguards put in place to prevent unauthorized execution. That means it is possible for an attacker to execute any command on the "server" machine,
including but not limited to: commands that would shutdown the "server" machine, commands that install and run new programs on the "server" machine, commands that send potentially sensitive
files on the "server" machine to other machines, or even commands that could spread malware to other machines that are networked with the "server" machine. It is strongly recommended to use
virtual machines or, as will be explained later, Docker images to execute the "server.py" script to help mitigate harm caused by unauthorized attackers.
      

2. Installation instructions:
      !Before you begin the installation process, please review the information about the potential risks presented in the second paragraph of the Project Overview. Proceed only if you understand
            and accept those risks!
      Note: These installation instructions assume a basic understanding of Docker, Git, Python, Pip, Port Forwarding, and Firewalls. If you have difficulty, please contact the author at p8walsh@gmail.com

      a) Clone this repository. 
      b) Install Python.
      c) Several libraries are necessary for the scripts to run properly. To install, run:
            > pip install tk 
            > pip install cryptography
      d) In order to be able interact with the server remotely, you will need to use port forwarding. On the machine/network that will be running the server script, choose a port that the script 
            will be run on (default is 12344) and forward that port. If you do not choose port 12344, you will need to edit ~line 36~ of server.py to reflect the port you chose.
      Steps are optional, but recommended through step g.
      e) Install Docker.
      f) Open a command prompt window and navigate to the /server folder.
      g) Create a new image. Ex:
            > docker build --tag server .
         More information at https://docs.docker.com/engine/reference/commandline/build/
      End optional steps.

3. Operation instructions:

      a) Start the server on the computer you'd like to remotely connect to. 
            If using Docker, run this command or something similar:
                  > docker run -i --rm -p 0.0.0.0:12344:12344 server
            More information at https://docs.docker.com/engine/reference/commandline/run/

            ! WARNING ! Running this script outside of a virtual machine or Docker container is extremely dangerous, see Project Overview section for more. ! WARNING !
            If not using Docker, run this command:
                  ../NRELProject/server> python server.py [OPTIONAL PORTNUMBER] 
            
         If the server has started properly, you should see the following output (there may be some output before it as well depending on if you used the PORTNUMBER input argument):
            Waiting for data on port [PORTNUMBER]

      b) Start the client on the computer you'd like to remotely connect to the server from.
            Run the following command:
                  ../NRELProject/client> python client.py

         If the client has started properly, there should be a pop-up GUI which prompts you to enter the IP address of the server and the port number the server is listening on.
         NOTE: If the client ever stops responding, try force closing the GUI and restarting at step b. Many errors can be resolved that way without having to restart the server.

      c) Enter the IP address of the server and the port number the server is listening on.

         If this step is successful, that window will close and a new one prompting a password will open. On the server side, there will also be a new line of output saying "Connected to client!"
         If this step is unsuccessful, you will likely have to force close the program and try again from step b.
      
      d) Enter the password. (default is password123, can be changed by editing the plaintext password in server.py)

         If this step is successful, a line of output will appear saying "Authentication Successful!" and the GUI will close and a new GUI wll open.
         If this step is unsuccessful, a line will appear underneath the enter button saying "Authentication Unsuccessful. Try again." and the GUI will not close.

      e) Enter the desired command to run, the number of times to execute that command, and the delay in seconds between executing that command. Pay special attention to the operating system
            the server is running, as that will affect which commands will execute successfully.

            In the default example, command: date, Times to execute command: 5, and Delay between executions: 2, the command date would be executed 5 times with a 2 second delay between each run.
            More complex commands could also be used. For example, one could use the wget command to download files to the server. This illustrates one of many huge security problems with this project,
                  as a knowledgeable attacker could download and then execute malicious programs on the server machine.
      
      f) Repeat step e as many times as desired. To close the session, type "stop" in the command window or simply close the GUI.