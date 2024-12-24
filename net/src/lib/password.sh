#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/configuration

add_record() {
    local host_name="$1"
    local password="$2"

    if grep -q "^$host_name :" "$PASSWORD_FILE"; then
        echo "Ошибка: запись для хоста '$host_name' уже существует."
        return 1
    fi

    echo "$host_name : $password" >> "$PASSWORD_FILE"
    echo "Запись для хоста '$host_name' добавлена."
    return 0
}

delete_record() {
    local host_name="$1"

    if ! grep -q "^$host_name :" "$PASSWORD_FILE"; then
        echo "Ошибка: запись для хоста '$host_name' не найдена."
        return 1
    fi

    sed -i "/^$host_name :/d" "$PASSWORD_FILE"
    echo "Запись для хоста '$host_name' удалена."
    return 0
}

get_password() {
    local host_name="$1"

    local password=$(grep "^$host_name :" "$PASSWORD_FILE" | cut -d ' ' -f 3-)

    if [[ -z "$password" ]]; then
        echo "Ошибка: запись для хоста '$host_name' не найдена."
        return 1
    fi

    echo "$password"
    return 0
}

update_password() {
    local host_name="$1"
    local new_password="$2"

    if ! grep -q "^$host_name :" "$PASSWORD_FILE"; then
        echo "Ошибка: запись для хоста '$host_name' не найдена."
        return 1
    fi

    sed -i "s/^$host_name : .*/$host_name : $new_password/" "$PASSWORD_FILE"
    echo "Пароль для хоста '$host_name' обновлен."
    return 0
}
