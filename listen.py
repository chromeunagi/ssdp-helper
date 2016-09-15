# Listen in on the UPnP Multicast network and collect SSDP packets for a set
# amount of time. If a target file is provided, the messages collected will
# be written to the file after this program has completed its execution.

import datetime
import os
import socket
import struct
import sys
import time

USAGE = "Usage: python listen.py [seconds] [output file]"

MC_GROUP = "239.255.255.250"
MC_PORT = 1900

def listen(seconds):
    messages = []

    # Create socket and set options
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MC_GROUP, MC_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MC_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(3)

    # Set start time for the timer
    start = time.time()

    # Listen for approximately the input <seconds>
    while time.time() < start + seconds:
        try:
            data, src = sock.recvfrom(1400)
            dt = datetime.datetime.now()

            # Print to std out and add to messages list
            print("{0}\n{1}\n{2}".format(dt, src, str(data)))
            messages += [(datetime.datetime.now(), str(src), data)]
        except:
            pass

    return messages

if __name__ == "__main__":
    # Check usage
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print(USAGE)
        exit(1)

    # Collect messages
    messages = listen(int(sys.argv[1]))

    # Exit if no packets were detected
    if not len(messages):
        print("No packets detected.")
        exit(0)

    # Output the messages. If an output file was specified in as
    # an input argument, the output will be written to that path.
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as f:
            for m in messages:
                f.write("{0}\n{1}\n{2}".format(m[0], m[1], m[2]))
