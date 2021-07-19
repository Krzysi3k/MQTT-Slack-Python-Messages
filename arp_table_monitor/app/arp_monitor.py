import subprocess
from typing import List, Dict
from pathlib import Path
import os
from datetime import datetime
import requests
from time import sleep


def send_slack_alert(devices: List[str]):
    api_url = 'https://slack.com/api/chat.postMessage'
    token = os.getenv('SLACK_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'channel': '#smart-home',
        'text': f'{now}\nnew device(s) just connected to home network:\n{devices}'
    }
    r = requests.post(api_url, headers=headers, json=data)


def read_arp_table() -> List[Dict[str, str]]:
    p = subprocess.Popen("arp -a | awk '{print $1\",\"$2\",\"$4}'" , shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read().decode('utf-8').split('\n')
    lst = [i for i in output if len(i) > 0 and 'incomplete' not in i]
    
    items = []
    for i in lst:
        elements = i.split(',')
        if elements[0] == '?':
            name = 'unknown'
        else:
            name = elements[0]

        ipaddr = elements[1].replace('(','').replace(')','')
        items.append({
            'name': name,
            'ipaddr': ipaddr,
            'hwaddr': elements[2]
        })

    return items


if __name__ == '__main__':
    while True:
        file = Path(__file__).parent / 'registered_devices.txt'
        new_devices = []
        with open(file=file, mode='r+') as f:
            known_macs = f.read().split('\n')
            current_macs = read_arp_table()
            for i in current_macs:
                if not i['hwaddr'] in known_macs:
                    new_devices.append(i)
                    f.writelines(i['hwaddr'] + '\n')
        if len(new_devices) > 0:
            send_slack_alert(new_devices)
        sleep(60 * 5)