package ru.labs.ZeroMq;

import org.zeromq.ZMQ;

public class Proxy implements Runnable{
    private ZMQ.Socket xsub;
    private ZMQ.Socket xpub;
    private ZMQ.Context context;

    Proxy(){
        context = ZMQ.context(1);
        xpub = context.socket(ZMQ.XPUB);
        xsub = context.socket(ZMQ.XSUB);
        xpub.bind("tcp://localhost:5556");
        xsub.bind("tcp://localhost:5555");
    }

    @Override
    public void run(){
        ZMQ.proxy(xsub,xpub,null);
        xsub.close();
        xpub.close();
        context.term();
    }
}
