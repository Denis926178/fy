#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/server-monitor

DIR_NAME=$(dirname "$PASSWORD_FILE")
if [ ! -d "$DIR_NAME" ]; then
    echo "Директория $DIR_NAME не существует. Создаю..."
    mkdir -p "$DIR_NAME"
fi

if [ ! -f "$PASSWORD_FILE" ]; then
    echo "Файл $PASSWORD_FILE не существует. Создаю..."
    touch "$PASSWORD_FILE"
fi

DIR_NAME=$(dirname "$MONITOR_HOSTS_FILE")
if [ ! -d "$DIR_NAME" ]; then
    echo "Директория $DIR_NAME не существует. Создаю..."
    mkdir -p "$DIR_NAME"
fi

if [ ! -f "$MONITOR_HOSTS_FILE" ]; then
    echo "Файл $MONITOR_HOSTS_FILE не существует. Создаю..."
    touch "$MONITOR_HOSTS_FILE"
fi

monitor_active_servers $TIMER_MONITOR_NEW_SERVERS &
monitor_servers_temperature $TIMER_MONITOR_CPU_TEMPERATURE &
monitor_servers_disk_space $TIMER_MONITOR_DISK_SPACE &

wait
