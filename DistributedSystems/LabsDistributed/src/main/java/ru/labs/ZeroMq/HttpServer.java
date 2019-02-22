package ru.labs.ZeroMq;

import io.undertow.Handlers;
import io.undertow.Undertow;
import io.undertow.server.handlers.resource.ClassPathResourceManager;
import io.undertow.server.handlers.resource.ResourceHandler;
import io.undertow.util.Headers;
import io.undertow.websockets.WebSocketProtocolHandshakeHandler;
import io.undertow.websockets.core.AbstractReceiveListener;
import io.undertow.websockets.core.BufferedTextMessage;
import io.undertow.websockets.core.WebSocketChannel;
import org.zeromq.ZMQ;



public class HttpServer {
    private int port;
    private ZMQ.Context context;
    private Subscriber sub;
    private PullSocket pullPub;
    private final ThreadLocal<ZMQ.Socket> socket = new ThreadLocal<>();

    HttpServer(int port){
        this.port = port;
        this.context = ZMQ.context(1);
        this.pullPub = new PullSocket(port);
    }

    public void perform() {
        WebSocketProtocolHandshakeHandler websocketHandler = Handlers.websocket((exchange, channel) -> {
            channel.getReceiveSetter().set(new AbstractReceiveListener() {
                @Override
                protected void onFullTextMessage(WebSocketChannel channel, BufferedTextMessage message) {
                    final String messageData = message.getData();
                    ZMQ.Socket sock = socket.get();
                    if(sock == null){
                        sock = context.socket(ZMQ.PUSH);
                        int proxyPort = port + 3;
                        sock.connect("tcp://localhost:"+proxyPort);
                        socket.set(sock);
                    }
                    sock.send(messageData);
                }
            });
            channel.resumeReceives();
        });

        this.sub = new Subscriber(websocketHandler);
        new Thread(sub).start();
        new Thread(pullPub).start();

        ResourceHandler resourceHandler = Handlers.resource(new ClassPathResourceManager(HttpServer.class.getClassLoader(), ""))
                .addWelcomeFiles("index.html");

        Undertow server = Undertow.builder()
                .addHttpListener(port, "localhost")
                .setHandler(Handlers.path()
                        .addPrefixPath("/chatsocket", websocketHandler)
                        .addPrefixPath("/", resourceHandler)
                        .addPrefixPath("/connections", Handlers.path(exchange -> {
                            exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/plain");
                            exchange.getResponseSender().send("" + websocketHandler.getPeerConnections().size());
                        }))
                )
                .build();
        server.start();
    }
}
