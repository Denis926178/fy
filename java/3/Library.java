import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

class Book {
    private int id;
    private String name;
    private String author;
    private String edition;
    private String publisher;
    private int yearOfPublication;
    private String category;

    public Book(int id, String name, String author, String edition, String publisher, int yearOfPublication, String category) {
        this.id = id;
        this.name = name;
        this.author = author;
        this.edition = edition;
        this.publisher = publisher;
        this.yearOfPublication = yearOfPublication;
        this.category = category;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public String getAuthor() { return author; }
    public String getEdition() { return edition; }
    public String getPublisher() { return publisher; }
    public int getYearOfPublication() { return yearOfPublication; }
    public String getCategory() { return category; }

    @Override
    public String toString() {
        return "Book{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", author='" + author + '\'' +
                ", edition='" + edition + '\'' +
                ", publisher='" + publisher + '\'' +
                ", yearOfPublication=" + yearOfPublication +
                ", category='" + category + '\'' +
                '}';
    }
}

class Library {
    private static Library instance;
    private Map<Integer, Book> books;
    private Map<Integer, Integer> availableCopies; 
    private Map<Integer, Reader> readers;

    private Library() {
        books = new HashMap<>();
        availableCopies = new HashMap<>();
        readers = new HashMap<>();
    }

    public static Library getInstance() {
        if (instance == null) {
            instance = new Library();
        }
        return instance;
    }

    public void addBook(Book book, int copies) {
        books.putIfAbsent(book.getId(), book);
        availableCopies.put(book.getId(), availableCopies.getOrDefault(book.getId(), 0) + copies);
    }

    public void showBooks() {
        for (Book book : books.values()) {
            int copies = availableCopies.getOrDefault(book.getId(), 0);
            System.out.println(book + ", availableCopies=" + copies);
        }
    }

    public Book findBookById(int id) {
        if (!books.containsKey(id))
            System.out.println("Книга с ID " + id + " не найдена.");

        return books.get(id);
    }

    public Reader findReaderById(int id) {
        if (!readers.containsKey(id))
            System.out.println("Читатель с ID " + id + " не найден.");

        return readers.get(id);
    }

    public boolean borrowBook(int bookId, Reader reader) {
        if (reader == null) {
            System.out.println("Читатель с ID " + reader.getId() + " не найден.");
            return false;
        }

        int copies = availableCopies.getOrDefault(bookId, 0);
        if (copies > 0) {
            availableCopies.put(bookId, copies - 1);
            reader.addBook(books.get(bookId));
            return true;
        }
    
        System.out.println("Книга с ID " + bookId + " недоступна для выдачи.");
        return false;
    }

    public void returnBook(int bookId, int readerId) {
        Reader reader = readers.get(readerId);
        if (reader == null) {
            System.out.println("Читатель с ID " + readerId + " не найден.");
            return;
        }

        if (reader.getBorrowedBooks().removeIf(book -> book.getId() == bookId)) {
            availableCopies.put(bookId, availableCopies.getOrDefault(bookId, 0) + 1);
        } else {
            System.out.println("Книга с ID " + bookId + " не найдена у читателя с ID " + readerId + ".");
        }
    }

    public void removeBook(int bookId) {
        if (books.containsKey(bookId)) {
            books.remove(bookId);
            availableCopies.remove(bookId);
            System.out.println("Книга с ID " + bookId + " успешно удалена из библиотеки.");
        } else {
            System.out.println("Книга с ID " + bookId + " не найдена в библиотеке.");
        }
    }

    public int getAvailableCopies(int bookId) {
        return availableCopies.getOrDefault(bookId, 0);
    }

    public boolean isReaderRegistered(int readerId) {
        return readers.containsKey(readerId);
    }

    public void registerReader(Reader reader) {
        if (isReaderRegistered(reader.getId())) {
            System.out.println("Читатель уже зарегистрирован: " + reader);
        } else {
            readers.put(reader.getId(), reader);
            System.out.println("Читатель успешно зарегистрирован: " + reader);
        }
    }

    public void showRegisteredReaders() {
        if (readers.isEmpty()) {
            System.out.println("Нет зарегистрированных читателей.");
        } else {
            System.out.println("Зарегистрированные читатели:");
            for (Reader reader : readers.values()) {
                System.out.println(reader);
            }
        }
    }

    public void showBorrowedBooksForReader(int id) {
        Reader reader = findReaderById(id);

        System.out.println("Книги пользователя с id: " + id);
        for (Book book : reader.getBorrowedBooks())
            System.out.println(" - " + book);
    }

    public void printLibraryInfo() {
        System.out.println("Информация о библиотеке:");

        System.out.println("\nВсе книги в библиотеке:");
        for (Map.Entry<Integer, Book> entry : books.entrySet()) {
            Book book = entry.getValue();
            Integer bookId = entry.getKey();
            Integer copies = availableCopies.getOrDefault(bookId, 0);
            System.out.println("Книга: " + book.getName() + ", Автор: " + book.getAuthor() + ", Количество экземпляров: " + copies);
        }

        System.out.println("\nЧитатели и их книги:");
        for (Map.Entry<Integer, Reader> entry : readers.entrySet()) {
            Reader reader = entry.getValue();
            System.out.println("Читатель: " + reader.getId());
            if (reader.getBorrowedBooks() != null && !reader.getBorrowedBooks().isEmpty()) {
                System.out.println("Взятые книги:");
                for (Book borrowedBook : reader.getBorrowedBooks()) {
                    System.out.println(" - " + borrowedBook.getName() + " (" + borrowedBook.getAuthor() + ")");
                }
            } else {
                System.out.println("Нет взятых книг.");
            }
            System.out.println();
        }
    }

    public void showBooksReaders() {
        for (Reader reader : readers.values()) {
            showBorrowedBooksForReader(reader.getId());
        }
    }

    public Reader registerReader() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите идентификатор читателя: ");
        int id = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Введите имя: ");
        String firstName = scanner.nextLine();

        System.out.print("Введите фамилию: ");
        String lastName = scanner.nextLine();

        System.out.print("Введите отчество: ");
        String middleName = scanner.nextLine();

        System.out.print("Введите адрес: ");
        String address = scanner.nextLine();

        Reader newReader = new Reader(id, firstName, lastName, middleName, address);
        registerReader(newReader);
        return newReader;
    }
}
