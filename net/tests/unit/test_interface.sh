#!/bin/bash

# Цвета для вывода
RED="\033[31m"
GREEN="\033[32m"
CYAN="\033[36m"
YELLOW="\033[33m"
RESET="\033[0m"

# Счётчики тестов
TESTS_PASSED=0
TESTS_FAILED=0

# Логика выполнения теста
run_test() {
    local test_name="$1"
    local expected_exit_code="$2"
    local expected_output="$3"
    local actual_output
    local actual_exit_code

    # Выполняем тест, получаем вывод и код возврата
    actual_output=$(eval "${@:4}" 2>&1)
    actual_exit_code=$?

    # Сравниваем код возврата и вывод
    if [[ "$actual_exit_code" -eq "$expected_exit_code" && "$actual_output" == "$expected_output" ]]; then
        echo -e "${GREEN}[PASS]${RESET} $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}[FAIL]${RESET} $test_name"
        echo -e "${YELLOW}  Expected Exit Code: ${CYAN}$expected_exit_code${RESET}, Got: ${CYAN}$actual_exit_code${RESET}"
        echo -e "${YELLOW}  Expected Output: ${CYAN}$expected_output${RESET}"
        echo -e "${YELLOW}  Got Output:      ${CYAN}$actual_output${RESET}"
        ((TESTS_FAILED++))
    fi
}

# Завершение тестирования
print_summary() {
    echo -e "\n${CYAN}--- Test Summary ---${RESET}"
    echo -e "${GREEN}Passed: $TESTS_PASSED${RESET}"
    echo -e "${RED}Failed: $TESTS_FAILED${RESET}"
    if [[ "$TESTS_FAILED" -eq 0 ]]; then
        echo -e "${GREEN}All tests passed!${RESET}"
    else
        echo -e "${RED}Some tests failed. Please review the output above.${RESET}"
    fi
}
