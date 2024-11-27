#!/bin/bash

print_help() {
    cat << EOF
Usage: server-monitor-tool [COMMAND] [OPTIONS]

Available commands:
  call [--update-server --server=ip]          Обновление системы с IP
  call [--restart-server --server=ip]         Перезапуск сервера с IP
  call [--stop --service=name --server=ip]    Остановка службы на сервере
  call [--start --service=name --server=ip]   Запуск службы на сервере
  call [--restart --service=name --server=ip] Перезапуск службы на сервере

  setting [--all]                             Настройка всех параметров (по умолчанию)
  setting [--collect-info]                    Настройка выводимой информации о серверах в подсети
  setting [--crit-params]                     Настройка оповещений при достижении критических параметров на серверах
  setting [--log]                             Настройка логирования

  info []                                     Информация, указанная в конфигурации
  info [--all]                                Получение информации по всем параметрам
  info [--cpu]                                Информация по CPU
  info [--ram]                                Информация по RAM
  info [--connection]                         Информация по сетевым соединениям
  info [--processes]                          Информация по процессам
  info [--os]                                 Информация по ОС
  info [--output=html|json|text|console]      Информация в текстовом формате в консоль (по умолчанию)
  info [--ip=ip]                              Информация для конкретного сервера

  add-monitor [--dest=ip --password=password] Добавление сервера в мониторинг
  remove-monitor [--dest=ip]                  Удаление сервера из мониторинга
  clear-monitor                               Сброс всех настроек по мониторингу
  
  daemon [--start --ip=ip/mask]               Запуск демона
  daemon [--restart --ip=ip/mask]             Перезапуск демона для другой подсети
  daemon [--stop]                             Остановка демона
EOF
}

declare -A seen_args

check_duplicates() {
    for arg in "$@"; do
        if [[ -n "${seen_args[$arg]}" ]]; then
            echo "Ошибка: аргумент '$arg' уже был использован."
            return 1
        else
            seen_args["$arg"]=1
        fi
    done

    return 0
}

check_single_argument() {
    local count=0
    local valid_args=("${@:1:$(($#-1))}")
    local case_args_str="${!#}"
    IFS='|' read -r -a case_args <<< "$case_args_str"

    for arg in "${valid_args[@]}"; do
        for case_arg in "${case_args[@]}"; do
            if [[ "$arg" == "$case_arg" ]]; then
                ((count++))
                break
            fi
        done
    done

    if [[ $count -ne 1 ]]; then
        echo "Ошибка: должен быть задан только один из следующих аргументов: ${case_args[*]}"
        exit 1
    fi
}

call_call_opts() {
    check_single_argument "$@" "--update-server|--restart-server |--stop|--start|--restart"

    local update_server=0
    local restart_server=0
    local stop_service=0
    local start_service=0
    local restart_service=0

    local server_ip=""
    local service_name=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --update-server)
                update_server=1
                ;;
            --restart-server)
                restart_server=1
                ;;
            --stop)
                stop_service=1
                ;;
            --start)
                start_service=1
                ;;
            --restart)
                restart_service=1
                ;;
            --server)
                server_ip="$2"
                shift
                ;;
            --service)
                service_name="$2"
                shift
                ;;
            *)
                echo "Неизвестный параметр: $1"
                exit 1
                ;;
        esac
        shift
    done

    if [[ "$server_ip" == "" ]]; then
        echo "Отстуствует параметр --server"
        exit 1
    fi

    if [[ "$update_server" == "1" ]]; then
        call_update_server "$server_ip"
    elif [[ "$restart_server" == "1" ]]; then
        call_restart_server "$server_ip"
    elif [[ "$stop_service" == "1" && "$service_name" != "" ]]; then
        call_stop_service "$server_ip" "$service_name"
    elif [[ "$start_service" == "1" && "$service_name" != "" ]]; then
        call_start_service "$server_ip" "$service_name"
    elif [[ "$restart_service" == "1" && "$service_name" != "" ]]; then
        call_restart_service "$server_ip" "$service_name"
    else
        echo "Отстуствует параметр --service"
        exit 1
    fi

    return 0
}

