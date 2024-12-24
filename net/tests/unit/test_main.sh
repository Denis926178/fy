#!/bin/bash

source /usr/bin/server-monitor-tool
source ./tests/unit/test_interface.sh

run_call() {
    echo "run_call called with args: $*"
    return 0
}

run_setting() {
    echo "run_setting called with args: $*"
    return 0
}

run_info() {
    echo "run_info called with args: $*"
    return 0
}

run_add_monitor() {
    echo "run_add_monitor called with args: $*"
    return 0
}

run_remove_monitor() {
    echo "run_remove_monitor called with args: $*"
    return 0
}

run_clear_monitor() {
    echo "run_clear_monitor called with args: $*"
    return 0
}

run_daemon() {
    echo "run_daemon called with args: $*"
    return 0
}

print_help() {
    echo "print_help called"
    return 0
}

TESTS_PASSED=0
TESTS_FAILED=0

run_test "Test: check_duplicates failure" \
    1 \
    "Ошибка: аргумент 'two' уже был использован." \
    "main one two two"

run_test "Test: check call option" \
    0 \
    "run_call called with args: ..." \
    "main call ..."

run_test "Test: check setting option" \
    0 \
    "run_setting called with args: ..." \
    "main setting ..."

run_test "Test: check info option" \
    0 \
    "run_info called with args: ..." \
    "main info ..."

run_test "Test: check add-monitor option" \
    0 \
    "run_add_monitor called with args: ..." \
    "main add-monitor ..."

run_test "Test: check remove-monitor option" \
    0 \
    "run_remove_monitor called with args: ..." \
    "main remove-monitor ..."

run_test "Test: check clear-monitor option" \
    0 \
    "run_clear_monitor called with args: ..." \
    "main clear-monitor ..."

run_test "Test: check daemon option" \
    0 \
    "run_daemon called with args: ..." \
    "main daemon ..."

print_summary
