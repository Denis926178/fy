#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/configuration
source $LIB_DIR_MONITOR_SERVER/password

declare -A monitored_ips
last_checksum=""

update_monitored_ips() {
    current_checksum=$(sha256sum "$MONITOR_HOSTS_FILE" | awk '{print $1}')

    if [[ "$current_checksum" != "$last_checksum" ]]; then
        echo "Файл $MONITOR_HOSTS_FILE изменился, пересчитываем..."

        monitored_ips=()

        while IFS= read -r ip; do
            if [[ -n "$ip" ]]; then
                monitored_ips["$ip"]=1
            fi
        done < "$MONITOR_HOSTS_FILE"

        last_checksum="$current_checksum"
    fi
}

monitor_active_servers() {
    local timer=$1

    while true; do
        update_monitored_ips

        active_ips=$(nmap -sn "$DEFAULT_NET" | grep -oP 'for \K(\d+\.\d+\.\d+\.\d+)')

        for ip in $active_ips; do
            if [[ -z "${monitored_ips[$ip]}" ]]; then
                logger "Найден новый активный сервер: $ip"
            fi
        done

        sleep $timer
    done
}

monitor_servers_temperature() {
    local timer=$1

    while true; do
        update_monitored_ips

        for ip in "${!monitored_ips[@]}"; do
            local password=$(get_password "$ip")
            if [[ $? -ne 0 ]]; then
                return 1
            fi

            local command="awk '{print \$1/1000}' < /sys/class/thermal/thermal_zone0/temp"
            temperature=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$ip" "$command")

            if (( $(echo "$temperature > $CPU_MAX_TEMPERATURE" | bc -l) )); then
                logger "ALERT: Температура процессора на сервере $ip: ${temperature}°C (выше порогового значения)"
            fi
        done

        sleep $timer
    done
}

monitor_servers_disk_space() {
    local timer=$1

    while true; do
        update_monitored_ips

        for ip in "${!monitored_ips[@]}"; do
            local password=$(get_password "$ip")
            if [[ $? -ne 0 ]]; then
                return 1
            fi

            local command="df -h / | awk 'NR==2{print \$5}' | tr -d '%'"
            disk_space=$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$ip" "$command")

            if (( $(echo "$disk_space > $LOW_DISK_SPACE" | bc -l) )); then
                logger "ALERT: Занятое место на диске сервера $ip: ${disk_space}% (выше порогового значения)"
            fi
        done

        sleep $timer
    done
}
