# Generate the packets used for SSDP. They will be written to the packets
# folder. A new advertisement UUID is generated each time this program is run.

import platform
import socket
import uuid

# Get the IPv4 address that this device will advertise as its own
def get_ipv4():
    return socket.gethostbyname(socket.gethostname())

# Get the UUID that this device will advertise as its own
def get_uuid():
    return str(uuid.uuid4())

# Get the operating system name that will appear in this device's
# notify advertisement, in the SERVER header.
def get_os():
    return platform.system()

# Get the operating system's version that will appear in this device's
# notify advertisement, in the SERVER header.
def get_os_version():
    return platform.release()

# Generate the SSDP NOTIFY packet
def generate_notify():

    os = get_os() + "/" + get_os_version()
    prod = "TestProduct/5.5"

    m = [
            "NOTIFY * HTTP/1.1",
            "NT:upnp:rootdevice",
            "NTS:ssdp:update",
            "LOCATION:http://" + get_ipv4() + "/upnp/BasicDevice.xml",
            "USN:uuid:" + get_uuid() + "::upnp:rootdevice",
            "CACHE-CONTROL:max-age=1230",
            "SERVER: " + os + " UPnP/1.0 " + prod,
            "EXT:",
        ]
    return "\n".join(m)

# Generate the SSDP MSEARCH packet
def generate_msearch():
    m = [
            "M-SEARCH * HTTP/1.1",
            "HOST: 239.255.255.250:1900",
            "ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1",
            "MAN: \"ssdp:discover\"",
            "MX: 1",
        ]
    return "\n".join(m)

# Generate the packets used for SSDP testing
def generate():
    with open("packets/notify.ssdp", "w") as f:
        f.write(generate_notify())
        f.close()
        print("notify.ssdp")
   
    with open("packets/msearch.ssdp", "w") as f:
        f.write(generate_msearch())
        f.close()
        print("msearch.ssdp")

if __name__ == "__main__":
    generate()
