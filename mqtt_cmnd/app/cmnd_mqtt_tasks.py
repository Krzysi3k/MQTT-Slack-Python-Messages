import subprocess
import struct
import socket


def wol_status(hostname, msg):

    hostnames_ip = {
        'hypervisor': '192.168.0.124'
    }

    ip_addr = hostnames_ip.get(hostname, None)
    if ip_addr is not None:
        p = subprocess.Popen(f'ping -c 1 {ip_addr}', shell=True, stdout=subprocess.PIPE)
        output = p.stdout.read().decode('utf-8')
        if ' 0% packet loss' in output:
            subprocess.Popen("/usr/bin/mosquitto_pub -h 192.168.0.123 -t 'tele/hypervisor/wol_status' -m 'ON'", shell=True)
        else:
            subprocess.Popen("/usr/bin/mosquitto_pub -h 192.168.0.123 -t 'tele/hypervisor/wol_status' -m 'OFF'", shell=True)


def wol(hostname, msg):
    if msg == 'ON':
        hosts_mac = {
            'hypervisor':'A1-A2-A3-A4-A5-A6',
            'stacjonara':'B1-B2-B3-B4-B5-B6'
        }

        mac = hosts_mac.get(hostname, None)
        if mac is not None:
            macaddress = mac.replace(mac[2], '')
            print(macaddress)
            # Pad the synchronization stream
            data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
            send_data = b''
            # Split up the hex values in pack
            for i in range(0, len(data), 2):
                send_data += struct.pack('B', int(data[i: i + 2], 16))

            # Broadcast it to the LAN
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(send_data, ('255.255.255.255',7))
            print("magic packet sent")
        else:
            print('MAC address not found')