import java.io.*;
import java.util.HashMap;
import java.util.Scanner;

public class Main {
    
    private static final HashMap<String, String> dictionary = new HashMap<>();
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Пожалуйста, передайте путь к файлу в качестве аргумента командной строки.");
            return;
        }

        String filename = args[0];
        loadDictionaryFromFile(filename);

        while (true) {
            showMenu();
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    searchWord();
                    break;
                case 2:
                    exitProgram();
                    return;
                default:
                    System.out.println("Неверный выбор. Пожалуйста, попробуйте снова.");
            }
        }
    }

    private static void loadDictionaryFromFile(String filename) {
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length == 2) {
                    String word = parts[0].trim();
                    String meaning = parts[1].trim();
                    dictionary.put(word, meaning);
                }
            }
        } catch (IOException e) {
            System.out.println("Ошибка при чтении файла: " + e.getMessage());
        }
    }

    private static void showMenu() {
        System.out.println("Меню:");
        System.out.println("1. Найти слово");
        System.out.println("2. Выход");
        System.out.print("Введите ваш выбор: ");
    }

    private static void searchWord() {
        System.out.print("Введите слово для поиска: ");
        String word = scanner.nextLine().trim();

        String meaning = dictionary.get(word);
        if (meaning != null) {
            System.out.println("Значение слова '" + word + "': " + meaning);
        } else {
            System.out.println("Слово не найдено в словаре.");
        }
    }

    private static void exitProgram() {
        System.out.println("Выход из программы...");
        scanner.close();
    }
}
