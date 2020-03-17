import socket
from os import popen
import signal
import sys

interrupted = False


def ping(host: str, number=1, timeout_milliseconds=500):
    result = popen(f'ping -w {timeout_milliseconds} -n {number} {host}').read().split('\n')
    timeouts: float = 0
    success = False
    for line in result:
        line: str = line.lower().strip()
        if 'timed out' in line:
            timeouts += 1
            success = False
        elif 'reply from' in line:
            success = True
    return success, timeouts, timeouts / number


def interrupt(sig, frame):
    global interrupted
    interrupted = True
    print("SHIT")


def connect(ip: str, port: int):
    ip = str(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)
    result = sock.connect_ex((ip, int(port)))
    sock.close()
    return result == 0


def network_sweep(port=22, debug=False):
    devices = popen('arp -a').read().split('\n')
    if debug:
        print(f'Using port: {port}')
    connections = 0
    dev_list = {}
    working = []
    for d in devices:
        device = d.strip().split()
        if len(device) == 3:
            ip = device[0]
            mac = device[1]
            typ = device[2]
            if typ.lower() == 'dynamic':
                c = False
                if ping(ip, 2)[0]:
                    c = connect(ip, port)
                if c:
                    connections += 1
                    working.append(ip)
                dev_list[ip] = c
                if debug:
                    print(ip, c)
    if connections == 0:
        if debug:
            print("No devices found")
        force = input('Force check for connections? [y/n]: ')
        if force.lower().strip() == 'y':
            dev_number = input('Please specify number of checks [0, 254]: ')
            dev_number = 0 if dev_number.isspace() or not dev_number.isnumeric() else int(dev_number)
            dev_number = min(254, max(dev_number, 0))
            if debug:
                print(f'Checking {dev_number} devices...')
            for i in range(1, dev_number + 1):
                ip = f'192.168.0.{i}'
                if ip in dev_list:
                    continue
                c = False
                if ping(ip, 2)[0]:
                    c = connect(ip, port)
                if c:
                    connections += 1
                    working.append(ip)
                dev_list[ip] = c
                if debug:
                    print(ip, c)
                if interrupted:
                    break
            if connections == 0:
                if debug:
                    print("No devices found!")
                return None
            if debug:
                print("Found devices:")
                for ip in working:
                    print(f'\t{ip}')
            return working
