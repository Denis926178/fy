#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/password

run_remote_command() {
    local host_name="$1"
    local command="$2"

    local password=$(get_password "$host_name")
    if [[ $? -ne 0 ]]; then
        return 1
    fi

    echo "$(sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$host_name" "$command")"
    return $?
}

collect_cpu_info() {
    local host_name="$1"
    local command_to_complete="top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - \$1 \"%\"}'"
    echo "Загрузка процессора: $(run_remote_command "$host_name" "$command_to_complete")"
    return $?
}

collect_ram_info() {
    local host_name="$1"
    command_to_complete="free -h | awk '/Mem:/ {print \$3 \"/\" \$2}'"
    echo "Расход оперативной памяти: $(run_remote_command "$host_name" "$command_to_complete")"
    return $?
}

collect_connection_info() {
    local host_name="$1"
    command_to_complete="ss -tuln"
    echo "$(run_remote_command "$host_name" "$command_to_complete")"
    return $?
}

collect_processes_info() {
    local host_name="$1"
    command_to_complete="ps aux --sort=-%cpu | head -10"
    echo "$(run_remote_command "$host_name" "$command_to_complete")"
    return $?
}

collect_os_info() {
    local host_name="$1"
    command_to_complete="uname -a"
    echo "$(run_remote_command "$host_name" "$command_to_complete")"
    return $?
}

call_info() {
    local ip=""
    local cpu=0
    local ram=0
    local connection=0
    local processes=0
    local os=0
    local output="console"
    local args="$@"

    # Параметры
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --cpu)
                cpu=1
                ;;
            --ram)
                ram=1
                ;;
            --connection)
                connection=1
                ;;
            --processes)
                processes=1
                ;;
            --os)
                os=1
                ;;
            --output)
                output="$2"
                shift
                ;;
            --ip)
                ip="$2"
                shift
                ;;
            *)
                echo "Неизвестный аргумент: $1"
                exit 1
            ;;
        esac
        shift
    done

    if [[ -f "$MONITOR_HOSTS_FILE" ]]; then
        servers=($(cat "$MONITOR_HOSTS_FILE"))
    else
        echo "Файл $MONITOR_HOSTS_FILE не найден!"
        exit 1
    fi

    result=""

    for server_ip in "${servers[@]}"; do
        if [[ -n "$ip" && "$server_ip" != "$ip" ]]; then
            continue
        fi

        server_info="Server IP: $server_ip\n"
    
        if [[ $cpu -eq 1 ]]; then
            cur_info="$(collect_cpu_info $server_ip)"
            server_info="$server_info\n\n$cur_info"
        fi

        if [[ $ram -eq 1 ]]; then
            cur_info="$(collect_ram_info $server_ip)"
            server_info="$server_info\n\n$cur_info"
        fi

        if [[ $connection -eq 1 ]]; then
            cur_info="$(collect_connection_info $server_ip)"
            server_info="$server_info\n\n$cur_info"
        fi

        if [[ $processes -eq 1 ]]; then
            cur_info="$(collect_processes_info $server_ip)"
            server_info="$server_info\n\n$cur_info"
        fi

        if [[ $os -eq 1 ]]; then
            cur_info="$(collect_os_info $server_ip)"
            server_info="$server_info\n\n$cur_info"
        fi

        result="$result\n$server_info\n\n"
    done

    case "$output" in
        json)
            echo "{"
            echo "\"servers\": ["
            first=1
            for server_ip in "${servers[@]}"; do
                if [[ -n "$ip" && "$server_ip" != "$ip" ]]; then
                    continue
                fi
                if [[ $first -eq 1 ]]; then
                    first=0
                else
                    echo ","
                fi
                echo "  {"
                echo "    \"ip\": \"$server_ip\","
                echo "    \"info\": \"$server_info\""
                echo "  }"
            done
            echo "]"
            echo "}"
            ;;
        xml)
            echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            echo "<servers>"
            for server_ip in "${servers[@]}"; do
                if [[ -n "$ip" && "$server_ip" != "$ip" ]]; then
                    continue
                fi
                echo "  <server>"
                echo "    <ip>$server_ip</ip>"
                echo "    <info>$server_info</info>"
                echo "  </server>"
            done
            echo "</servers>"
            ;;
        text)
            echo "$result"
            ;;
        console)
            echo -e "$result"
            ;;
        *)
            echo "Неизвестный формат вывода: $output"
            exit 1
            ;;
    esac
}
