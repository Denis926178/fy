#!/bin/bash

source $LIB_DIR_MONITOR_SERVER/password
source ./tests/unit/test_interface.sh

PASSWORD_FILE="./test_password.sh"
echo "" > "$PASSWORD_FILE"

run_test "Add record success" \
         0 \
         "Запись для хоста 'server1' добавлена." \
         add_record "server1" "mypassword1"

run_test "Add record failed" \
         1 \
         "Ошибка: запись для хоста 'server1' уже существует." \
         add_record "server1" "newpassword1"

run_test "Get password success" \
         0 \
         "mypassword1" \
         get_password "server1"

run_test "Get password failed" \
         1 \
         "Ошибка: запись для хоста 'server2' не найдена." \
         get_password "server2"

run_test "Update password success" \
         0 \
         "Пароль для хоста 'server1' обновлен." \
         update_password "server1" "newpassword1"

run_test "Update password failed" \
         1 \
         "Ошибка: запись для хоста 'server2' не найдена." \
         update_password "server2" "newpassword1"

run_test "Delete record success" \
         0 \
         "Запись для хоста 'server1' удалена." \
         delete_record "server1"

run_test "Delete record failed" \
         1 \
         "Ошибка: запись для хоста 'server1' не найдена." \
         delete_record "server1"

print_summary
rm $PASSWORD_FILE
