package ru.labs.ZeroMq;

import org.zeromq.ZMQ;

public class PullSocket implements Runnable {
    private ZMQ.Socket pull;
    private ZMQ.Socket pub;
    private ZMQ.Context context;

    PullSocket(int port){
        context = ZMQ.context(1);
        pub = context.socket(ZMQ.PUB);
        pull = context.socket(ZMQ.PULL);
        int pullPort = port + 3;
        pull.bind("tcp://localhost:"+pullPort);
        pub.connect("tcp://localhost:5555");
    }

    @Override
    public void run(){
        while (!Thread.currentThread().isInterrupted()){
            String msg = pull.recvStr();
            pub.send(msg,0);
        }
    }
}
