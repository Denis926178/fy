#!/bin/bash

# Имя проекта
PROJECT_NAME="server-monitor"

# Настройка пользователя от лица которого будет подключение по ssh
SERVER_USER="root"

# Таймаунт проверки новых серверов в подсети
MONITOR_SERVERS_TIME="5"

# Подсеть, с которой работает скрипт
DEFAULT_NET="192.168.100.0/24"

# Сбор информации о процессоре
NEED_COLLECT_CPU_INFO="yes"

# Сбор информации об использовании оперативной памяти
NEED_COLLECT_RAM_INFO="yes"

# Сбор информации и подключениях/портах сервера
NEED_COLLECT_ACTIVE_CONNECTIONS_INFO="yes"

# Сбор информации о запущенных процессах на сервере
NEED_COLLECT_ACTIVE_PROCESSES_INFO="yes"

# Сбор информации об операционной системе сервера
NEED_COLLECT_VERSION_OS_INFO="yes"


# Оповещение при достижении температуры (Градусы Цельсия)
CPU_MAX_TEMPERATURE="80"

# Оповещение при малом количестве свободного пространства на диске (Проценты)
LOW_DISK_SPACE="10"

# Таймер для обнаружения новых серверов в подсети
TIMER_MONITOR_NEW_SERVERS=10

# Таймер для проверки температуры процессора
TIMER_MONITOR_CPU_TEMPERATURE=60

# Таймер для проверки свободного места на диске
TIMER_MONITOR_DISK_SPACE=3600


# Файл база данных - тут хранятся данные о том, ip серверов и пароли к ним
PASSWORD_FILE="/etc/$PROJECT_NAME/password.conf"

# Файл база данных - тут хранятся данные о всех хостах, с которыми работает скрипт
MONITOR_HOSTS_FILE="/etc/$PROJECT_NAME/monitor-hosts.conf"
