#!/bin/bash

source /usr/bin/server-monitor-tool
source ./tests/unit/test_interface.sh

echo -e "${CYAN}Running tests for check_duplicates...${RESET}"

run_test "Test with unique arguments" \
    0 \
    "" \
    "check_duplicates one two three"

run_test "Test with duplicate arguments" \
    1 \
    "Ошибка: аргумент 'two' уже был использован." \
    "check_duplicates one two two"

run_test "Test with no arguments" \
    0 \
    "" \
    "check_duplicates"

run_test "Test with mixed duplicates" \
    1 \
    "Ошибка: аргумент 'one' уже был использован." \
    "check_duplicates one two one"

print_summary