# This program is a simple utility that sends packets on the SSDP Multicast
# group. The goal here is to simplify both manual and automatic testing.
# generate.py should be run before this program, as to generate the SSDP
# packets required.
#
# To send a NOTIFY packet, use:
#   'python send.py [notify|n]'
# To send a MSEARCH packet, use:
#   'python send.py [msearch|m]'
# To build a custom packet, line by line, use:
#   'python send.py [custom|c]

import os
import socket
import sys

USAGE = "Usage: python send.py [notify|msearch|custom]"

MC_GROUP = "239.255.255.250"
MC_PORT = 1900

# Build message via stdin
def build_message():
    message = ""
    while True:
        line = sys.stdin.readline().strip("\n")
        message += line + "\r\n"
        if line == "":
            break
    return message

# Read in from file path
def extract_message(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    message =  "\r\n".join(line.strip("\n") for line in lines) + "\r\n"
    return message

# Send message via multicast
def send(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(message, (MC_GROUP, MC_PORT))

    print("{0} bytes written to {1}:{2}".format(len(message), MC_GROUP,
        MC_PORT))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE)
        exit(1)
    elif sys.argv[1] == "notify" or sys.argv[1] == "n":
        send(extract_message("packets/notify.ssdp"))
    elif sys.argv[1] == "msearch" or sys.argv[1] == "m":
        send(extract_message("packets/msearch.ssdp"))
    elif sys.argv[1] == "custom" or sys.argv[1] == "c":
        send(build_message())
    else:
        print(USAGE)
        exit(1)
