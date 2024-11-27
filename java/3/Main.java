import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;

class GlobalScanner {
    public static final Scanner SCANNER = new Scanner(System.in);
}

public class Main {
    public static void main(String[] args) {
        boolean isRunning = true;

        while (isRunning) {
            ShowMenu.showStartMenu();

            String input = GlobalScanner.SCANNER.nextLine().trim();

            switch (input) {
                case "0" -> {
                    System.out.println("Завершение программы.");
                    isRunning = false; // Завершаем цикл вместо System.exit(0)
                }
                case "1" -> runActivePerson(new Manager());
                case "2" -> runActivePerson(new Librarian());
                case "3" -> runActivePerson(new Reader());
                default -> System.out.println("Некорректный ввод. Пожалуйста, введите число от 0 до 3.");
            }
        }

        GlobalScanner.SCANNER.close();
    }

    private static void runActivePerson(Person person) {
        person.run();
    }
}

interface IPerson {
    void run();
}

abstract class Person implements IPerson {
    protected int id = -1;
    protected String firstName;
    protected String lastName;
    protected String middleName;
    protected String address;

    public int getId() { return id; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getMiddleName() { return middleName; }
    public String getAddress() { return address; }

    public void setId(int id) { this.id = id; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public void setMiddleName(String middleName) { this.middleName = middleName; }
    public void setAddress(String address) { this.address = address; }

    @Override
    public String toString() {
        return "ID: " + id +
               ", Имя: " + firstName +
               ", Фамилия: " + lastName +
               ", Отчество: " + middleName +
               ", Адрес: " + address;
    }
}

class Manager extends Person {
    @Override
    public void run() {
        while (true) {
            ShowMenu.showManagerMenu();

            String input = GlobalScanner.SCANNER.nextLine().trim();

            switch (input) {
                case "1" -> addBookAction();
                case "2" -> removeBookAction();
                case "3" -> showStatistics();
                case "0" -> {
                    System.out.println("Зарешение работы менеджера.");
                    return;
                }
                default -> {
                    System.out.println("Ошибка: введите число от 0 до 3.");
                }
            }
        }
    }

    private void addBookAction() {
        System.out.println("Введите ID книги:");
        String idInput = GlobalScanner.SCANNER.nextLine().trim();

        if (!isNumeric(idInput)) {
            System.out.println("Ошибка: ID книги должен быть числом.");
            return;
        }

        int id = Integer.parseInt(idInput);

        System.out.println("Введите название книги:");
        String name = GlobalScanner.SCANNER.nextLine().trim();

        System.out.println("Введите автора книги:");
        String author = GlobalScanner.SCANNER.nextLine().trim();

        System.out.println("Введите издание книги:");
        String edition = GlobalScanner.SCANNER.nextLine().trim();

        System.out.println("Введите издателя книги:");
        String publisher = GlobalScanner.SCANNER.nextLine().trim();

        System.out.println("Введите год издания книги:");
    
        String yearInput = GlobalScanner.SCANNER.nextLine().trim();
        if (!isNumeric(yearInput)) {
            System.out.println("Ошибка: Год издания должен быть числом.");
            return;
        }

        int year = Integer.parseInt(yearInput);

        System.out.println("Введите категорию книги:");
        String category = GlobalScanner.SCANNER.nextLine().trim();

        System.out.println("Введите количество экземпляров:");
        String copiesInput = GlobalScanner.SCANNER.nextLine().trim();

        if (!isNumeric(copiesInput)) {
            System.out.println("Ошибка: Количество экземпляров должно быть числом.");
            return;
        }
    
        int copies = Integer.parseInt(copiesInput);

        Book book = new Book(id, name, author, edition, publisher, year, category);
        Library.getInstance().addBook(book, copies);
        System.out.println("Книга успешно добавлена.");
    }

    private void removeBookAction() {
        System.out.println("Введите ID книги для удаления:");
        String idInput = GlobalScanner.SCANNER.nextLine().trim();

        if (!isNumeric(idInput)) {
            System.out.println("Ошибка: ID книги должен быть числом.");
            return;
        }
    
        int id = Integer.parseInt(idInput);
        Library.getInstance().removeBook(id);
    }

    private void showStatistics() {
        System.out.println("Статистика библиотеки:");
        Library.getInstance().printLibraryInfo();
    }

    private boolean isNumeric(String str) {
        return str != null && str.matches("\\d+");
    }
}

class Librarian extends Person {
    public void run() {
        Library library = Library.getInstance();

        while (true) {
            ShowMenu.showLibrarianMenu();

            String input = GlobalScanner.SCANNER.nextLine().trim();

            switch (input) {
                case "1" -> searchBook();
                case "2" -> giveBook();
                case "3" -> returnBook();
                case "0" -> {
                    System.out.println("Работа библиотекаря завершена.");
                    return;
                }
                default -> {
                    System.out.println("Ошибка: введите число от 0 до 2.");
                }
            }
        }
    }

    public void giveBook() {
        System.out.print("Введите ID книги для поиска: ");
        int bookId = GlobalScanner.SCANNER.nextInt();
        GlobalScanner.SCANNER.nextLine();

        Book book = Library.getInstance().findBookById(bookId);

        if (book == null)
            return;

        if (Library.getInstance().getAvailableCopies(bookId) <= 0) {
            System.out.println("Нет доступных копий книги с ID " + bookId);
            return;
        }

        System.out.print("Введите ID читателя для выдачи книги: ");
        int readerId = GlobalScanner.SCANNER.nextInt();
        GlobalScanner.SCANNER.nextLine();

        if (!Library.getInstance().isReaderRegistered(readerId)) {
            System.out.println("Читатель с ID " + readerId + " не зарегистрирован.");
            return;
        }

        Reader reader = Library.getInstance().findReaderById(readerId);
        Library.getInstance().borrowBook(bookId, reader);
        System.out.println("Книга '" + book.getName() + "' успешно выдана читателю с ID " + readerId);
    }

    public void returnBook() {
        System.out.print("Введите ID книги для возврата: ");
        int bookId = GlobalScanner.SCANNER.nextInt();
        GlobalScanner.SCANNER.nextLine();

        Book book = Library.getInstance().findBookById(bookId);

        if (book == null)
            return;

        System.out.print("Введите ID читателя для возврата книги: ");
        int readerId = GlobalScanner.SCANNER.nextInt();
        GlobalScanner.SCANNER.nextLine();

        if (!Library.getInstance().isReaderRegistered(readerId)) {
            System.out.println("Читатель с ID " + readerId + " не зарегистрирован.");
            return;
        }

        Reader reader = Library.getInstance().findReaderById(readerId);
        if (!reader.getBorrowedBooks().contains(book)) {
            System.out.println("Читатель с ID " + readerId + " не имеет книги с ID " + bookId);
            return;
        }
    
        reader.returnBook(book);
        Library.getInstance().returnBook(bookId, 1);
        System.out.println("Книга '" + book.getName() + "' успешно возвращена от читателя с ID " + readerId);
    }

    public void searchBook() {
        System.out.print("Введите ID книги для поиска: ");
        int bookId = GlobalScanner.SCANNER.nextInt();
        GlobalScanner.SCANNER.nextLine();

        Book book = Library.getInstance().findBookById(bookId);
        
        if (book != null) {
            int availableCopies = Library.getInstance().getAvailableCopies(bookId);
            System.out.println("Найдена книга: " + book + ", Доступные копии: " + availableCopies);
        } else {
            System.out.println("Книга с ID " + bookId + " не найдена.");
        }
    }
}

class Reader extends Person {
    private List<Book> borrowedBooks = new ArrayList<>();

    public Reader() {
        this.borrowedBooks = new ArrayList<>();
    }

    public Reader(int id, String firstName, String lastName, String middleName, String address) {
        setId(id);
        setFirstName(firstName);
        setLastName(lastName);
        setMiddleName(middleName);
        setAddress(address);
        this.borrowedBooks = new ArrayList<>();
    }

    public List<Book> getBorrowedBooks() {
        return borrowedBooks;
    }

    public void addBook(Book book) {
        borrowedBooks.add(book);
    }

    public void returnBook(Book book) {
        borrowedBooks.remove(book);
    }

    public void register() {
        Reader newReader = Library.getInstance().registerReader();
        setId(newReader.getId());
        setFirstName(newReader.getFirstName());
        setLastName(newReader.getLastName());
        setMiddleName(newReader.getMiddleName());
        setAddress(newReader.getAddress());
    }

    @Override
    public void run() {
        Scanner scanner = new Scanner(System.in);
        Library library = Library.getInstance();

        while (true) {
            ShowMenu.showReaderMenu();

            String input = GlobalScanner.SCANNER.nextLine().trim();

            switch (input) {
                case "1" -> register();
                case "2" -> borrowBook();
                case "3" -> returnBook();
                case "4" -> showBorrowedBooks();
                case "0" -> {
                    System.out.println("Завершена работа читателя.");
                    return;
                }
                default -> {
                    System.out.println("Ошибка: введите число от 0 до 4.");
                }
            }
        }
    }

    private void borrowBook() {
        if (id == -1) {
            System.out.println("Читатель не зарегистрирован.");
            return;
        }

        Librarian Librarian = new Librarian();
        Librarian.giveBook();
    }

    private void returnBook() {
        if (id == -1) {
            System.out.println("Читатель не зарегистрирован.");
            return;
        }

        Librarian Librarian = new Librarian();
        Librarian.returnBook();
    }

    private void showBorrowedBooks() {
        if (id == -1) {
            System.out.println("Читатель не зарегистрирован.");
            return;
        }

        Library library = Library.getInstance();
        library.showBorrowedBooksForReader(id);
    }
}
