import java.util.*;

class Client {
    String name;
    String city;
    
    public Client(String name, String city) {
        this.name = name;
        this.city = city;
    }

    @Override
    public String toString() {
        return "Клиент: " + name + ", Город: " + city;
    }
}

class ClientPriorityComparator implements Comparator<Client> {
    private static final Set<String> LOCAL_CITIES = new HashSet<>(Arrays.asList("Местный город", "Близлежащий город"));
    
    @Override
    public int compare(Client c1, Client c2) {
        if (LOCAL_CITIES.contains(c1.city) && !LOCAL_CITIES.contains(c2.city)) {
            return 1;
        } else if (!LOCAL_CITIES.contains(c1.city) && LOCAL_CITIES.contains(c2.city)) {
            return -1;
        }
        return c1.name.compareTo(c2.name);
    }
}

public class Main {
    public static void main(String[] args) {
        PriorityQueue<Client> queue = new PriorityQueue<>(new ClientPriorityComparator());
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.println("Введите данные клиента:");
            System.out.print("Имя клиента: ");
            String name = scanner.nextLine();
            
            System.out.print("Город клиента: ");
            String city = scanner.nextLine();
            
            Client client = new Client(name, city);
            queue.add(client);
            
            System.out.println("Клиент добавлен в очередь.");
            
            System.out.print("Хотите ли вы добавить еще одного клиента? (y/n): ");
            String response = scanner.nextLine();
            if (response.equalsIgnoreCase("n")) {
                break;
            }
        }
        
        System.out.println("\nОбслуживание клиентов:");
        while (!queue.isEmpty()) {
            Client nextClient = queue.poll();
            System.out.println(nextClient);
        }

        scanner.close();
    }
}
