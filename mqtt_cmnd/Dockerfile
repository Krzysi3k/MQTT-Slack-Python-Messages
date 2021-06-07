FROM python:3.8.0-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add mosquitto-clients && \
    pip install -r requirements.txt
ENTRYPOINT [ "python", "cmnd_mqtt_handler.py" ]
