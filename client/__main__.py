import sys
import re
import socket
from ftp_client import FTPClient, IPFormatError


def main(args=None):
    """Entry point for chat_client"""
    ipFormat = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{4,5}$"
    
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
            key = None
            
            if len(sys.argv) == 6:
                key = sys.argv[5]

            #if cipher != "none" and key is None:
                # raise exception, key needs to be set if cipher is not none
            
            if not re.match(ipFormat, host_port):
                host_port_split = host_port.split(":")
                if len(host_port_split) != 2:
                    raise IPFormatError("!! {0} is an invalid port/ip. Must be of the form host:port".format(host_port)) 
                port = int(host_port_split[1])
                (host, aliaslist, ip) = socket.gethostbyname_ex(host_port_split[0])
                if len(ip) > 0:
                    print("!! {0} is - aliases:{1} ip:{2}".format(host_port_split[1], aliaslist, ip))
                    host_ip = ip[0]
                else:
                    raise IPFormatError("!! Cannot resolve domain: {0}".format(host_port_split[1]))

            client = FTPClient(host_ip, port, command, filename, cipher, key)                            
        except ValueError:
            print("!! {0} does not specify a valid port number.".format(sys.argv[3]))
        except IPFormatError:
            print("!! {0} does not specify a valid ip number.".format(sys.argv[3]))
        finally:
            print("!! Exitting...")

if __name__ == "__main__":
    main()
