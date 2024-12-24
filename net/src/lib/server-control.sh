#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/configuration
source $LIB_DIR_MONITOR_SERVER/password

add_monitor() {
    local ip=$1
    local passoword=$2

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

    echo "$ip" >> "$MONITOR_HOSTS_FILE"
    
    add_record $ip $password
}

remove_monitor() {
    local ip=$1

    if [ ! -f "$MONITOR_HOSTS_FILE" ]; then
        echo "Файл $MONITOR_HOSTS_FILE не найден. Удаление невозможно."
        return 1
    fi

    if [ ! -f "$PASSWORD_FILE" ]; then
        echo "Файл $PASSWORD_FILE не найден. Удаление невозможно."
        return 1
    fi

    sed -i "/^[[:space:]]*$ip[[:space:]]*$/d" "$MONITOR_HOSTS_FILE"
    delete_record $ip $password
}

clear_monitor() {
    echo "" > $MONITOR_HOSTS_FILE
    echo "" > $PASSWORD_FILE
}
