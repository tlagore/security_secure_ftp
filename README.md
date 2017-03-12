### cpsc_526_assignment3

# Authors:
Tyrone Lagore T01 (10151950) James MacIsaac T03 (10063078)

# Desc:
Network data transfer system that uses AES encrypted communications. Contains a client and a server application.

# Running the program
open the package containing the files.
The client and server should be ran in separate folders, as they are organized in the distribution.
We require you to have PyCrypto and python3 to be installed in order to run the program.

## Setting up the venv

To set up an environment to install Pycrypto follow these steps:
   1) install virtualenv using the command
      	      	'pip3 install virtualenv'
   2) create a virtualenv called 'venv' in the project root folder by using the command
      	        'python3 -m venv venv'
   3) activate the venv using
      	        'source venv/bin/activate'
   4) install PyCrypto using
      	        pip3 install pycrypto

You now have a vitualenv with pycrypto ready to run the program.

## Running the server:

enter the 'server' folder that is in the project root folder.

start the server using this command and argument scheme:

      python3 __main__.py <port> [key]

where
      port is the port to listen on
      key is the optional secret key to use for encrypted communications

The server will display it's public facing IP to allow for easy startup of the client.

## Running the client:

enter the 'client' folder that is in the project root folder.

start the client using this command and argument scheme

      python3 __main__.py <read|write> <filename> <host>:<port> <none|aes128|aes256> [key]

where
      mode can be read or write
      filename is the name of the file to be read/written
      host is the host ip that is running the server
      port is the port on the host machine to communicate with the server
      encryption scheme for communications is off/aes128/aes256
      key to use for encryption (not used if no encryption is to happen)

# Test Output:
