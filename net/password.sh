#!/bin/bash

get_password_by_ip() {
    local ip="$1"
    local password=""

    password=$(grep "^$ip=" "$servers_file" | awk '{print $2}')

    return "$password"
}