import sys
import re
from ftp_client import FTPClient, IPFormatError


def main(args=None):
    """Entry point for chat_client"""

    # request this from user at a later point
    if len(sys.argv) < 5:
        print("Invalid usage. Usage:")
        print("{0} {write | read} filename host:port { aes256 | aes128 | none } [key]".format(str(sys.argv[0]))) 
    elif len(sys.argv) > 6:
        print("Invalid usage. Usage:")
        print("{0} {write | read} filename host:port { aes256 | aes128 | none } [key]".format(str(sys.argv[0]))) 
    else:
        try:
            command = str(sys.argv[1])
            filename = str(sys.argv[2])
            host_port = str(sys.argv[3])

            cipher = str(sys.argv[4])
            
            if len(sys.argv) == 6:
                key = sys.argv[5]
                
            if not re.match(ipFormat, host_port):
                raise IPFormatError("Invalid IP format. Must be of the form host:port")
            
            #port = int(sys.argv[2])
            #client = FTPClient(host, port)
        except ValueError:
            print("{0} is not a valid port number.".format(sys.argv[2]))
        except IPFormatError:
            print("{0} is not a valid ip number.".format(sys.argv[3]))
        finally:
            print("Exitting...")

if __name__ == "__main__":
    main()
