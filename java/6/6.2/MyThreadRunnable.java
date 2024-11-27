public class MyThreadRunnable extends Thread {
    private final String name;
    private final Object obj;

    public MyThreadRunnable(String name)
    {
        this.name=name;
        obj=new Object();
    }

    @Override
    public void run() {
        printState();
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        synchronized (obj) {
            try {
                obj.wait();
            } catch (InterruptedException ex) {
                throw new RuntimeException(ex);
            }
        }
        printState();
    }

    @Override
    public void start()
    {
        printState();
        super.start();
    }

    public void printState()
    {
        System.out.println("Thread State: " + super.getState());
    }

    public void threadNotify()
    {
        synchronized (obj) {
            obj.notify();
        }
    }
}
