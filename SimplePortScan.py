#!/bin/python
"""
A simple Python port scanner that uses TCP connect scans.
"""

import argparse
import socket
import textwrap
import sys

open_ports = []

def tcp_connect(target_ip, target_port):
    #Tries to connect to a port on a given IP -> if successful, port is open
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((target_ip, int(target_port)))
        open_ports.append(int(target_port))
    except (OSError,OverflowError):
       pass
    finally:
        connection.close() #Close connection
    

def port_scan(target, port_number):
    # Scan the given port
    try:
        target_ip = socket.gethostbyname(target)
        tcp_connect(target_ip, int(port_number))
    except OSError:
        print(f'Cannot resolve {target} : Host Unknown')
        sys.exit()
    

def argument_parser():
    parser = argparse.ArgumentParser(
        description='Simple TCP Port Scanner : Accepts an IP address and port number',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples
            portscan.py -t 10.10.0.1 -p 22,80,443
            portscan.py -t 10.10.0.1 -a
            portscan.py -t 10.10.0.1 --allports
        ''')) 
    parser.add_argument('-t', '--target', required=True, help = 'Target IP address')
    parser.add_argument('-p', '--ports', help = 'List of Ports to scan - comma separated list. For example : 22,80,443,8080')
    parser.add_argument('-a', '--allports', action='store_true', help = 'Scan all ports.')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    try:
        user_args = argument_parser() #Get user arguments
 
    except:
        print('Valid arguments not provided : use the -h flag for information and correct syntax.')
        sys.exit()

    target = user_args['target']

    if user_args['ports']: #If the user provided a list of ports
        port_list = user_args['ports'].split(',') #Get list of ports to scan
        for port in port_list:
            port_scan(target,port)

    elif user_args['allports']: #Scan all ports
        print("Scanning all ports - this may take awhile.")
        for port in range(1,65536):
            port_scan(target,port)

    print(f'Scan results for {target} :')

    if len(open_ports) > 0:
        for port in open_ports:
            print(f"[+] {port} / tcp open")
        print("All other specified ports are closed or filtered.")
    else:
        print("All ports specified are closed or filtered.")       
            




