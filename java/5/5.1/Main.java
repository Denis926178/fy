import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Main {

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Использование: java WordProcessor <входной файл> <выходной файл>");
            return;
        }

        String inputFileName = args[0];
        String outputFileName = args[1];
        StringBuilder text = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new FileReader(inputFileName))) {
            String line;
            while ((line = reader.readLine()) != null) {
                text.append(line).append("\n");
            }
        } catch (IOException e) {
            System.out.println("Ошибка при чтении файла: " + e.getMessage());
            return;
        }

        String cleanedText = text.toString().replaceAll("[^a-zA-Zа-яА-Я0-9 ]", "").toLowerCase();
        String[] words = cleanedText.split("\\s+");

        Set<String> uniqueWords = new TreeSet<>(Arrays.asList(words));

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName))) {
            for (String word : uniqueWords)
                writer.write(word + "\n");

            System.out.println("Результат успешно сохранен в файл: " + outputFileName);
        } catch (IOException e) {
            System.out.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }
}
