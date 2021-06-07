import redis
import json
import os
import requests
from datetime import datetime


r = redis.Redis(host='192.168.0.123')


def post_to_slack(slack_msg):
    api_url = 'https://slack.com/api/chat.postMessage'
    token = os.getenv('SLACK_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'channel': '#smart-home',
        'text': f'{now}\n{slack_msg}'
    }
    r = requests.post(api_url, headers=headers, json=data)


def monitor_washing(device, msg):
    '''
    pralka ustawiona na tym topicu: tele/gniazdko-4/SENSOR 
    '''
    washing_state = r.get('washing_state')
    last_value = r.get('last_value')
    counter = r.get('counter')
    json_data = json.loads(msg)
    current_value = json_data['ENERGY']['Today']

    if washing_state is None or last_value is None or counter is None:
        r.set('last_value', current_value)
        r.set('washing_state', 'stopped')
        r.set('counter', 0)
    else:
        last_value = float(last_value)
        counter = int(counter)
        washing_state = washing_state.decode('utf-8')

        if washing_state == 'stopped':
            if current_value > last_value:
                counter += 1
                r.set('counter', counter)
                if counter >= 3:
                    print('register: washing started')
                    r.set('washing_state', 'started')
                    r.set('counter', 0)
            else:
                r.set('counter', 0)
        elif washing_state == 'started':
            if current_value == last_value:
                counter += 1
                r.set('counter', counter)
                if counter >= 2:
                    print('register: washing is finished')
                    r.set('washing_state', 'stopped')
                    r.set('counter', 0)
                    post_to_slack('wyjmij pranie')
            else:
                r.set('counter', 0)

        r.set('last_value', current_value)
        print(f'current counter: {counter} current value: {current_value}')


# topic full name: eg. tele/gniazdko-4/SENSOR
SENSOR = {
    'gniazdko-4': monitor_washing
}