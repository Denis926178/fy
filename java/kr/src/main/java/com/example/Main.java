package com.example;

import java.time.LocalDate;
import java.util.Scanner;
import java.util.InputMismatchException;
import java.time.format.DateTimeParseException;

public class Main {
    public static final Scanner scanner = new Scanner(System.in);
    public static final EmployeeService employeeService = new EmployeeService();

    public static void main(String[] args) {
        while (true) {
            printMenu();
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1 -> addEmployee();
                case 2 -> findById();
                case 3 -> findByName();
                case 4 -> findByBirthDay();
                case 5 -> updateInformationAboutEmployee();
                case 6 -> deleteEmployee();
                case 7 -> countSalary();
                case 0 -> {
                    System.out.println("Работа завершена");
                    return;
                }
                default -> System.out.println("Неверный выбор.");
            }
        }
    }

    static private Double readSalary() {
        double salary = 0;

        while (true) {
            System.out.print("Введите зарплату: ");
            try {
                salary = scanner.nextDouble();
                if (salary < 0)
                    System.out.println("Зарплата не может быть отрицательной. Попробуйте снова.");
                else
                    return salary;
            } catch (InputMismatchException e) {
                System.out.println("Ошибка ввода. Пожалуйста, введите правильное числовое значение.");
                scanner.nextLine();
            }
        }
    }

    static private LocalDate readBirthDay() {
        LocalDate birthDay = null;

        while (birthDay == null) {
            System.out.print("Введите дату рождения (yyyy-MM-dd): ");
            String input = scanner.nextLine();

            try {
                birthDay = LocalDate.parse(input);
                System.out.println("Дата рождения успешно введена: " + birthDay);
            } catch (DateTimeParseException e) {
                System.out.println("Некорректный формат даты. Пожалуйста, введите дату в формате yyyy-MM-dd.");
            }
        }

        return birthDay;
    }

    static private Long readId() {
        Long id;

        while (true) {
            System.out.print("Введите ID: ");
            try {
                id = scanner.nextLong();
                return id;
            } catch (InputMismatchException e) {
                System.out.println("Ошибка ввода. Пожалуйста, введите правильное числовое значение.");
                scanner.nextLine();
            }
        }
    }

    static private void addEmployee() {
        System.out.print("Введите имя: ");
        String firstName = scanner.nextLine();

        System.out.print("Введите фамилию: ");
        String lastName = scanner.nextLine();
    
        System.out.print("Введите место рождения: ");
        String birthPlace = scanner.nextLine();

        LocalDate birthDate = readBirthDay();
        Double salary = readSalary();

        employeeService.addEmployee(
            new Employee(
                firstName,
                lastName,
                birthDate,
                birthPlace,
                salary
            )
        );
    }

    static private void printMenu() {
        System.out.println("\nМеню:");
        System.out.println("1. Добавить сотрудника");
        System.out.println("2. Найти сотрудника по ID");
        System.out.println("3. Найти сотрудника по имени");
        System.out.println("4. Найти сотрудника по дате рождения");
        System.out.println("5. Обновить информацию о сотруднике");
        System.out.println("6. Удалить сотрудника");
        System.out.println("7. Рассчитать общую сумму зарплат");
        System.out.println("0. Выйти");
        System.out.print("    Введите оппцию: ");
    }

    static private void findById() {
        Employee employee = employeeService.findEmployeeById(readId());
        System.out.println(employee != null ? employee : "Сотрудник не найден.");
    }

    static private void findByName() {
        System.out.print("Введите имя: ");
        String name = scanner.nextLine();
        employeeService.findEmployeesByName(name).forEach(System.out::println);
    }

    static private void findByBirthDay() {
        employeeService.findEmployeesByBirthDate(readBirthDay()).forEach(System.out::println);
    }

    static private void updateInformationAboutEmployee() {
        Employee employee = employeeService.findEmployeeById(readId());
        if (employee == null) {
            System.out.println("Сотрудник не найден.");
            return;
        }

        System.out.print("Введите новое имя: ");
        employee.setFirstName(scanner.nextLine());
        System.out.print("Введите новую фамилию: ");
        employee.setLastName(scanner.nextLine());
        System.out.print("Введите новую зарплату: ");
        employee.setSalary(readSalary());
        employeeService.updateEmployee(employee);
    }

    static private void deleteEmployee() {
        employeeService.deleteEmployee(readId());
    }

    static private void countSalary() {
        System.out.println("Общая сумма зарплат: " + employeeService.calculateTotalSalary());
    }
}
