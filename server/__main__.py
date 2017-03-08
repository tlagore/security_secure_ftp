import sys
import numbers
from ftp_server import FTPServer

def main(args=None):
    """Entry point for chat_server

       server port [key]
    
    """
    
    if len(sys.argv) >= 2 and len(sys.argv) < 4:
        try:
            port = int(sys.argv[1]);
            if port > 1024 and port <= 65535:
                if(len(sys.argv) == 3):
                    server = FTPServer(port, sys.argv[2])
                else:
                    server = FTPServer(port, None)
                server.start_server()
            else:
                print("Please specify a port between 1025 and 65535")
                print("Ports 1-1024 are used by common applications...")
                
        except ValueError:
            print("%s is not a valid port number." % sys.argv[1])
        finally:
            print("Exitting...")
        
    else:
        print("Invalid usage. Usage:")
        print("{0} port [key]".format(sys.argv[0]))

            
if __name__ == "__main__":
    main()
