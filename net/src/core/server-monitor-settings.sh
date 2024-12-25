#!/bin/bash

main() {
    CONFIG_FILE="$LIB_DIR_MONITOR_SERVER/configuration"

    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Файл $CONFIG_FILE не найден."
        exit 1
    fi

    TMP_FILE=$(mktemp)

    edit_setting() {
        local var_name="$1"
        local current_value="$2"
        local prompt="$3"

        echo -n "$prompt [$current_value]: "
        
        read -r user_input

        if [[ -n "$user_input" ]]; then
            echo "$var_name=\"$user_input\"" >> "$TMP_FILE"
            echo "$var_name обновлена до: $user_input"
        else
            echo "$var_name=\"$current_value\"" >> "$TMP_FILE"
            echo "$var_name оставлена без изменений."
        fi
    }

    if [[ $# -gt 0 ]]; then
        for arg in "$@"; do
            if [[ $arg =~ ^--([A-Za-z_]+)=(.*)$ ]]; then
                var_name="${BASH_REMATCH[1]}"
                new_value="${BASH_REMATCH[2]}"

                if grep -q "^$var_name=" "$CONFIG_FILE"; then
                    sed -i "s#^$var_name=.*#$var_name=\"$new_value\"#" "$CONFIG_FILE"
                    echo "$var_name обновлена до: $new_value"
                else
                    echo "Переменная $var_name не найдена в конфигурационном файле."
                fi
                exit 0
            fi
        done
    else
        echo "Редактирование настроек в $CONFIG_FILE:"

        while read -u 3 line; do 
            if [[ -z "$line" || "$line" =~ ^\# ]]; then
                echo "$line" >> "$TMP_FILE"
                continue
            fi

            if [[ $line =~ ^([A-Za-z_]+)=\"(.*)\"$ ]]; then
                var_name="${BASH_REMATCH[1]}"
                current_value="${BASH_REMATCH[2]}"

                case $var_name in
                    SERVER_USER)
                        edit_setting "$var_name" "$current_value" "Введите имя пользователя сервера"
                        ;;
                    MONITOR_SERVERS_TIME)
                        edit_setting "$var_name" "$current_value" "Введите интервал мониторинга серверов (в секундах)"
                        ;;
                    DEFAULT_NET)
                        edit_setting "$var_name" "$current_value" "Введите подсеть для мониторинга"
                        ;;
                    NEED_COLLECT_CPU_INFO)
                        edit_setting "$var_name" "$current_value" "Собирать информацию о CPU? (yes/no)"
                        ;;
                    NEED_COLLECT_RAM_INFO)
                        edit_setting "$var_name" "$current_value" "Собирать информацию о RAM? (yes/no)"
                        ;;
                    NEED_COLLECT_ACTIVE_CONNECTIONS_INFO)
                        edit_setting "$var_name" "$current_value" "Собирать информацию о активных подключениях? (yes/no)"
                        ;;
                    NEED_COLLECT_ACTIVE_PROCESSES_INFO)
                        edit_setting "$var_name" "$current_value" "Собирать информацию о активных процессах? (yes/no)"
                        ;;
                    NEED_COLLECT_VERSION_OS_INFO)
                        edit_setting "$var_name" "$current_value" "Собирать информацию о версии ОС? (yes/no)"
                        ;;
                    CPU_MAX_TEMPERATURE)
                        edit_setting "$var_name" "$current_value" "Введите максимальную температуру CPU (в градусах)"
                        ;;
                    LOW_DISK_SPACE)
                        edit_setting "$var_name" "$current_value" "Введите минимальный уровень свободного места на диске (в ГБ)"
                        ;;
                    PASSWORD_FILE)
                        edit_setting "$var_name" "$current_value" "Введите путь к файлу паролей"
                        ;;
                    MONITOR_HOSTS_FILE)
                        edit_setting "$var_name" "$current_value" "Введите путь к файлу с хостами"
                        ;;
                    *)
                        echo "$line" >> "$TMP_FILE"
                        ;;
                esac
            else
                echo "$line" >> "$TMP_FILE"
            fi
        done 3<"$CONFIG_FILE"
        mv "$TMP_FILE" "$CONFIG_FILE"
    fi

    echo "Настройки обновлены."
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then    
    main "$@"
fi
