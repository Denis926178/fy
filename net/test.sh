#!/bin/bash

docker network create --subnet=192.168.100.0/24 test_network

create_container() {
    local container_name=$1
    local ip_address=$2

    docker run -d --name "$container_name" --network test_network --ip "$ip_address" -h "$container_name" \
        -e TZ=Europe/Moscow -e DEBIAN_FRONTEND=noninteractive \
        ubuntu:latest bash -c "
            apt update && \
            apt install -y openssh-server iproute2 && \
            mkdir -p /var/run/sshd && \
            echo 'root:password' | chpasswd && \
            sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
            /usr/sbin/sshd -D"
}

# create_container "test_server1" "192.168.100.10"
# create_container "test_server2" "192.168.100.11"
create_container "test_server4" "192.168.100.13"

echo "Создано три тестовых сервера в подсети 192.168.100.0/24."
echo "IP-адреса: 192.168.100.10, 192.168.100.11, 192.168.100.12"
