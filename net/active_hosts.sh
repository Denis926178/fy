#!/bin/bash

source "$(dirname "$0")/password.sh"
source "$(dirname "$0")/config.sh"

read -p "Введите подсеть (например, 192.168.1.0/24): " subnet

if [ -z "$subnet" ]; then
    echo "Подсеть не указана. Скрипт завершен."
    exit 1
fi

active_hosts_file="/tmp/active_hosts.txt"

collect_active_hosts() {
    sudo nmap -sn "$subnet" | sudo grep 'Nmap scan report' | sudo awk '{print $5}' > "$active_hosts_file"
}

PREFIX_COMMAND_EXEC_ON_SERVER="sshpass -p "password" ssh -o StrictHostKeyChecking=no "

complete_command() {
    "$($1)"
    
    if [[ $? -ne 0 ]]; then
        logger -t servers-monitord "Ошибка при выполнении команды: $output"
    else
        echo "$output"
    fi
}

construct_cmd() {
    echo "sshpass -p $2 ssh -o StrictHostKeyChecking=no "root@$server_ip" $1"
}

collect_cpu_info() {
    command_to_complete=top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - \$1 \"%\"}'
    cmd="$(construct_cmd "$password" "$command_to_complete")"
    complete_command "$cmd"
}

collect_ram_info() {

}

collect_active_connections_info() {

}

collect_active_processes_info() {

}

declare -A function_map

function_map["collect_cpu_info"]="$NEED_COLLECT_CPU_INFO collect_cpu_info"
function_map["collect_ram_info"]="$NEED_COLLECT_RAM_INFO collect_ram_info"

gather_server_info() {
    echo "Сбор информации о каждом сервере..."
    while IFS= read -r server_ip; do
        echo "================================"
        echo "Сервер: $server_ip"
        
        for cmd in "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - \$1 \"%\"}'" \
                   "free -h | awk '/Mem:/ {print \$3 \"/\" \$2}'" \
                   "df -h / | awk 'NR==2 {print \$3 \"/\" \$2 \" (\" \$5 \")\"}'" \
                   "ss -tuln" \
                   "ps aux --sort=-%cpu | head -10" \
                   "uname -a"; do
            echo "Выполнение команды: $cmd"
            output=$(sshpass -p "password" ssh -o StrictHostKeyChecking=no "root@$server_ip" "$cmd" 2>&1)
            if [[ $? -ne 0 ]]; then
                echo "Ошибка при выполнении команды: $output"
            else
                echo "$output"
            fi
        done
    done < "$active_hosts_file"
}

# Функция для проверки новых серверов в подсети
check_new_servers() {
    previous_hosts=$(cat "$active_hosts_file")
    while true; do
        collect_active_hosts
        current_hosts=$(cat "$active_hosts_file")
        
        # Если список серверов изменился, собираем информацию
        if [[ "$previous_hosts" != "$current_hosts" ]]; then
            echo "Обнаружены новые или измененные серверы."
            gather_server_info
            previous_hosts="$current_hosts"
        fi
        
        sleep 5  # Пауза между проверками
    done
}

# Запуск проверки новых серверов в фоновом режиме
check_new_servers &


server-monitor-tool 
--help

call --update-server --server=ip
call --restart-server --server=ip

call --stop --service=name --server=ip
call --start --service=name --server=ip
call --restart --service=name --server=ip

setting --collect-info
setting --crit-params
setting --log

info --all # default value
info --cpu
info --ram
info --connection
info --processes
info --os
info --json
info --html
info --text # default value

add-monitor --dest=ip --password=password
remove-monitor --dest
clear-monitor

daemon --restart --ip=ip/mask
