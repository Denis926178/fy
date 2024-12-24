#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/password

run_remote_command() {
    local host_name="$1"
    local command="$2"

    local password=$(get_password "$host_name")
    if [[ $? -ne 0 ]]; then
        return 1
    fi

    sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$host_name" "$command"
    return $?
}

update_server() {
    local host_name="$1"
    run_remote_command "$host_name" "apt-get update && apt-get upgrade -y"
    return $?
}

restart_server() {
    local host_name="$1"
    run_remote_command "$host_name" "reboot"
    return $?
}

stop_service() {
    local service_name="$1"
    local host_name="$2"
    run_remote_command "$host_name" "systemctl stop $service_name"
    return $?
}

start_service() {
    local service_name="$1"
    local host_name="$2"
    run_remote_command "$host_name" "systemctl start $service_name"
    return $?
}

restart_service() {
    local service_name="$1"
    local host_name="$2"
    run_remote_command "$host_name" "systemctl restart $service_name"
    return $?
}
