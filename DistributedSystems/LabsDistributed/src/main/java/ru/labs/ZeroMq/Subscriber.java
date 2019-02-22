package ru.labs.ZeroMq;

import io.undertow.websockets.WebSocketProtocolHandshakeHandler;
import io.undertow.websockets.core.WebSocketChannel;
import io.undertow.websockets.core.WebSockets;
import org.zeromq.ZMQ;

public class Subscriber implements Runnable{
    private ZMQ.Socket sub;
    private ZMQ.Context context;
    private WebSocketProtocolHandshakeHandler webSocketHandler;

    Subscriber(WebSocketProtocolHandshakeHandler webSocketHandler){
        this.webSocketHandler = webSocketHandler;
        context = ZMQ.context(1);
        sub = context.socket(ZMQ.SUB);
        sub.connect("tcp://localhost:5556");
        sub.subscribe("");
    }

    @Override
    public void run(){
        while (!Thread.currentThread().isInterrupted()){
            String msg = sub.recvStr(0);
            for (WebSocketChannel session : webSocketHandler.getPeerConnections()) {
                WebSockets.sendText(msg, session, null);
            }
        }
    }
}
