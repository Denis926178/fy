public class MyThreadRunnable implements Runnable {
    private Thread t;
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

    public void start()
    {
        t=new Thread(this,name);
        printState();
        t.start();
    }

    public void printState()
    {
        if (t != null) {
            System.out.println("Thread State: " + t.getState());
        } else {
            System.out.println("Thread not started yet.");
        }
    }

    public void join() {
        try {
            t.join();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
    public  void join(int millis) {
        try {
            t.join(millis);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public void threadNotify()
    {
        synchronized (obj) {
            obj.notify();
        }
    }
}
