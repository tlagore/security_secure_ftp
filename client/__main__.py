import sys
import re
import socket
import traceback
from ftp_client import FTPClient, IPFormatError

def main(args=None):
    """Entry point for chat_client"""

    
    if len(sys.argv) < 5:
        print("Invalid usage. Usage:")
        print("{0} {{ write | read }} filename host:port {{ aes256 | aes128 | none }} [key]".format(str(sys.argv[0]))) 
    elif len(sys.argv) > 6:
        print("Invalid usage. Usage:")
        print("{0} {{ write | read }} filename host:port {{ aes256 | aes128 | none }} [key]".format(str(sys.argv[0]))) 
    else:
        try:
            command = str(sys.argv[1])

            # make sure command is properly specified
            if command != "read" and command != "write":
                raise Exception("'command' must be 'read' or 'write'")
            
            filename = str(sys.argv[2])
            host_port = str(sys.argv[3])
            cipher = str(sys.argv[4]).lower()
            key = None
            
            if len(sys.argv) == 6:
                key = str(sys.argv[5])

            # make sure cipher is properly specified
            if cipher != "aes256" and cipher != "aes128" and cipher != "none":
                raise Exception("cipher must be one of 'aes256', 'aes128', or 'none'")
                
            # raise exception, key needs to be set if cipher is not none                
            if cipher != "none" and key is None:
                raise Exception("key must be specified if cipher is not equal to 'none'")
            elif cipher == "aes256" and len(key) != 32:
                raise Exception("key must be 32 bytes if cipher is 'aes256'")
            elif cipher == "aes128" and len(key) != 16:
                raise Exception("key must be 16 bytes if cipher is 'aes128'")                 
    
            (host_ip, port) = domain_resolution(host_port)
            client = FTPClient(host_ip, port, command, filename, cipher, key)   
        except ValueError:
            print("!! {0} does not specify a valid port number.".format(sys.argv[3]))
            print(traceback.format_exc())
        except IPFormatError:
            print("!! {0} does not specify a valid ip number.".format(sys.argv[3]))
            print(traceback.format_exc())
        except socket.error as ex:
            print("!! Error deriving domain name: {0}".format(type(ex).__name__))
            print(traceback.format_exc())
        except:
            print("!! Error: {0}".format(sys.exc_info()[1]))
            print(traceback.format_exc())
            

def domain_resolution(host_port):
    """ 
    resolves a domain in the format xxx.xxx.xxx.xxx:xxxx[x]
    if the specified domain is an alias, a resolution is attempted
    """
    ipFormat = r"(\d{1,3}\.){3}\d{1,3}:\d{4,5}$"

    # if the host_port combo does not match the ip regex
    if not re.match(ipFormat, host_port):
        # check if it is a host name that needs to be resolved, raise exception if bad format
        host_port_split = host_port.split(":")
        if len(host_port_split) != 2:
            raise IPFormatError("!! {0} is an invalid port/ip. Must be of the form host:port".format(host_port)) 
        port = int(host_port_split[1])
        (host, aliaslist, ip) = socket.gethostbyname_ex(host_port_split[0])
        
        if len(ip) > 0:
            print("!! {0} is - aliases:{1} ips:{2}".format(host_port_split[1], aliaslist, ip))
            host_ip = ip[0]
        else:
            raise IPFormatError("!! Cannot resolve domain: {0}".format(host_port_split[1]))
    else:
        # else host_port combo matches regex and is directly retrievable
        host_port_split = host_port.split(":")
        port = int(host_port_split[1])
        host_ip = host_port_split[0]

    return (host_ip, port)
            
if __name__ == "__main__":
    main()

    
