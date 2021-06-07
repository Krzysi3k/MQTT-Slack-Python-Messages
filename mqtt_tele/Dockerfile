FROM python:3.8.0-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Europe/Warsaw /etc/localtime && \
    echo "Europe/Warsaw" >  /etc/timezone && \
    apk del tzdata && \
    pip install -r requirements.txt
ENTRYPOINT [ "python", "tele_mqtt_handler.py" ]