call_setting_opts() {
    if [[ $# -eq 0 ]]; then
        call_settings "--all"
        return 0
    fi

    local all=0
    local collect_info=0
    local crit_params=0
    local log=0

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all)
                all=1
                ;;
            --collect-info)
                restart_server=1
                ;;
            --crit-params)
                update_server=1
                ;;
            --log)
                restart_server=1
                ;;
            *)
                echo "Неизвестный параметр: $1"
                exit 1
                ;;
        esac
        shift
    done

    if [[ "$all" == "1" ]]; then
        call_settings "--all"
    fi

    if [[ "$collect_info" == "1" ]]; then
        call_settings "--collect-info"
    fi

    if [[ "$crit_params" == "1" ]]; then
        call_settings "--crit-params"
    fi

    if [[ "$log" == "1" ]]; then
        call_settings "--log"
    fi
}

call_info_opts() {
    if [[ $# -eq 0 ]]; then
        call_info
        return 0
    fi

    local all=0
    local cpu=0
    local ram=0
    local connection=0
    local processes=0
    local os=0
    local output="console"
    local ip=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all)
                all=1
                ;;
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

    if [[ "$output" != "html" && "$output" != "json" && "$output" != "text" && "$output" != "console" ]]; then
        echo "Неизвестная опция: --output=$output"
        exit 1
    fi

    args=""

    if [[ $all ]]; then
        call_info
        return 0
    fi

    if [[ $cpu ]]; then
        args="$args + --cpu "
    fi
    
    if [[ $ram ]]; then
        args="$args + --ram "
    fi

    if [[ $connection ]]; then
        args="$args + --connection "
    fi

    if [[ $processes ]]; then
        args="$args + --processes "
    fi

    if [[ $os ]]; then
        args="$args + --os "
    fi

    if [[ $ip ]]; then
        args="$args + --ip "
    fi

    if [[ $output ]]; then
        args="$args + $output"
    fi

    call_info "$args"
}

call_add_monitor_opts() {
    local dest_ip=""
    local password=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dest)
                dest_ip="$2"
                shift
                ;;
            --password)
                password="$2"
                shift
                ;;
            *)
                echo "Неизвестный аргумент: $1"
                exit 1
                ;;
        esac
        shift
    done

    if [[ -z "$dest_ip" ]]; then
        echo "Ошибка: аргумент --dest обязателен и должен содержать IP-адрес."
        exit 1
    fi

    if [[ -z "$password" ]]; then
        echo "Ошибка: аргумент --password обязателен и должен содержать пароль."
        exit 1
    fi

    call_add_monitor "$dest_ip" "$password"
}

call_remove_monitor_opts() {
    local dest_ip=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dest)
                dest_ip="$2"
                shift
                ;;
            *)
                echo "Неизвестный аргумент: $1"
                exit 1
                ;;
        esac
        shift
    done

    if [[ -z "$dest_ip" ]]; then
        echo "Ошибка: аргумент --dest обязателен и должен содержать IP-адрес."
        exit 1
    fi

    call_remove_monitor "$dest_ip"
}

call_clear_monitor_opts() {
    call_clear_monitor
}

call_daemon_opts() {
    check_single_argument "$@" "--start|--stop|--restart"

    local start=0
    local restart=0
    local stop=0

    local net_ip=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --start)
                start=1
                ;;
            --restart)
                restart=1
                ;;
            --stop)
                stop=1
                ;;
            --net_ip)
                net_ip="$2"
                shift
                ;;
            *)
                echo "Неизвестный аргумент: $1"
                exit 1
                ;;
        esac
        shift
    done

    if [[ "$stop" == "1" ]]; then
        daemon_stop
    elif [[ "$start" == "1" ]]; then
        daemon_start "$net_ip"
    elif [[ "$restart" == "1" ]]; then
        daemon_restart "$net_ip"
    fi

    return 0
}

if ! check_duplicates "$@"; then
    exit 1
fi

case "$1" in
call)
    shift 1
    call_call_opts "$@"
    ;;
setting)
    shift 1
    call_setting_opts "$@"
    ;;
info)
    shift 1
    call_info_opts "$@"
    ;;
add-monitor)
    shift 1
    call_add_monitor_opts "$@"
    ;;
remove-monitor)
    shift 1
    call_remove_monitor_opts "$@"
    ;;
clear-monitor)
    shift 1
    call_clar_monitor_opts "$@"
    ;;
daemon)
    shift 1
    call_daemon_opts "$@"
    ;;
--help)
    print_help
    shift
    ;;
*)
    echo "Invalid option"
    print_help
    exit 1
    ;;
esac
