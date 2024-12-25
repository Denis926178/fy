SHELL := /bin/bash

PROJECT_NAME=server-monitor

INSTALL_DIR=/usr/bin

LIB_DIR=/usr/lib/$(PROJECT_NAME)
SYSTEMD_DIR=/etc/systemd/system
TEST_DIR=tests

UTIL_FILE=src/core/$(PROJECT_NAME)-tool.sh
DAEMON_FILE=src/core/$(PROJECT_NAME)d.sh
SETTINGS_FILE=src/core/$(PROJECT_NAME)-settings.sh
SYSTEMD_FILE=systemd/$(PROJECT_NAME).service

HELPER_FILES=\
	src/daemon/server-monitor.sh \
	src/lib/call.sh \
	src/lib/configuration.sh \
	src/lib/info.sh \
	src/lib/password.sh \
	src/lib/server-control.sh

.PHONY: all install uninstall install_util install_daemon install_lib install_systemd set-env-variable

COLOR_RESET=\033[0m
COLOR_GREEN=\033[0;32m
COLOR_YELLOW=\033[0;33m
COLOR_BLUE=\033[0;34m
COLOR_RED=\033[0;31m

all: install set-env-variable unit_test enable-service

install: install_util install_settings install_daemon install_lib install_systemd

install_util:
	@echo -e "$(COLOR_GREEN)Установка основной утилиты в $(INSTALL_DIR):$(COLOR_RESET)"
	@base_name=$$(basename "$(SETTINGS_FILE)" | sed 's/\(.*\)\..*/\1/') && \
	echo -e "  $(COLOR_BLUE)$(SETTINGS_FILE) -> $(INSTALL_DIR)/$$base_name$(COLOR_RESET)" && \
	install -Dm755 "$(SETTINGS_FILE)" "$(INSTALL_DIR)/$$base_name"

install_settings:
	@echo -e "$(COLOR_GREEN)Установка утилиты для настроек в $(INSTALL_DIR):$(COLOR_RESET)"
	@base_name=$$(basename "$(UTIL_FILE)" | sed 's/\(.*\)\..*/\1/') && \
	echo -e "  $(COLOR_BLUE)$(UTIL_FILE) -> $(INSTALL_DIR)/$$base_name$(COLOR_RESET)" && \
	install -Dm755 "$(UTIL_FILE)" "$(INSTALL_DIR)/$$base_name"

install_daemon:
	@echo -e "$(COLOR_GREEN)Установка основного демона в $(INSTALL_DIR):$(COLOR_RESET)"
	@base_name=$$(basename "$(DAEMON_FILE)" | sed 's/\(.*\)\..*/\1/') && \
	echo -e "  $(COLOR_BLUE)$(DAEMON_FILE) -> $(INSTALL_DIR)/$$base_name$(COLOR_RESET)" && \
	install -Dm755 "$(DAEMON_FILE)" "$(INSTALL_DIR)/$$base_name"

install_lib:
	@echo -e "$(COLOR_GREEN)Установка вспомогательных файлов в $(LIB_DIR):$(COLOR_RESET)"

	@install -d $(LIB_DIR)
	@for file in $(HELPER_FILES); do \
	    base_name=$$(basename "$$file" | sed 's/\(.*\)\..*/\1/'); \
	    echo -e "  $(COLOR_BLUE)$$file -> $(LIB_DIR)/$$base_name$(COLOR_RESET)"; \
	    install -Dm755 "$$file" "$(LIB_DIR)/$$base_name"; \
	done

install_systemd:
	@echo -e "$(COLOR_GREEN)Установка systemd файла в $(SYSTEMD_DIR):$(COLOR_RESET)"
	@echo -e "  $(COLOR_BLUE)$(SYSTEMD_FILE) -> $(SYSTEMD_DIR)/$(notdir $(SYSTEMD_FILE))$(COLOR_RESET)"
	@install -Dm644 $(SYSTEMD_FILE) $(SYSTEMD_DIR)/$(notdir $(SYSTEMD_FILE))

uninstall:
	@echo -e "$(COLOR_RED)Удаление основной утилиты из $(INSTALL_DIR):$(COLOR_RESET)"
	@echo -e "  $(COLOR_BLUE)$(INSTALL_DIR)/$(basename $(UTIL_FILE))$(COLOR_RESET)"
	@rm -f $(INSTALL_DIR)/$(basename $(UTIL_FILE))

	@echo -e "$(COLOR_RED)Удаление основного демона из $(INSTALL_DIR):$(COLOR_RESET)"
	@echo -e "  $(COLOR_BLUE)$(INSTALL_DIR)/$(basename $(DAEMON_FILE))$(COLOR_RESET)"
	@rm -f $(INSTALL_DIR)/$(basename $(DAEMON_FILE))

	@echo -e "$(COLOR_RED)Удаление вспомогательных файлов из $(LIB_DIR):$(COLOR_RESET)"

	@for file in $(HELPER_FILES); do \
	    base_name=$$(basename "$$file" | sed 's/\(.*\)\..*/\1/'); \
	    echo -e "  $(COLOR_BLUE)$(LIB_DIR)/$$base_name$(COLOR_RESET)"; \
	    rm "$(LIB_DIR)/$$base_name"; \
	done

	@echo -e "$(COLOR_RED)Удаление systemd файла из $(SYSTEMD_DIR):$(COLOR_RESET)"
	@echo -e "  $(COLOR_BLUE)$(SYSTEMD_DIR)/$(basename $(SYSTEMD_FILE))$(COLOR_RESET)"
	@rm -f $(SYSTEMD_DIR)/$(basename $(SYSTEMD_FILE).service)

unit_test:
	@echo "Запуск юнит-тестов"
	@for test_file in $(TEST_DIR)/unit/*.sh; do \
	    echo "Запуск $$test_file"; \
	    bash $$test_file || exit 1; \
	done

# [[deprecated]]
func_test:
	@echo "Запуск функциональных тестов"
	echo "Запуск $(TEST_DIR)/func/test.sh"; \
	bash $(TEST_DIR)/func/test.sh --start || exit 1; \
	echo "Остановка $(TEST_DIR)/func/test.sh"; \
	bash $(TEST_DIR)/func/test.sh --stop|| exit 1; \
	@echo "Все тесты успешно завершены"

enable-service:
	@echo "Включение и запуск службы server-monitor.service"
	@systemctl daemon-reload
	@systemctl enable server-monitor.service
	@systemctl start server-monitor.service

disable-service:
	@echo "Отключение и остановка службы server-monitor.service"
	@systemctl stop server-monitor.service
	@systemctl disable server-monitor.service

set-env-variable:
	@USER=$(whoami) \
	&& echo -e "$(COLOR_GREEN)LIB_DIR_MONITOR_SERVER=\"/usr/lib/server-monitor\":$(COLOR_RESET)" \
	&& grep -q 'LIB_DIR_MONITOR_SERVER' /home/$(SUDO_USER)/.bashrc || echo 'export LIB_DIR_MONITOR_SERVER="/usr/lib/server-monitor"' >> /home/$(SUDO_USER)/.bashrc \
	&& grep -q 'LIB_DIR_MONITOR_SERVER' /root/.bashrc || echo 'export LIB_DIR_MONITOR_SERVER="/usr/lib/server-monitor"' | sudo tee -a /root/.bashrc >/dev/null \
	&& source /home/$(SUDO_USER)/.bashrc \
	&& sudo bash -c 'source /root/.bashrc' \
	&& echo -e "$(COLOR_BLUE)  Переменная окружения LIB_DIR_MONITOR_SERVER добавлена в ~/.bashrc для $(SUDO_USER) и /root/.bashrc для пользователя root:$(COLOR_RESET)"
