#!/usr/bin/python3
"""
A simple Python port scanner that uses TCP connect scans.
"""

import argparse
import socket
import textwrap
import sys

open_ports = []

def port_scan(target_ip, target_port):
    #Tries to connect to a port on a given IP -> if successful, port is open
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect((target_ip, int(target_port)))
        open_ports.append(int(target_port))
        connection.close() #Close connection
        
    except (OSError,OverflowError):
        pass

def argument_parser(): #Nice command line tool to accept arguments / nicely handle text wrapping in terminal.
    parser = argparse.ArgumentParser(
        description='Simple TCP Port Scanner : Accepts an IP address or host name and the ports to scan',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples
            portscan.py -h 10.10.0.1 -p 22,80,443
            portscan.py -h 'www.google.com' -p 80,443
            portscan.py -h 10.10.0.1 -a
            portscan.py -h 10.10.0.1 --allports
        ''')) 
    parser.add_argument('-t', '--target', required=True, help = 'Host IP address to scan')
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

    #To scan a list of ports
    if user_args['ports']:
        port_list = user_args['ports'].split(',') 
        for port in port_list:
            port_scan(target,port)
           
    #To scan all ports
    elif user_args['allports']: 
        print("Scanning all ports - this may take awhile.")
        for port in range(1,65536):
            port_scan(target,port)

    print(f'Scan results for {target} :')

    if len(open_ports) > 0:
        for port in open_ports:
            print(f"[+] {port} / tcp open")
        print("All other specified ports are closed or filtered. Program complete")
    else:
        print("All ports specified are closed or filtered.")       
