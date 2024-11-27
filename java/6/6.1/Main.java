public class Main {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("The different states of a thread are: ");

        for (Thread.State state : Thread.State.values()) {
            System.out.print(state+" ");
        }

        System.out.print("\nLet's get practical:\n");

        MyThreadRunnable t = new MyThreadRunnable("Thread States");

        t.start();
        Thread.sleep(500);
        t.printState();

        t.join(3000);
        t.printState();
        t.threadNotify();

        synchronized (t) {
            t.notifyAll();
        }

        t.printState();

        t.join();
        t.printState();

        System.out.println("\nThread execution completed.");
    }
}
