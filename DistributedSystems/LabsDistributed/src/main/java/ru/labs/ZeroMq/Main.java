package ru.labs.ZeroMq;

public class Main {
    public static void main(String... args) throws Exception{
        Proxy proxy = new Proxy();
        new Thread(proxy).start();
        Thread.sleep(1000);

        for(int i = 1 ; i < 3 ; i++){
            HttpServer server = new HttpServer(8080 + i * 4);
            new Thread(server::perform).start();
        }

        HttpServer server = new HttpServer(8080);
        server.perform();
    }
}
