#!/bin/bash

TEMP_DIR="/tmp/server-monitor"

CONFIG_FILE="$LIB_DIR_MONITOR_SERVER/configuration.sh"
BACKUP_FILE="$TEMP_DIR/configuration_backup.sh"

backup_config() {
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "Конфигурация сохранена в $BACKUP_FILE"
}

restore_config() {
    if [[ -f "$BACKUP_FILE" ]]; then
        cp "$BACKUP_FILE" "$CONFIG_FILE"
        echo "Конфигурация восстановлена из $BACKUP_FILE"
        rm $BACKUP_FILE
    else
        echo "Резервная копия конфигурации не найдена."
    fi
}

create_container() {
    local container_name=$1
    local ip_address=$2
    local password=$3

    current_user="${SUDO_USER:-$USER}"

    docker run -d \
        --name "$container_name" \
        --network server-monitor-network \
        --ip "$ip_address" \
        -h "$container_name" \
        -e TZ=Europe/Moscow \
        -e DEBIAN_FRONTEND=noninteractive \
        ubuntu:latest bash -c "
            apt update && \
            apt install -y openssh-server iproute2 && \
            mkdir -p /var/run/sshd && \
            useradd -m -s /bin/bash $current_user && \
            echo '$current_user:$password' | chpasswd && \
            echo '$current_user ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
            echo 'root:$password' | chpasswd && \
            sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
            sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
            /usr/sbin/sshd -D"
}

start_containers() {
    backup_config

    $LIB_DIR_MONITOR_SERVER/settings.sh --MONITOR_HOSTS_FILE="$TEMP_DIR/monitor-hosts.conf"
    $LIB_DIR_MONITOR_SERVER/settings.sh --PASSWORD_FILE="$TEMP_DIR/password.conf"
    $LIB_DIR_MONITOR_SERVER/settings.sh --DEFAULT_NET="192.168.100.0/24"

    mkdir -pv $TEMP_DIR

    source $LIB_DIR_MONITOR_SERVER/configuration.sh
    touch $MONITOR_HOSTS_FILE
    touch $PASSWORD_FILE

    if ! docker network inspect server-monitor-network &>/dev/null; then
        docker network create \
            --subnet=$DEFAULT_NET \
            server-monitor-network
        echo "Создана сеть Docker: server-monitor-network ($DEFAULT_NET)"
    fi

    > "$MONITOR_HOSTS_FILE"

    echo "Запуск контейнеров..."

    for i in {1..5}; do
        if docker ps -a --filter "name=server-$i" --format '{{.Names}}' | grep -q "server-$i"; then
            echo "Контейнер server-$i уже существует, удаляю..."
            docker rm -f "server-$i"
        fi

        ip="192.168.100.$((100 + i))"
        container_name="server-$i"
        password="password$i"

        create_container "server-$i" "$ip" "$password"

        if [[ $? -eq 0 ]]; then
            echo "$ip" >> "$MONITOR_HOSTS_FILE"
            echo "$ip : $password" >> "$PASSWORD_FILE"
            echo "Контейнер $container_name запущен с IP: $ip"
        else
            echo "Ошибка при запуске контейнера $container_name"
        fi
    done

    echo "Список активных хостов записан в $MONITOR_HOSTS_FILE"
}

stop_containers() {
    source $LIB_DIR_MONITOR_SERVER/configuration.sh

    # Удаляем временную директорию, где хранятся конфигурационные файлы
    rm -rf $TEMP_DIR

    # Восстанавливаем конфигурацию из резервной копии
    restore_config

    echo "Остановка контейнеров и удаление конфигурации..."

    # Останавливаем и удаляем все контейнеры с именами, начинающимися с "server-"
    docker ps -a --filter "name=server-" --format "{{.ID}}" | xargs -r docker rm -f &>/dev/null

    # Удаляем сеть Docker, если она существует
    docker network inspect server-monitor-network &>/dev/null && docker network rm server-monitor-network &>/dev/null || true

    # Удаляем все образцы и промежуточные образы, связанные с тестами
    docker image prune -af &>/dev/null

    echo "Все контейнеры остановлены, сеть и ненужные образы удалены."
}

case "$1" in
    --start)
        start_containers
        ;;
    --stop)
        stop_containers
        ;;
    *)
        echo "Использование: $0 --start|--stop"
        exit 1
        ;;
esac
