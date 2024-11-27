import java.util.Comparator;
import java.util.NoSuchElementException;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

interface IMyDoublyLinkedList<T>
{
    public void pushBegin(T element);
    public void pushEnd(T element);
    public void pushAt(T element, int index);

    public void removeBegin();
    public void removeEnd();
    public void removeAt(int index);

    public void replace(T element, int index);

    Stream<T> stream();
    void sort(Comparator<T> comparator);
}

class MyDoublyLinkedList<T> implements IMyDoublyLinkedList<T> {

    private class Node {
        T data;
        Node next;
        Node prev;

        Node(T data) {
            this.data = data;
        }
    }

    private Node head;
    private Node tail;
    private int size;

    public MyDoublyLinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }

    public void pushBegin(T element) {
        Node temp = new Node(element);
        if (head == null) {
            head = temp;
            tail = temp;
        }
        else {
            temp.next = head;
            head.prev = temp;
            head = temp;
        }
        size++;
    }

    public void pushEnd(T element) {
        Node temp = new Node(element); 
        if (tail == null) {
            head = temp;
            tail = temp;
        }
        else {
            tail.next = temp;
            temp.prev = tail;
            tail = temp;
        }
        size++;
    }

    public void pushAt(T element, int index) {
        Node temp = new Node(element); 
        if (index == 1) {
            pushBegin(element);
        }
        else {
            Node current = head;
            int currIndex = 1;
            while (current != null && currIndex < index) {
                current = current.next;
                currIndex++;
            } 
            if (current == null) {
                pushEnd(element);
            } 
            else {
                temp.next = current;
                temp.prev = current.prev;
                current.prev.next = temp;
                current.prev = temp;
            }
        }
        size++;
    }

    public void removeBegin() {
        if (head == null) {
            return;
        }
    
        if (head == tail) {
            head = null;
            tail = null;
            size--;
            return;
        }
    
        Node temp = head;
        head = head.next;
        head.prev = null;
        temp.next = null;
        size--;
    }

    public void removeEnd() {
        if (tail == null) {
            return;
        }
    
        if (head == tail) {
            head = null;
            tail = null;
            size--;
            return;
        }
    
        Node temp = tail;
        tail = tail.prev;
        tail.next = null;
        temp.prev = null;
        size--;
    }

    public void removeAt(int index) {
        if (head == null) { 
            return;
        }
    
        if (index == 1) {
            removeBegin();
            return;
        }
    
        Node current = head;
        int count = 1;
    
        while (current != null && count != index) {
            current = current.next;
            count++;
        }
    
        if (current == null) {
            System.out.println("Position wrong"); 
            return;
        }
    
        if (current == tail) {
            removeEnd();
            return;
        }
    
        current.prev.next = current.next;
        current.next.prev = current.prev;
        current.prev = null;
        current.next = null;
        size--;
    }

    public void replace(T element, int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Invalid index: " + index);
        }

        Node current;
        if (index < size / 2) {
            current = head;
            for (int i = 0; i < index; i++) {
                current = current.next;
            }
        } else {
            current = tail;
            for (int i = size - 1; i > index; i--) {
                current = current.prev;
            }
        }

        current.data = element;
    }

    public void sort(Comparator<T> comparator) {
        if (size < 2) return;

        for (Node i = head; i != null; i = i.next) {
            for (Node j = i.next; j != null; j = j.next) {
                if (comparator.compare(i.data, j.data) > 0) {
                    T temp = i.data;
                    i.data = j.data;
                    j.data = temp;
                }
            }
        }
    }

    public Stream<T> stream() {
        return StreamSupport.stream(
                new Iterable<T>() {
                    @Override
                    public java.util.Iterator<T> iterator() {
                        return new java.util.Iterator<T>() {
                            private Node current = head;

                            @Override
                            public boolean hasNext() {
                                return current != null;
                            }

                            @Override
                            public T next() {
                                if (current == null) throw new NoSuchElementException();
                                T data = current.data;
                                current = current.next;
                                return data;
                            }
                        };
                    }
                }.spliterator(), false);
    }
}

public class Main {
    public static void main(String[] args) {
        MyDoublyLinkedList<Integer> list = new MyDoublyLinkedList<>();

        list.pushEnd(5);
        list.pushEnd(2);
        list.pushEnd(8);
        list.pushEnd(3);

        System.out.println("Изначальный список:");
        list.stream().forEach(System.out::println);

        list.pushAt(10, 2);
        System.out.println("\nПосле вставки 10 в индекс 2:");
        list.stream().forEach(System.out::println);

        list.replace(20, 1);
        System.out.println("\nПосле замены элемента в индексе 1 на 20:");
        list.stream().forEach(System.out::println);

        list.removeAt(3);
        System.out.println("\nПосле удаления элемента в индексе 3:");
        list.stream().forEach(System.out::println);

        list.sort(Comparator.naturalOrder());
        System.out.println("\nПосле сортировки по возрастанию:");
        list.stream().forEach(System.out::println);

        System.out.println("\nЧисла больше 5:");
        list.stream()
            .filter(x -> x > 5)
            .forEach(System.out::println);
    }
}
