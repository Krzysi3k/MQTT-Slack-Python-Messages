# MQTT Python Slack Messages
## an example project how to use SLACK API and Python to handle MQTT messages

### Python packages used:
|package name |version|
--- | --- |
|paho-mqtt|1.5.1|
|redis|3.5.3|
|requests|2.25.1|

###   project tree:
```
├── mosquitto
│   └── mosquitto.conf
├── mqtt_cmnd
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
├── mqtt_tele
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
├── wireguard
│   └── config
├── docker-compose.yml
├── down.sh
├── readme.MD
└── up.sh
```